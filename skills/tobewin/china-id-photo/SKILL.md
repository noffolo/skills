---
name: china-id-photo
description: 生成中国标准证件照。Use when the user needs to create an ID photo, passport photo, visa photo, or any standard photo with specific size and background color. Supports 1-inch, 2-inch, passport, and custom sizes with white/blue/red backgrounds. Outputs JPEG or PNG.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📷", "requires": {"bins": ["python3"]}, "primaryEnv": ""}}
---

# 中国证件照生成 China ID Photo

将个人照片转换为符合中国标准的证件照，支持多种尺寸和背景颜色。

## 功能特点

- 🎨 支持白/蓝/红三种标准背景色
- 📐 支持1寸、2寸、护照等标准尺寸
- 🖼️ 输出JPEG（默认）或PNG格式
- 🔒 完全本地处理，不上传任何服务器

## 触发时机

- "帮我做一张证件照"
- "把这张照片转成1寸证件照"
- "我需要蓝色背景的2寸照片"
- "生成护照照片，白色背景"
- "这张照片转成证件照，要红色背景"
- "帮我制作身份证照片"

---

## Step 0：环境检查与依赖安装

```bash
# 检查 python3
if ! command -v python3 &> /dev/null; then
  echo "❌ 需要 python3"
  echo "  macOS:  brew install python3"
  echo "  Ubuntu: sudo apt install python3"
  echo "  Windows: 从 python.org 下载安装"
  exit 1
fi

# 检查并安装依赖
echo "📦 检查依赖..."
pip install rembg pillow -q 2>/dev/null || {
  echo "❌ 依赖安装失败，请手动执行："
  echo "  pip install rembg pillow"
  exit 1
}

echo "✅ 环境检查通过"
```

---

## Step 1：识别用户需求

```
用户提供照片路径 → 识别参数：

尺寸（用户指定或默认1寸）：
  "1寸" / "一寸" / "小一寸"     → 295×413 像素
  "2寸" / "二寸"                → 413×579 像素
  "小二寸" / "护照" / "passport" → 390×567 像素
  "大一寸" / "签证" / "visa"     → 390×567 像素
  "身份证" / "id card"          → 358×441 像素
  未指定                        → 默认1寸（295×413）

背景色（用户指定或默认白色）：
  "白色" / "白底" / "white"     → #FFFFFF
  "蓝色" / "蓝底" / "blue"      → #438EDB（标准证件照蓝）
  "红色" / "红底" / "red"       → #FF0000
  未指定                        → 默认白色

输出格式：
  "PNG" / "png" / "透明"        → PNG格式
  未指定                        → 默认JPEG格式
```

---

## Step 2：生成证件照

