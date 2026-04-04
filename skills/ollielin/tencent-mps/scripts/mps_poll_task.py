#!/usr/bin/env python3
"""
腾讯云 MPS 任务轮询工具模块

提供 poll_video_task() 和 poll_image_task() 两个函数，
供各处理脚本在提交任务后直接内置轮询等待，无需 Agent 手动启动查询。

用法（被其他脚本 import）：
    from mps_poll_task import poll_video_task, poll_image_task

    # 提交任务后直接轮询
    result = poll_video_task(task_id, region="ap-guangzhou", interval=10, max_wait=1800)
    result = poll_image_task(task_id, region="ap-guangzhou", interval=5, max_wait=300)
"""

import json
import os
import sys
import time

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK：pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False


STATUS_MAP = {
    "WAITING": "等待中",
    "PROCESSING": "处理中",
    "FINISH": "已完成",
    "SUCCESS": "成功",
    "FAIL": "失败",
}


def _get_credentials():
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("错误：请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def _create_client(region):
    cred = _get_credentials()
    http_profile = HttpProfile()
    http_profile.endpoint = "mps.tencentcloudapi.com"
    http_profile.reqMethod = "POST"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def _fmt(status):
    return STATUS_MAP.get(status, status)


def _print_video_result(result):
    """打印音视频任务结果摘要（含输出文件路径）。"""
    workflow_task = result.get("WorkflowTask") or {}
    result_set = workflow_task.get("MediaProcessResultSet") or []

    TASK_KEY_MAP = {
        "Transcode": "TranscodeTask",
        "AnimatedGraphics": "AnimatedGraphicsTask",
        "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
        "SampleSnapshot": "SampleSnapshotTask",
        "ImageSprites": "ImageSpritesTask",
        "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
    }
    TASK_NAME_MAP = {
        "Transcode": "转码",
        "AnimatedGraphics": "转动图",
        "SnapshotByTimeOffset": "时间点截图",
        "SampleSnapshot": "采样截图",
        "ImageSprites": "雪碧图",
        "AdaptiveDynamicStreaming": "自适应码流",
        "AiAnalysis": "AI 内容分析",
        "AiRecognition": "AI 内容识别",
    }

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        type_name = TASK_NAME_MAP.get(task_type, task_type)
        task_key = TASK_KEY_MAP.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode", 0)
            message = task_detail.get("Message", "")
            err_str = f" | 错误码: {err_code} - {message}" if err_code != 0 else ""
            print(f"   [{i}] {type_name}: {_fmt(status)}{err_str}")

            output = task_detail.get("Output", {})
            if output:
                out_path = output.get("Path", "")
                out_storage = output.get("OutputStorage", {}) or {}
                out_type = out_storage.get("Type", "")
                if out_type == "COS":
                    cos_out = out_storage.get("CosOutputStorage", {}) or {}
                    bucket = cos_out.get("Bucket", "")
                    region = cos_out.get("Region", "")
                    print(f"       📁 输出: COS - {bucket}:{out_path} (region: {region})")
                    if bucket and out_path and _COS_SDK_AVAILABLE:
                        try:
                            cred = _get_credentials()
                            cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
                            cos_client = CosS3Client(cos_config)
                            signed_url = cos_client.get_presigned_url(
                                Bucket=bucket,
                                Key=out_path.lstrip("/"),
                                Method="GET",
                                Expired=3600
                            )
                            print(f"       🔗 下载链接（预签名，1小时有效）: {signed_url}")
                        except Exception as e:
                            print(f"       ⚠️  生成预签名 URL 失败: {e}")
                elif out_path:
                    print(f"       📁 输出: {out_path}")


def _print_image_result(result):
    """打印图片任务结果摘要（含输出文件路径和签名URL）。"""
    result_set = result.get("ImageProcessTaskResultSet") or []
    for i, item in enumerate(result_set, 1):
        status = item.get("Status", "")
        err_msg = item.get("ErrMsg", "")
        err_str = f" | 错误: {err_msg}" if err_msg else ""
        print(f"   [{i}] 状态: {_fmt(status)}{err_str}")

        output = item.get("Output") or {}
        out_path = output.get("Path", "")
        signed_url = output.get("SignedUrl", "")
        out_storage = output.get("OutputStorage", {}) or {}
        out_type = out_storage.get("Type", "")

        if out_type == "COS":
            cos_out = out_storage.get("CosOutputStorage", {}) or {}
            bucket = cos_out.get("Bucket", "")
            region = cos_out.get("Region", "")
            print(f"       📁 输出: COS - {bucket}:{out_path} (region: {region})")
        elif out_path:
            print(f"       📁 输出: {out_path}")

        if signed_url:
            print(f"       🔗 下载链接: {signed_url}")
        elif out_type == "COS" and bucket and out_path and _COS_SDK_AVAILABLE:
            try:
                cred = _get_credentials()
                cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
                cos_client = CosS3Client(cos_config)
                signed_url = cos_client.get_presigned_url(
                    Bucket=bucket,
                    Key=out_path,
                    Method="GET",
                    Expired=3600
                )
                print(f"       🔗 下载链接（预签名，1小时有效）: {signed_url}")
            except Exception as e:
                print(f"       ⚠️  生成预签名 URL 失败: {e}")

        content = output.get("Content", "")
        if content:
            display = content if len(content) <= 100 else content[:100] + "..."
            print(f"       📝 图生文结果: {display}")


def poll_video_task(task_id, region="ap-guangzhou", interval=10, max_wait=1800, verbose=False):
    """
    轮询音视频处理任务（ProcessMedia 提交的任务）直到完成。

    Args:
        task_id:   任务 ID
        region:    MPS 服务区域
        interval:  轮询间隔（秒），默认 10
        max_wait:  最长等待时间（秒），默认 1800（30分钟）
        verbose:   是否输出完整 JSON

    Returns:
        最终任务结果 dict，或 None（超时）
    """
    client = _create_client(region)
    elapsed = 0
    attempt = 0

    print(f"\n⏳ 开始轮询任务状态（间隔 {interval}s，最长等待 {max_wait}s）...")

    while elapsed < max_wait:
        attempt += 1
        try:
            req = models.DescribeTaskDetailRequest()
            req.from_json_string(json.dumps({"TaskId": task_id}))
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "")
            workflow_task = result.get("WorkflowTask") or {}
            wf_status = workflow_task.get("Status", status)

            print(f"   [{attempt}] 状态: {_fmt(wf_status)}  (已等待 {elapsed}s)")

            if wf_status == "FINISH":
                wf_err = workflow_task.get("ErrCode") or 0
                wf_msg = workflow_task.get("Message") or ""
                if wf_err != 0:
                    print(f"\n❌ 任务失败！错误码: {wf_err} - {wf_msg}")
                else:
                    print(f"\n✅ 任务完成！")
                    _print_video_result(result)

                if verbose:
                    print("\n完整响应：")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

            if wf_status == "FAIL":
                wf_err = workflow_task.get("ErrCode") or 0
                wf_msg = workflow_task.get("Message") or ""
                print(f"\n❌ 任务失败！错误码: {wf_err} - {wf_msg}")
                if verbose:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

        except TencentCloudSDKException as e:
            print(f"   [{attempt}] 查询失败: {e}，{interval}s 后重试...")

        time.sleep(interval)
        elapsed += interval

    print(f"\n⚠️  等待超时（已等待 {max_wait}s），任务可能仍在处理中。")
    print(f"   可手动查询：python scripts/mps_get_video_task.py --task-id {task_id}")
    return None


