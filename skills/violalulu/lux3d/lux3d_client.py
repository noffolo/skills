"""
Lux3D Client - Generate 3D models from 2D images
"""

import base64
import hashlib
import time
import requests
from PIL import Image
import io
import os

# Configuration
API_KEY = os.environ.get("LUX3D_API_KEY", "your_lux3d_api_key")
BASE_URL = "https://api.luxreal.ai"


def parse_invitation_code(code):
    """Parse base64 encoded invitation code to get ak/sk/appuid (format: version:ak:sk:appuid)"""
    decoded = base64.b64decode(code).decode('utf-8')
    parts = decoded.split(':')
    if len(parts) != 4:
        raise ValueError(f"Invalid invitation code format: expected 4 parts, got {len(parts)}")
    return {'version': parts[0], 'ak': parts[1], 'sk': parts[2], 'appuid': parts[3]}


def generate_sign(ak, sk, appuid):
    """Generate MD5 signature"""
    timestamp = str(int(time.time() * 1000))
    sign_string = sk + ak + appuid + timestamp
    sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
    return {'appkey': ak, 'appuid': appuid, 'timestamp': timestamp, 'sign': sign}


def image_to_base64(image_path):
    """Convert image file to base64"""
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_str}"


def create_task(image_path):
    """Submit image-to-3D task
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        str: Task ID
        
    Raises:
        Exception: If request fails or API returns error
    """
    # Parse API key
    code = parse_invitation_code(API_KEY)
    sign = generate_sign(code['ak'], code['sk'], code['appuid'])
    
    # Convert image to base64
    base64_image = image_to_base64(image_path)
    
    # Submit task
    url = f"{BASE_URL}/global/lux3d/generate/task/create?appuid={sign['appuid']}&appkey={sign['appkey']}&sign={sign['sign']}&timestamp={sign['timestamp']}"
    
    headers = {"Content-Type": "application/json"}
    payload = {"img": base64_image}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    
    try:
        result = response.json()
    except ValueError:
        raise Exception(f"Invalid JSON response: {response.text}")
    
    # Error code handling
    if result.get("code") != 0:
        err_msg = result.get("message", "unknown error")
        raise Exception(f"API error: {err_msg}")
    
    task_id = result.get("d")
    if not task_id:
        raise Exception(f"failed to get task_id, response: {result}")
    
    return task_id


def query_task_status(task_id, max_attempts=60, interval=15):
    """Query task status and get result
    
    Args:
        task_id: Task ID returned from create_task
        max_attempts: Maximum number of polling attempts (default: 60)
        interval: Interval between attempts in seconds (default: 15)
        
    Returns:
        str: URL to download the generated 3D model
        
    Raises:
        Exception: If task fails or timeout
    """
    code = parse_invitation_code(API_KEY)
    sign = generate_sign(code['ak'], code['sk'], code['appuid'])
    
    url = f"{BASE_URL}/global/lux3d/generate/task/get?busid={task_id}&appuid={sign['appuid']}&appkey={sign['appkey']}&sign={sign['sign']}&timestamp={sign['timestamp']}"
    
    for attempt in range(max_attempts):
        response = requests.get(url, headers={"Content-Type": "application/json"})
        try:
            result = response.json()
        except ValueError:
            raise Exception(f"Invalid JSON response: {response.text}")
        status = result.get("d", {}).get("status")
        
        if status == 3:  # Completed
            outputs = result.get("d", {}).get("outputs", [])
            if outputs:
                return outputs[0].get("content")  # GLB model URL
        elif status == 4:  # Failed
            raise Exception("Task execution failed")
        else:
            time.sleep(interval)
    
    raise Exception("Task timeout")


def download_model(model_url, output_path):
    """Download generated model
    
    Args:
        model_url: URL from query_task_status
        output_path: Local path to save the model
        
    Returns:
        int: Number of bytes downloaded
    """
    response = requests.get(model_url)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    return len(response.content)


def generate_3d_model(image_path, output_path=None):
    """Complete workflow: submit task, wait, and download
    
    Args:
        image_path: Path to input image
        output_path: Path to save output (optional, auto-generated from input)
        
    Returns:
        str: Path to downloaded model
    """
    # Step 1: Submit task
    print("=== Submitting task ===")
    task_id = create_task(image_path)
    print(f"Task ID: {task_id}")
    
    # Step 2: Query result (wait for completion)
    print("\n=== Querying result ===")
    model_url = query_task_status(task_id)
    print(f"Generated 3D model URL: {model_url}")
    
    # Step 3: Download model
    if output_path is None:
        output_name = image_path.rsplit('.', 1)[0] + '_3d.zip'
    else:
        output_name = output_path
    
    print(f"\n=== Downloading model ===")
    size = download_model(model_url, output_name)
    print(f"Downloaded: {output_name} ({size} bytes)")
    
    return output_name


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lux3d_client.py <image_path> [output_path]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = generate_3d_model(image_path, output_path)
        print(f"\n✅ Success! Model saved to: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)