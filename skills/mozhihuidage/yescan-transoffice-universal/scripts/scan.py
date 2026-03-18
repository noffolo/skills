#!/usr/bin/env python3
"""
Quark OCR - 夸克扫描王 OCR 识别服务
支持图片 URL、本地文件路径（自动转 BASE64）、BASE64 字符串
"""
import argparse
import json
import os
import sys
import base64
import binascii
import logging
from typing import Tuple, Dict, Any, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from requests.exceptions import Timeout, ConnectionError

# --- 配置常量 ---
API_URL = "https://scan-business.quark.cn/vision"

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}

# 文件大小限制（5MB），与代码保持一致
MAX_FILE_SIZE = 5 * 1024 * 1024

# 请求超时时间（秒）
REQUEST_TIMEOUT = 120

# API 成功响应码
SUCCESS_CODE = "00000"

# 错误码消息常量
ERR_MSG_A0211_QUOTA_INSUFFICIENT = "请前往https://scan.quark.cn/business，登录开发者后台，选择需要的套餐进行充值（请注意购买Skill专用套餐）"

# 配置日志
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def _mask_api_key(api_key: str) -> str:
    """
    脱敏 API Key，只显示前 4 位和后 4 位

    Args:
        api_key: 原始 API Key

    Returns:
        脱敏后的 API Key，如：abcd****efgh
    """
    if not api_key or len(api_key) < 8:
        return "****"
    return f"{api_key[:4]}****{api_key[-4:]}"

# 导入文件保存器
try:
    from file_saver import FileSaver
except ImportError:
    logger.warning("FileSaver not available, file saving will be disabled")
    FileSaver = None

@dataclass
class OCRResult:
    """OCR 识别结果 - 直接返回 API 原始响应"""
    code: str
    message: Optional[str]
    data: Optional[Dict[str, Any]]  # 原始 API 返回的 data 字段

    def to_json(self) -> str:
        """返回完整的 API 响应结构"""
        return json.dumps({
            "code": self.code,
            "message": self.message,
            "data": self.data
        }, ensure_ascii=False, indent=2)

class URLValidator:
    """URL 基础验证器"""

    @staticmethod
    def validate(url: str) -> Tuple[bool, Optional[str]]:
        if not url or not isinstance(url, str):
            return False, "URL cannot be empty"

        url = url.strip()

        try:
            parsed = urlparse(url)
        except ValueError as e:
            return False, f"Invalid URL format: {str(e)}"

        if parsed.scheme.lower() not in {"http", "https"}:
            return False, f"Protocol '{parsed.scheme}' not allowed."

        return True, None

class CredentialManager:
    @staticmethod
    def load() -> str:
        api_key = os.getenv("SCAN_WEBSERVICE_KEY", "").strip()
        if api_key:
            logger.info(f"API Key loaded successfully: {_mask_api_key(api_key)}")
            return api_key
        raise ValueError(
            "⚠️ 环境变量 SCAN_WEBSERVICE_KEY 未配置\n\n"
            "夸克扫描王 OCR 服务需要 API Key 才能使用。\n\n"
            "🔧 如何获取密钥？官方入口在此：\n"
            "请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看API Key→ \n"
            "⚠️ 注意：若你点击链接后跳转到其他域名（如 scan.quark.cn 或 open.quark.com），\n"
            "说明该链接已失效 —— 请直接在浏览器地址栏手动输入 https://scan.quark.cn/business\n"
            "（这是当前唯一有效的官方入口）。\n\n"
            "获取密钥后，在终端执行：\n"
            "  export SCAN_WEBSERVICE_KEY=\"your_key_here\"\n"
            "然后重新运行 OCR 命令即可。"
        )

