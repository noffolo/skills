import requests
import re
import json
import os
import sys
import subprocess
from datetime import datetime

# API 配置
API_URL = "http://119.91.237.2:5432/taobao_item_month_sale"
API_TOKEN = "tbmonthsale1124"
API_VERSION = "6.0"
MAX_FREE_USAGE = 10  # 免费使用次数上限

# 使用次数记录文件路径
USAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".usage_count")


def get_usage_count() -> int:
    """获取当前使用次数"""
    try:
        if os.path.exists(USAGE_FILE):
            with open(USAGE_FILE, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0


def increment_usage_count() -> int:
    """增加使用次数并返回新值"""
    count = get_usage_count() + 1
    try:
        with open(USAGE_FILE, "w") as f:
            f.write(str(count))
    except:
        pass
    return count


def check_usage_limit() -> str:
    """检查使用次数是否超限，返回提示信息或None"""
    if get_usage_count() >= MAX_FREE_USAGE:
        return f"免费额度已用完（{MAX_FREE_USAGE}次），请联系开发者 tom.yan@earlydata.com 购买token额度"
    return None

# 自动安装依赖库
def install_dependencies():
    required_packages = ["requests"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()


def extract_item_id(item_url: str) -> str:
    """
    从淘宝/天猫商品链接中提取商品ID
    支持格式：
    - https://item.taobao.com/item.htm?id=123456789
    - https://detail.tmall.com/item.htm?id=123456789
    - 短链接等
    """
    if not item_url:
        return None
    
    # 匹配 id= 后的数字
    patterns = [
        r'[?&]id=(\d+)',           # 标准链接
        r'[?&]itemId=(\d+)',       # 部分变体
        r'/item/(\d+)',            # 短链接格式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, item_url)
        if match:
            return match.group(1)
    
    # 若链接本身就是纯数字ID
    if item_url.strip().isdigit():
        return item_url.strip()
    
    return None


async def get_tb_month_sale(item_id: str = None, item_url: str = None, export: bool = False, export_path: str = None) -> str:
    """
    查询淘宝/天猫商品月销量
    
    参数：
    item_id: 商品ID（与 item_url 二选一）
    item_url: 商品链接（支持淘宝/天猫链接，自动解析ID）
    export: 是否导出结果为文件（默认 False）
    export_path: 导出路径（默认桌面 tb_sale_result.json）
    
    返回：
    查询结果字符串
    """
    # 0. 检查使用次数限制
    limit_msg = check_usage_limit()
    if limit_msg:
        return limit_msg
    
    # 1. 参数校验：提取商品ID
    if not item_id and not item_url:
        return "查询失败：请提供商品ID或商品链接（支持淘宝/天猫）"
    
    if not item_id:
        item_id = extract_item_id(item_url)
        if not item_id:
            return "查询失败：无法识别的链接格式，请提供有效的淘宝/天猫商品链接"
    
    # 确保item_id是纯数字
    item_id = str(item_id).strip()
    if not item_id.isdigit():
        return "查询失败：商品ID格式无效，请提供正确的数字ID"
    
    # 2. 调用API查询
    try:
        params = {
            "itemId": item_id,
            "token": API_TOKEN,
            "v": API_VERSION
        }
        
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 3. 解析返回数据
        if not data:
            return "查询失败：该商品不存在或已下架，请确认商品ID/链接是否正确"
        
        # 根据实际API返回格式解析数据
        result = {
            "item_id": item_id,
            "data": data,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 4. 导出结果（若需要）
        if export:
            if not export_path:
                if sys.platform == "win32":
                    export_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "tb_sale_result.json")
                else:
                    export_path = os.path.expanduser("~/Desktop/tb_sale_result.json")
            
            export_dir = os.path.dirname(export_path)
            if export_dir and not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 查询成功，增加使用次数
            current_count = increment_usage_count()
            remaining = MAX_FREE_USAGE - current_count
            usage_tip = f"\n（剩余免费次数：{remaining}）" if remaining > 0 else f"\n（免费额度已用完，请联系 tom.yan@earlydata.com 购买token额度）"
            
            return f"查询成功！\n商品ID：{item_id}\n返回数据：{json.dumps(data, ensure_ascii=False)}\n结果已导出到：{export_path}{usage_tip}"
        
        # 查询成功，增加使用次数
        current_count = increment_usage_count()
        remaining = MAX_FREE_USAGE - current_count
        usage_tip = f"\n（剩余免费次数：{remaining}）" if remaining > 0 else f"\n（免费额度已用完，请联系 tom.yan@earlydata.com 购买token额度）"
        
        return f"查询成功！\n商品ID：{item_id}\n返回数据：{json.dumps(data, ensure_ascii=False)}{usage_tip}"
    
    except requests.exceptions.Timeout:
        return "查询失败：网络请求超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "查询失败：网络连接失败，请检查网络后重试"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "查询失败：请求过于频繁，请稍后再试"
        return f"查询失败：服务器错误（HTTP {e.response.status_code}）"
    except json.JSONDecodeError:
        return "查询失败：接口返回数据格式异常"
    except PermissionError:
        return f"查询成功但导出失败：无权限写入指定路径（{export_path}），请更换保存路径"
    except Exception as e:
        return f"查询失败：未知错误 - {str(e)}"


async def batch_get_tb_month_sale(item_ids: list, export: bool = False, export_path: str = None) -> str:
    """
    批量查询商品月销量
    
    参数：
    item_ids: 商品ID列表（最多20个）
    export: 是否导出结果
    export_path: 导出路径
    """
    if not item_ids:
        return "查询失败：请提供商品ID列表"
    
    if len(item_ids) > 20:
        return "查询失败：单次最多支持查询20个商品，请分批查询"
    
    results = []
    for item_id in item_ids:
        result = await get_tb_month_sale(item_id=str(item_id))
        results.append({"item_id": item_id, "result": result})
    
    # 导出结果
    if export:
        if not export_path:
            if sys.platform == "win32":
                export_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "tb_sale_batch_result.json")
            else:
                export_path = os.path.expanduser("~/Desktop/tb_sale_batch_result.json")
        
        export_dir = os.path.dirname(export_path)
        if export_dir and not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return f"批量查询完成！共查询 {len(item_ids)} 个商品\n结果已导出到：{export_path}"
    
    return f"批量查询完成！共查询 {len(item_ids)} 个商品\n" + "\n".join([f"- {r['result']}" for r in results])