def poll_image_task(task_id, region="ap-guangzhou", interval=5, max_wait=300, verbose=False):
    """
    轮询图片处理任务（ProcessImage 提交的任务）直到完成。

    Args:
        task_id:   任务 ID
        region:    MPS 服务区域
        interval:  轮询间隔（秒），默认 5
        max_wait:  最长等待时间（秒），默认 300（5分钟）
        verbose:   是否输出完整 JSON

    Returns:
        最终任务结果 dict，或 None（超时）
    """
    client = _create_client(region)
    elapsed = 0
    attempt = 0

    print(f"\n⏳ 开始轮询任务状态（间隔 {interval}s，最长等待 {max_wait}s）...")

    while elapsed < max_wait:
        attempt += 1
        try:
            req = models.DescribeImageTaskDetailRequest()
            req.from_json_string(json.dumps({"TaskId": task_id}))
            resp = client.DescribeImageTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "")
            print(f"   [{attempt}] 状态: {_fmt(status)}  (已等待 {elapsed}s)")

            if status == "FINISH":
                err_code = result.get("ErrCode") or 0
                err_msg = result.get("ErrMsg") or ""
                if err_code != 0:
                    print(f"\n❌ 任务失败！错误码: {err_code} - {err_msg}")
                else:
                    print(f"\n✅ 任务完成！")
                    _print_image_result(result)

                if verbose:
                    print("\n完整响应：")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

            if status == "FAIL":
                err_code = result.get("ErrCode") or 0
                err_msg = result.get("ErrMsg") or ""
                print(f"\n❌ 任务失败！错误码: {err_code} - {err_msg}")
                if verbose:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

        except TencentCloudSDKException as e:
            print(f"   [{attempt}] 查询失败: {e}，{interval}s 后重试...")

        time.sleep(interval)
        elapsed += interval

    print(f"\n⚠️  等待超时（已等待 {max_wait}s），任务可能仍在处理中。")
    print(f"   可手动查询：python scripts/mps_get_image_task.py --task-id {task_id}")
    return None


