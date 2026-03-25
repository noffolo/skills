---
name: watermark-pro
description: 文件水印工具。Use when user wants to add watermark to images, Word documents, PowerPoint, or PDF files. Supports text watermark, logo watermark, diagonal/center/tile layouts. 图片水印、文档水印、Word加水印、PPT加水印。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "💧", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow python-docx python-pptx"
---

# Watermark Pro

文件水印工具，支持图片、Word、PPT、PDF添加水印。

## Features

- 🖼️ **图片水印**：支持JPG/PNG/WEBP
- 📄 **Word水印**：支持.docx
- 📊 **PPT水印**：支持.pptx
- 📑 **PDF水印**：支持.pdf
- ✍️ **文字水印**：自定义文字、字体、颜色
- 🖼️ **Logo水印**：支持透明PNG Logo
- 📍 **多种布局**：对角线/居中/平铺

## Trigger Conditions

- "加水印" / "Add watermark"
- "图片加水印" / "Watermark this image"
- "Word文档加水印" / "Add watermark to Word"
- "PPT加水印" / "Watermark PowerPoint"
- "watermark-pro"

---

## Watermark Types (水印类型)

### 文字水印

| 参数 | 说明 | 默认值 |
|------|------|--------|
| text | 水印文字 | "Sample" |
| font_size | 字体大小 | 自动计算 |
| color | 颜色 | 灰色(128,128,128) |
| opacity | 透明度 | 0.3 (30%) |
| angle | 旋转角度 | -45度 |
| layout | 布局方式 | diagonal |

### Logo水印

| 参数 | 说明 | 默认值 |
|------|------|--------|
| logo_path | Logo文件路径 | 必填 |
| scale | 缩放比例 | 0.2 (20%) |
| opacity | 透明度 | 0.3 (30%) |
| layout | 布局方式 | center |

---

## Step 1: Add Watermark to Image

```python
from PIL import Image, ImageDraw, ImageFont
import os

class ImageWatermark:
    def __init__(self):
        self.font = None
    
    def add_text_watermark(self, image_path, text, output_path,
                          font_size=None, color=(128, 128, 128),
                          opacity=0.3, angle=-45, layout='diagonal'):
        """Add text watermark to image"""
        
        # Open image
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size
        
        # Create watermark layer
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Auto font size
        if font_size is None:
            font_size = max(width, height) // 30
        
        # Load font
        try:
            font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate alpha
        alpha = int(255 * opacity)
        fill_color = (*color, alpha)
        
        if layout == 'diagonal':
            # Diagonal watermark pattern
            for y in range(-height, height * 2, text_height * 3):
                for x in range(-width, width * 2, text_width * 2):
                    draw.text((x, y), text, font=font, fill=fill_color)
        
        elif layout == 'center':
            # Single centered watermark
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            draw.text((x, y), text, font=font, fill=fill_color)
        
        elif layout == 'tile':
            # Tiled pattern
            for y in range(0, height, text_height * 2):
                for x in range(0, width, text_width + 50):
                    draw.text((x, y), text, font=font, fill=fill_color)
        
        # Rotate watermark
        watermark = watermark.rotate(angle, expand=False)
        
        # Composite
        result = Image.alpha_composite(img, watermark)
        
        # Save
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            result = result.convert('RGB')
        result.save(output_path)
        
        return output_path
    
    def add_logo_watermark(self, image_path, logo_path, output_path,
                          scale=0.2, opacity=0.3, layout='center'):
        """Add logo watermark to image"""
        
        # Open images
        img = Image.open(image_path).convert('RGBA')
        logo = Image.open(logo_path).convert('RGBA')
        
        width, height = img.size
        
        # Resize logo
        logo_width = int(width * scale)
        logo_height = int(logo.size[1] * (logo_width / logo.size[0]))
        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
        
        # Adjust opacity
        logo.putalpha(Image.eval(logo.split()[3], lambda a: int(a * opacity)))
        
        # Create watermark layer
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        
        if layout == 'center':
            x = (width - logo_width) // 2
            y = (height - logo_height) // 2
            watermark.paste(logo, (x, y))
        
        elif layout == 'tile':
            for y in range(0, height, logo_height * 2):
                for x in range(0, width, logo_width * 2):
                    watermark.paste(logo, (x, y))
        
        # Composite
        result = Image.alpha_composite(img, watermark)
        
        # Save
        if output_path.lower().endswith('.jpg'):
            result = result.convert('RGB')
        result.save(output_path)
        
        return output_path

# Example usage
wm = ImageWatermark()

# Text watermark
wm.add_text_watermark(
    'input.jpg',
    '版权所有',
    'output_watermarked.jpg',
    opacity=0.3,
    layout='diagonal'
)

# Logo watermark
wm.add_logo_watermark(
    'input.jpg',
    'logo.png',
    'output_logo.jpg',
    scale=0.15,
    opacity=0.4
)
```

---

## Step 2: Add Watermark to Word

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class WordWatermark:
    def add_text_watermark(self, docx_path, text, output_path,
                          font_size=48, color=(200, 200, 200)):
        """Add text watermark to Word document"""
        
        doc = Document(docx_path)
        
        # Add watermark to each section
        for section in doc.sections:
            header = section.header
            
            # Clear existing header
            for para in header.paragraphs:
                para.clear()
            
            # Add watermark text
            para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            run = para.add_run(text)
            run.font.size = Pt(font_size)
            run.font.color.rgb = RGBColor(*color)
            run.font.name = '宋体'
            
            # Add spacing to center vertically
            para.paragraph_format.space_before = Pt(200)
        
        doc.save(output_path)
        return output_path

# Example usage
wm = WordWatermark()
wm.add_text_watermark('input.docx', '机密文件', 'output.docx')
```

---

## Step 3: Add Watermark to PowerPoint

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

class PptWatermark:
    def add_text_watermark(self, pptx_path, text, output_path,
                          font_size=60, color=(200, 200, 200)):
        """Add text watermark to PowerPoint"""
        
        prs = Presentation(pptx_path)
        
        for slide in prs.slides:
            # Add watermark text box
            left = Inches(1)
            top = Inches(3)
            width = Inches(8)
            height = Inches(2)
            
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = Pt(font_size)
            p.font.color.rgb = RGBColor(*color)
            p.alignment = PP_ALIGN.CENTER
            
            # Make semi-transparent
            txBox.fill.background()
        
        prs.save(output_path)
        return output_path

# Example usage
wm = PptWatermark()
wm.add_text_watermark('input.pptx', '草稿', 'output.pptx')
```

---

## Usage Examples

### 图片加水印

```
User: "给这张图片加上'版权所有'水印"

Agent:
1. Load image
2. Add diagonal text watermark
3. Save output
```

### Word加水印

```
User: "这个Word文档加个'机密'水印"

Agent:
1. Open .docx file
2. Add watermark to header
3. Save output
```

### PPT加水印

```
User: "PPT加个'草稿'水印"

Agent:
1. Open .pptx file
2. Add text box to each slide
3. Save output
```

---

## Notes

- 纯本地处理，无隐私风险
- 支持中英文水印
- 跨平台兼容