```bash
INPUT_IMAGE="/path/to/user/photo.jpg"  # 用户提供的照片路径
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/id_photo_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 参数设置
SIZE="1"           # 尺寸：1/2/passport/id_card/custom
BG_COLOR="white"   # 背景色：white/blue/red
OUTPUT_FORMAT="jpg" # 输出格式：jpg/png

python3 << 'PYEOF'
import sys
import os
from rembg import remove
from PIL import Image
import io

# 配置参数
input_path = os.environ.get('INPUT_IMAGE', '')
output_dir = os.environ.get('OUTPUT_DIR', '')
size_type = os.environ.get('SIZE', '1')
bg_color_name = os.environ.get('BG_COLOR', 'white')
output_format = os.environ.get('OUTPUT_FORMAT', 'jpg')

# 标准尺寸映射（像素，300DPI）
SIZES = {
    '1': (295, 413),        # 1寸
    '2': (413, 579),        # 2寸
    'passport': (390, 567), # 护照/小二寸
    'id_card': (358, 441),  # 身份证
}

# 背景色映射
BG_COLORS = {
    'white': (255, 255, 255),
    'blue': (67, 142, 219),   # #438EDB 标准证件照蓝
    'red': (255, 0, 0),
}

def center_crop(img, target_size):
    """居中裁剪到目标尺寸"""
    target_w, target_h = target_size
    img_w, img_h = img.size
    target_ratio = target_w / target_h
    img_ratio = img_w / img_h

    if img_ratio > target_ratio:
        # 图片太宽，裁剪宽度
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, img_h))
    else:
        # 图片太高，裁剪高度
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        img = img.crop((0, top, img_w, top + new_h))

    return img.resize(target_size, Image.LANCZOS)

def detect_subject_bbox(img):
    """检测主体边界框（基于alpha通道）"""
    if img.mode != 'RGBA':
        return None
    
    # 获取alpha通道
    alpha = img.split()[3]
    bbox = alpha.getbbox()
    return bbox

def process_image(input_path, output_dir, size_type, bg_color_name, output_format):
    print(f"📸 正在处理图片...")
    
    # 读取原图
    input_img = Image.open(input_path).convert('RGB')
    print(f"   原图尺寸: {input_img.size}")
    
    # 抠图（移除背景）
    print("✂️ 正在抠图...")
    output_img = remove(input_img)
    
    # 检测主体位置
    bbox = detect_subject_bbox(output_img)
    if bbox:
        print(f"   检测到主体区域: {bbox}")
    
    # 获取目标尺寸
    if size_type in SIZES:
        target_size = SIZES[size_type]
        size_name = {'1': '1寸', '2': '2寸', 'passport': '护照', 'id_card': '身份证'}[size_type]
    else:
        target_size = (295, 413)
        size_name = '1寸（默认）'
    
    print(f"📐 目标尺寸: {size_name} {target_size}")
    
    # 获取背景色
    bg_color = BG_COLORS.get(bg_color_name, BG_COLORS['white'])
    print(f"🎨 背景色: {bg_color_name} {bg_color}")
    
    # 创建背景并合成
    bg = Image.new('RGB', output_img.size, bg_color)
    bg.paste(output_img, mask=output_img.split()[3])
    
    # 居中裁剪到目标尺寸
    result = center_crop(bg, target_size)
    
    # 保存
    output_ext = 'png' if output_format == 'png' else 'jpg'
    output_path = os.path.join(output_dir, f'id_photo_{size_type}_{bg_color_name}.{output_ext}')
    
    if output_ext == 'png':
        result.save(output_path, 'PNG')
    else:
        result.save(output_path, 'JPEG', quality=95)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ 证件照已生成: {output_path}")
    print(f"   文件大小: {file_size / 1024:.1f} KB")
    
    return output_path

try:
    result = process_image(input_path, output_dir, size_type, bg_color_name, output_format)
    print("\n🎉 处理完成！")
except Exception as e:
    print(f"\n❌ 处理失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF
```

### 设置环境变量并执行

```bash
export INPUT_IMAGE="/path/to/user/photo.jpg"
export OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/id_photo_$(date +%Y%m%d_%H%M%S)"
export SIZE="1"          # 1/2/passport/id_card
export BG_COLOR="white"  # white/blue/red
export OUTPUT_FORMAT="jpg"  # jpg/png

# 执行上面的python脚本
```

---

## Step 3：输出结果

证件照生成完成后：

```
✅ 证件照已生成！

📐 尺寸：1寸（295×413像素，2.5×3.5厘米）
🎨 背景：白色
📁 格式：JPEG
📍 位置：/path/to/id_photo_xxx/id_photo_1_white.jpg

可直接用于：
- 简历、报名表
- 各类证件申请
- 在线提交
```

---

## 常用尺寸速查

| 名称 | 像素 | 厘米 | 常用场景 |
|------|------|------|----------|
| 1寸 | 295×413 | 2.5×3.5 | 简历、报名表 |
| 2寸 | 413×579 | 3.5×5.0 | 毕业证、资格证 |
| 护照/小二寸 | 390×567 | 3.3×4.8 | 护照、签证 |
| 身份证 | 358×441 | 2.6×3.2 | 身份证办理 |

---

## 错误处理

```
文件不存在           → 提示用户确认照片路径
格式不支持           → 提示支持的格式：JPG, PNG, WEBP
依赖安装失败         → 提示手动安装：pip install rembg pillow
内存不足             → 建议压缩原图后再试
抠图效果不佳         → 建议使用背景简洁的正面照
```

---

## 注意事项

- 首次运行需下载rembg模型（约170MB），请保持网络连接
- 建议使用正面免冠照片，背景简洁效果更佳
- 原图分辨率建议 >= 500×500 像素
- 处理时间约2-10秒（取决于CPU性能）
- 所有处理完全在本地进行，不会上传任何数据