class QuarkOCRClient:
    def __init__(self, api_key: str, service_option: str, input_configs: str,
                 output_configs: str, data_type: str):
        self.api_key = api_key
        self.service_option = service_option
        self.input_configs = input_configs
        self.output_configs = output_configs
        self.data_type = data_type
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def recognize(self, image_url: str = None, image_path: str = None, base64_data: str = None) -> OCRResult:
        """
        识别图片内容
        - image_url: 公网图片 URL
        - image_path: 本地文件路径（自动转 BASE64）
        - base64_data: base64 字符串
        """
        # 验证参数：确保只有一个参数被传入
        provided_params = sum(param is not None for param in [image_url, image_path, base64_data])
        if provided_params != 1:
            return OCRResult(
                code="INVALID_INPUT",
                message="Exactly one of image_url, image_path, or base64_data must be provided",
                data=None
            )

        if base64_data:
            return self._recognize_base64(base64_data)
        elif image_path:
            return self._recognize_local_file(image_path)
        else:
            is_valid, error_msg = URLValidator.validate(image_url)
            if not is_valid:
                return OCRResult(code="URL_VALIDATION_ERROR", message=f"URL validation failed: {error_msg}", data=None)
            param = self._build_request_param(image_url=image_url)
            response = self._send_request(param)
            return self._parse_response(response)

    def _recognize_base64(self, base64_data: str) -> OCRResult:
        """
        处理 base64 字符串，支持两种格式：
        1. 纯 BASE64 字符串：/9j/4AAQSkZJRg...
        2. Data URL 格式：data:image/jpeg;base64,/9j/4AAQSkZJRg...
        """
        base64_content = base64_data.strip()

        # 检查是否是 Data URL 格式
        if base64_content.startswith('data:'):
            # 格式: data:image/jpeg;base64,/9j/4AAQ...
            try:
                if ';base64,' in base64_content:
                    # 提取 base64 部分
                    base64_content = base64_content.split(';base64,', 1)[1]
                else:
                    return OCRResult(
                        code="BASE64_FORMAT_ERROR",
                        message="Invalid Data URL format, expected format: data:image/jpeg;base64,<base64_string>",
                        data=None
                    )
            except (ValueError, IndexError) as e:
                return OCRResult(
                    code="BASE64_PARSE_ERROR",
                    message=f"Failed to parse Data URL: {str(e)}",
                    data=None
                )

        # 验证 base64 格式
        try:
            base64.b64decode(base64_content)
        except (ValueError, binascii.Error) as e:
            return OCRResult(code="BASE64_DECODE_ERROR", message=f"Invalid base64 string: {str(e)}", data=None)

        # 使用 base64 方式调用 OCR
        param = self._build_request_param(base64_data=base64_content)
        response = self._send_request(param)
        return self._parse_response(response)

    def _recognize_local_file(self, file_path: str) -> OCRResult:
        """
        处理本地文件：读取文件并转为 BASE64 后调用 OCR
        """
        file_path = os.path.expanduser(file_path.strip())

        # 验证文件
        is_valid, error_msg = self._validate_local_file(file_path)
        if not is_valid:
            return OCRResult(code="FILE_ERROR", message=f"File validation failed: {error_msg}", data=None)

        # 读取文件并转为 base64
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')
        except (IOError, OSError) as e:
            return OCRResult(code="FILE_READ_ERROR", message=f"Failed to read file: {str(e)}", data=None)

        # 使用 dataBase64 参数调用 OCR
        param = self._build_request_param(base64_data=base64_content)
        response = self._send_request(param)
        return self._parse_response(response)

    def _validate_local_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        if not file_path or not isinstance(file_path, str):
            return False, "File path cannot be empty"

        file_path = os.path.expanduser(file_path.strip())

        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        if not os.path.isfile(file_path):
            return False, f"Not a file: {file_path}"

        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return False, f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024}MB limit"

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return False, f"File extension '{ext}' not allowed"

        return True, None

    def _build_request_param(self, image_url: str = None, base64_data: str = None) -> Dict[str, Any]:
        """
        构建请求参数，严格按照 SKILL.md 中的格式
        注意：inputConfigs 和 outputConfigs 必须是 JSON 字符串（带引号）
        """
        param = {
            "aiApiKey": self.api_key,
            "clientId": "openclaw-yescan",  # 客户端标识
            "dataType": self.data_type,
            "serviceOption": self.service_option,
            "inputConfigs": self.input_configs,
            "outputConfigs": self.output_configs
        }

        # 根据输入类型选择使用 dataUrl 或 dataBase64（互斥）
        if base64_data:
            param["dataBase64"] = base64_data
        else:
            param["dataUrl"] = image_url

        return param

    def _send_request(self, param: Dict[str, Any]) -> requests.Response:
        headers = {"Content-Type": "application/json"}
        # 脱敏 API Key 后记录日志
        masked_key = _mask_api_key(param.get("aiApiKey", ""))
        logger.info(f"Sending OCR request with API Key: {masked_key}")
        response = self.session.post(
            API_URL,
            json=param,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )
        return response

    def _parse_response(self, response: requests.Response) -> OCRResult:
        """直接返回 API 原始响应，不做任何加工处理"""
        if response.status_code != 200:
            error_msg = response.text[:200] if response.text else "No error message"
            return OCRResult(
                code="HTTP_ERROR",
                message=f"HTTP {response.status_code}: {error_msg}",
                data=None
            )
        try:
            body = response.json()
        except json.JSONDecodeError as e:
            return OCRResult(
                code="JSON_PARSE_ERROR",
                message=f"Failed to parse JSON: {str(e)}",
                data=None
            )

        # 直接返回 API 的原始响应
        code = body.get("code", "unknown")
        message = body.get("message")
        data = body.get("data")

        # 特殊处理 A0211 错误码（配额/余额不足）
        if code == "A0211":
            message = ERR_MSG_A0211_QUOTA_INSUFFICIENT

        return OCRResult(code=code, message=message, data=data)

