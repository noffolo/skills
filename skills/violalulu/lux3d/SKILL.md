---
name: lux3d
description: "Use Lux3D to generate 3D models from 2D images. Trigger conditions: when user asks to generate 3D model from image, image to 3D, convert image to 3D object, create 3D from photo, 2D转3D, 图片生成3D模型, or any request involving 2D-to-3D conversion."
---

## What is Lux3D
Lux3D is a multimodal 3D generation model developed by Manycore Technology. It converts 2D images into high-quality 3D PBR models that are perfectly compatible with QIZHEN Engine.

## How to Use

### 1. Get API Key
External users need to fill out a questionnaire to apply for an API key:
- Questionnaire: https://forms.cloud.microsoft.com/r/kRTjdDBV1e
- Or contact: lux3d@qunhemail.com

### 2. Quick Start

```python
from lux3d_client import generate_3d_model

# Set your API key (base64 encoded invitation code)
import os
os.environ["LUX3D_API_KEY"] = "your_invitation_code_here"

# Generate 3D model from image
result = generate_3d_model("path/to/your/image.jpg")
print(f"Model saved to: {result}")
```

### 3. Advanced Usage

```python
from lux3d_client import create_task, query_task_status, download_model

# Step 1: Submit task
task_id = create_task("path/to/image.jpg")
print(f"Task ID: {task_id}")

# Step 2: Poll for result
model_url = query_task_status(task_id)
print(f"Model URL: {model_url}")

# Step 3: Download
download_model(model_url, "output.zip")
```

### 4. Command Line
```bash
python lux3d_client.py input.jpg output.zip
```

### 5. Output Format
The generated model includes:
- White model GLB file
- 9 PBR material channel maps

> ⚠️ **Note**: Model download URL is valid for **2 hours**, please download promptly.

## Requirements
```
pip install Pillow requests
```

## More Information
- GitHub: https://github.com/manycore-research/ComfyUI-Lux3D
- Email: lux3d@qunhemail.com