# ─── 本地文件自动上传 ──────────────────────────────────────────────────────────

def auto_upload_local_file(local_path, cos_key=None, verbose=False):
    """
    检测到本地文件路径时，自动上传到 COS 并返回上传结果。

    Args:
        local_path: 本地文件路径
        cos_key:    目标 COS Key（不指定则自动生成 /input/<文件名>）
        verbose:    是否输出详细日志

    Returns:
        dict: { "Bucket", "Region", "Key", "URL", "PresignedURL" }，失败返回 None
    """
    if not os.path.isfile(local_path):
        print(f"❌ 本地文件不存在: {local_path}", file=sys.stderr)
        print(f"   请明确指定文件来源：", file=sys.stderr)
        print(f"   - 本地文件：--local-file <本地路径>", file=sys.stderr)
        print(f"   - COS 文件：--cos-input-key <COS路径>（如 input/video.mp4）", file=sys.stderr)
        return None

    bucket = os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
    region = os.environ.get("TENCENTCLOUD_COS_REGION", "ap-guangzhou")
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not bucket:
        print("错误：本地文件上传需要配置 TENCENTCLOUD_COS_BUCKET 环境变量", file=sys.stderr)
        return None
    if not secret_id or not secret_key:
        print("错误：请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        return None

    if not _COS_SDK_AVAILABLE:
        print("错误：本地文件上传需要安装 COS SDK：pip install cos-python-sdk-v5", file=sys.stderr)
        return None

    # 自动生成 cos_key
    if not cos_key:
        filename = os.path.basename(local_path)
        cos_key = f"/input/{filename}"

    file_size = os.path.getsize(local_path)
    print(f"📤 检测到本地文件，自动上传到 COS...")
    print(f"   本地文件: {local_path} ({file_size / 1024 / 1024:.2f} MB)")
    print(f"   目标: {bucket}:{cos_key} (region: {region})")

    try:
        cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        cos_client = CosS3Client(cos_config)

        cos_client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_path,
            Key=cos_key,
            PartSize=10,
            MAXThread=5,
            EnableMD5=False
        )

        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"
        presigned_url = None
        try:
            presigned_url = cos_client.get_presigned_url(
                Method="GET", Bucket=bucket, Key=cos_key.lstrip("/"), Expired=3600
            )
        except Exception:
            pass

        result = {
            "Bucket": bucket,
            "Region": region,
            "Key": cos_key,
            "URL": url,
            "PresignedURL": presigned_url,
        }
        print(f"   ✅ 上传成功！COS Key: {cos_key}")
        return result

    except Exception as e:
        print(f"❌ 上传失败: {e}", file=sys.stderr)
        return None