def _validate_json_config(config_str: str, config_name: str) -> None:
    """
    验证 JSON 配置格式

    Args:
        config_str: JSON 字符串
        config_name: 配置名称（用于错误提示）

    Raises:
        ValueError: JSON 格式错误时抛出
    """
    try:
        json.loads(config_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid {config_name} JSON: {str(e)}")

def _save_files_from_result(result: OCRResult) -> OCRResult:
    """
    从 OCR 结果中提取并保存文件（仅 Word、Excel，不保存图片）

    Args:
        result: OCR 识别结果

    Returns:
        更新后的 OCR 结果（data 中只包含 path 字段）
    """
    if not FileSaver:
        logger.warning("FileSaver not available, skipping file save")
        return result

    # 支持的数据结构：
    # Word/Excel: result.data['TypesetInfo'][0]['FileBase64'] + ['FileType']

    saved_files = []

    # 处理 TypesetInfo（Word/Excel 文件）
    if isinstance(result.data, dict) and "TypesetInfo" in result.data:
        typeset_info_list = result.data["TypesetInfo"]
        if isinstance(typeset_info_list, list) and len(typeset_info_list) > 0:
            for typeset_info in typeset_info_list:
                if isinstance(typeset_info, dict) and "FileBase64" in typeset_info and "FileType" in typeset_info:
                    file_base64 = typeset_info["FileBase64"]
                    file_type = typeset_info["FileType"].lower()

                    if result.code == SUCCESS_CODE and file_base64:
                        try:
                            saver = FileSaver()
                            save_res = None

                            # 根据文件类型选择保存方法
                            if file_type == "word":
                                save_res = saver.save_word_from_base64(file_base64)
                            elif file_type == "excel":
                                save_res = saver.save_excel_from_base64(file_base64)
                            else:
                                logger.warning(f"Unsupported file type: {file_type}")
                                continue

                            if save_res and save_res["code"] == 0:
                                saved_files.append({
                                    "type": file_type,
                                    "path": save_res["data"]["path"]
                                })
                                logger.info(f"{file_type.capitalize()} file saved to: {save_res['data']['path']}")
                            else:
                                error_msg = save_res.get("msg", "Unknown error") if save_res else "Save failed"
                                logger.error(f"Failed to save {file_type} file: {error_msg}")
                        except Exception as e:
                            logger.error(f"{file_type.capitalize()} file save exception: {str(e)}", exc_info=True)

    # 更新结果：如果有保存的文件，返回文件列表；否则保持原样
    if saved_files:
        result.data = {"files": saved_files}

    return result

def main():
    parser = argparse.ArgumentParser(
        description="Quark OCR - 支持图片 URL、本地路径（自动转 BASE64）、BASE64 字符串",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 通用 OCR（URL）
  python3 scan.py \\
    --url "https://example.com/image.jpg" \\
    --service-option "structure" \\
    --input-configs '{"function_option": "RecognizeGeneralDocument"}' \\
    --output-configs '{"need_return_image": "True"}' \\
    --data-type "image"
  
  # 身份证识别（本地文件）
  python3 scan.py \\
    --path "/path/to/idcard.jpg" \\
    --service-option "structure" \\
    --input-configs '{"function_option": "RecognizeIDCard"}' \\
    --output-configs '{"need_return_image": "True"}' \\
    --data-type "image"
  
  # 文件扫描（BASE64）
  python3 scan.py \\
    --base64 "iVBORw0KGgo..." \\
    --service-option "scan" \\
    --input-configs '{"function_option": "work_scene"}' \\
    --output-configs '{"need_return_image": "True"}' \\
    --data-type "image"
        """
    )

    # 图片输入参数（三选一，必需）
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", "-u", help="图片 URL（如：https://example.com/image.jpg）")
    group.add_argument("--path", "-p", help="本地图片文件路径（自动转 BASE64）")
    group.add_argument("--base64", "-b", help="BASE64 字符串，支持纯 BASE64 或 Data URL 格式（如：data:image/jpeg;base64,/9j/...）")

    # API 参数（必需）
    parser.add_argument(
        "--service-option",
        required=True,
        help='serviceOption 参数（如：structure, ocr, scan）'
    )
    parser.add_argument(
        "--input-configs",
        required=True,
        help='inputConfigs JSON 字符串（如：\'{"function_option": "RecognizeGeneralDocument"}\'）'
    )
    parser.add_argument(
        "--output-configs",
        required=True,
        help='outputConfigs JSON 字符串（如：\'{"need_return_image": "True"}\'）'
    )
    parser.add_argument(
        "--data-type",
        required=True,
        choices=["image", "pdf"],
        help="数据类型（image 或 pdf）"
    )

    args = parser.parse_args()

    # 验证 JSON 参数格式
    try:
        _validate_json_config(args.input_configs, "input-configs")
        _validate_json_config(args.output_configs, "output-configs")
    except ValueError as e:
        print(OCRResult(code="INVALID_JSON", message=str(e), data=None).to_json())
        sys.exit(1)

    try:
        api_key = CredentialManager.load()
        with QuarkOCRClient(
            api_key=api_key,
            service_option=args.service_option,
            input_configs=args.input_configs,
            output_configs=args.output_configs,
            data_type=args.data_type
        ) as client:
            if args.base64:
                result = client.recognize(base64_data=args.base64)
            elif args.url:
                result = client.recognize(image_url=args.url)
            else:
                result = client.recognize(image_path=args.path)

        # 保存文件（如果返回结果包含文件）
        result = _save_files_from_result(result)

        # 输出识别结果
        print(result.to_json())
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(OCRResult(code="CONFIG_ERROR", message=str(e), data=None).to_json())
        sys.exit(1)
    except Timeout:
        logger.error("Request timed out")
        print(OCRResult(code="TIMEOUT", message="Request timed out", data=None).to_json())
        sys.exit(1)
    except ConnectionError as e:
        logger.error(f"Network error: {str(e)}")
        print(OCRResult(code="NETWORK_ERROR", message=f"Network failed: {str(e)}", data=None).to_json())
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(OCRResult(code="UNKNOWN_ERROR", message=f"Unexpected error: {str(e)}", data=None).to_json())
        sys.exit(1)

if __name__ == "__main__":
    main()