# ─── 任务输出文件提取与自动下载 ───────────────────────────────────────────────

def extract_output_files(task_result):
    """
    从任务结果中提取所有输出文件信息。

    Returns:
        list of dict: [{ "bucket", "region", "key", "signed_url" }, ...]
    """
    if not task_result:
        return []

    outputs = []

    def _try_presign(bucket, region, key):
        if not bucket or not key or not _COS_SDK_AVAILABLE:
            return None
        try:
            cred = _get_credentials()
            cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
            cos_client = CosS3Client(cos_config)
            return cos_client.get_presigned_url(
                Bucket=bucket, Key=key.lstrip("/"), Method="GET", Expired=3600
            )
        except Exception:
            return None

    def _add_cos_output(out_storage, out_path, signed_url=None):
        if not out_path:
            return
        out_type = (out_storage or {}).get("Type", "")
        if out_type == "COS":
            cos_out = (out_storage or {}).get("CosOutputStorage", {}) or {}
            bucket = cos_out.get("Bucket", "")
            region = cos_out.get("Region", "")
            if not signed_url:
                signed_url = _try_presign(bucket, region, out_path)
            outputs.append({
                "bucket": bucket, "region": region,
                "key": out_path, "signed_url": signed_url
            })

    # WorkflowTask（ProcessMedia 提交的视频任务）
    workflow_task = task_result.get("WorkflowTask") or {}
    for item in (workflow_task.get("MediaProcessResultSet") or []):
        task_type = item.get("Type", "")
        key_map = {
            "Transcode": "TranscodeTask", "AnimatedGraphics": "AnimatedGraphicsTask",
            "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
            "SampleSnapshot": "SampleSnapshotTask", "ImageSprites": "ImageSpritesTask",
            "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
            "AudioExtract": "AudioExtractTask",
        }
        task_key = key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None
        if task_detail:
            output = task_detail.get("Output", {}) or {}
            _add_cos_output(output.get("OutputStorage"), output.get("Path", ""))

    # 字幕任务
    for item in (workflow_task.get("SmartSubtitlesTaskResultSet") or []):
        sub_task = item.get("SmartSubtitlesTask") or {}
        output = sub_task.get("Output") or {}
        _add_cos_output(output.get("OutputStorage"), output.get("Path", ""))

    # ImageProcessTaskResultSet（图片任务）
    for item in (task_result.get("ImageProcessTaskResultSet") or []):
        output = item.get("Output") or {}
        out_path = output.get("Path", "")
        signed_url = output.get("SignedUrl", "")
        _add_cos_output(output.get("OutputStorage"), out_path, signed_url or None)

    return outputs


def auto_download_outputs(task_result, download_dir=".", verbose=False):
    """
    任务完成后，自动将所有输出文件下载到本地目录。

    Args:
        task_result:  poll_video_task / poll_image_task 返回的结果 dict
        download_dir: 本地下载目录，默认当前目录
        verbose:      是否输出详细日志

    Returns:
        list of str: 已下载的本地文件路径列表
    """
    outputs = extract_output_files(task_result)
    if not outputs:
        return []

    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not _COS_SDK_AVAILABLE:
        print("⚠️  未安装 COS SDK，跳过自动下载（pip install cos-python-sdk-v5）", file=sys.stderr)
        return []

    os.makedirs(download_dir, exist_ok=True)
    downloaded = []

    print(f"\n📥 自动下载输出文件到: {os.path.abspath(download_dir)}")
    for i, out in enumerate(outputs, 1):
        bucket = out["bucket"]
        region = out["region"]
        key = out["key"]
        filename = os.path.basename(key.lstrip("/"))
        local_path = os.path.join(download_dir, filename)

        # 如果文件名重复，加序号
        if os.path.exists(local_path):
            base, ext = os.path.splitext(filename)
            local_path = os.path.join(download_dir, f"{base}_{i}{ext}")

        print(f"   [{i}] {bucket}:{key} → {local_path}")
        try:
            cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
            cos_client = CosS3Client(cos_config)
            cos_client.download_file(
                Bucket=bucket,
                Key=key.lstrip("/"),
                DestFilePath=local_path
            )
            file_size = os.path.getsize(local_path)
            print(f"       ✅ 下载成功 ({file_size / 1024 / 1024:.2f} MB): {local_path}")
            downloaded.append(local_path)
        except Exception as e:
            print(f"       ❌ 下载失败: {e}", file=sys.stderr)

    if downloaded:
        print(f"\n✅ 共下载 {len(downloaded)} 个文件到 {os.path.abspath(download_dir)}")

    return downloaded


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='腾讯云 MPS 任务轮询工具 - 支持音视频和图片任务',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 轮询音视频任务
  python mps_poll_task.py --task-id 1234567890 --type video

  # 轮询图片任务
  python mps_poll_task.py --task-id 1234567890 --type image

  # 指定区域和轮询参数
  python mps_poll_task.py --task-id 1234567890 --region ap-beijing --interval 5 --max-wait 600

  # 详细输出模式
  python mps_poll_task.py --task-id 1234567890 --verbose

环境变量:
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必需）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必需）
        """.strip()
    )

    parser.add_argument(
        '--task-id',
        required=True,
        help='任务ID（必填）'
    )
    parser.add_argument(
        '--region',
        default='ap-guangzhou',
        help='MPS服务区域（默认: ap-guangzhou）'
    )
    parser.add_argument(
        '--type',
        choices=['video', 'image'],
        default='video',
        help='任务类型: video(音视频) 或 image(图片)（默认: video）'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=None,
        help='轮询间隔秒数（默认: video=10, image=5）'
    )
    parser.add_argument(
        '--max-wait',
        type=int,
        default=None,
        help='最长等待秒数（默认: video=1800, image=300）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='输出详细日志（包含完整API响应）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='模拟执行，显示轮询参数但不实际执行'
    )

    args = parser.parse_args()

    # Dry-run 模式：仅显示操作摘要
    if args.dry_run:
        print("=" * 60)
        print("=== 模拟执行（Dry-run）===")
        print("=" * 60)
        print("操作：轮询任务状态直到完成")
        print(f"\n  TaskId: {args.task_id}")
        print(f"  TaskType: {args.type}")
        print(f"  MPS Region: {args.region}")
        
        # 设置默认值
        interval = args.interval or (10 if args.type == 'video' else 5)
        max_wait = args.max_wait or (1800 if args.type == 'video' else 300)
        
        print(f"  轮询间隔: {interval}秒")
        print(f"  最长等待: {max_wait}秒")
        print("\n不会实际轮询任务。移除 --dry-run 参数后执行实际操作。")
        sys.exit(0)

    # 设置默认值
    interval = args.interval or (10 if args.type == 'video' else 5)
    max_wait = args.max_wait or (1800 if args.type == 'video' else 300)

    # 执行轮询
    if args.type == 'video':
        result = poll_video_task(args.task_id, args.region, interval, max_wait, args.verbose)
    else:
        result = poll_image_task(args.task_id, args.region, interval, max_wait, args.verbose)

    # 根据结果设置退出码
    if result is None:
        sys.exit(1)  # 超时
    elif result.get('Status') == 'FAIL' or (result.get('WorkflowTask', {}).get('ErrCode', 0) != 0):
        sys.exit(2)  # 任务失败
    else:
        sys.exit(0)  # 成功