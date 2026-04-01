---
name: image-editor
description: "Professional image post-processing tool. Supports multiple editing styles (apocalyptic cinematic, Japanese fresh, vintage film, etc.), auto-detects and installs ImageMagick, supports RAW/JPG/PNG formats, batch processing, and custom preset creation. Use when: (1) user needs photo editing/color grading/filters, (2) processing RAW format photos, (3) batch processing images, (4) creating custom editing presets"
---

# Professional Image Post-Processing Tool

## Features

- ✅ Auto-detect and install ImageMagick
- ✅ Multiple editing style presets
- ✅ Support for RAW/JPG/PNG/TIFF formats
- ✅ Batch processing support
- ✅ Custom preset saving
- ✅ Isolated intermediate file management

## Editing Style Presets

| Style | Characteristics | Use Cases |
|-------|-----------------|-----------|
| `apocalyptic` | Low saturation, teal-orange tones, vignette, grain | Post-apocalyptic, sci-fi, cinematic |
| `japanese` | High brightness, low contrast, cyan-green tint | Japanese fresh style, daily records |
| `vintage` | Warm tones, faded look, soft focus | Retro, nostalgic |
| `bw-high` | Black & white, high contrast | Documentary, artistic |
| `custom` | User-defined parameters | Personalized needs |

## Usage

### Single Image Processing

```python
from scripts.editor import ImageEditor

editor = ImageEditor()
result = editor.process(
    input_path="photo.dng",
    style="apocalyptic",
    output_name="my_photo"
)
```

### Batch Processing

```python
editor.batch_process(
    input_dir="./photos",
    style="japanese",
    output_dir="./output"
)
```

### Custom Presets

```python
# Create custom preset
editor.create_preset(
    name="my_style",
    params={
        "brightness_contrast": "-10x30",
        "modulate": "100,70",
        "tint": "#3a5a4a",
        "gamma": 0.95,
        "sharpen": "0x1.2",
        "noise": 0.3,
        "vignette": True
    }
)
```

## Workflow (Iterative Step-by-Step Editing)

### Core Principles

- Must use iterative step-by-step editing to ensure each step meets quality standards before proceeding, ultimately generating the final image from the original without compression loss.
- Do not increase contrast unless the style specifically calls for high contrast.
- Unless style dictates otherwise, preserve smooth tonal transitions and retain highlight and shadow details.
- When reviewing intermediate and final images with multimodal models, watch for artifacts like color banding, noise, or color patches caused by excessive parameter adjustments.

### Detailed Steps

#### 1. Initialization
- Detect ImageMagick, prompt for installation if not found
- Analyze original image (resolution, format, color space)
- **Create isolated working directory based on original filename** (to avoid file conflicts between different images; append -001, -002... for duplicates):
  ```
  workspace/image-editor-work/
  ├── {filename}/         # Directory named after original file
  │   ├── temp/           # Intermediate processing files
  │   │   ├── step01.jpg
  │   │   ├── step02.jpg
  │   │   └── params/     # Successful parameter records per step
  │   │       ├── step01_params.txt
  │   │       ├── step02_params.txt
  │   │       └── ...
  │   └── final/          # Final output
  │       └── xxx_final.jpg
  ├── {filename2}/        # Separate directory for another image
  └── ...
  ```
- **Example**: When processing `IMG_20260329_111232.dng`, create `image-editor-work/IMG_20260329_111232/` directory

#### 2. Iterative Step-by-Step Editing (Key Process)

**Core Principle: Preserve original dynamic range and bit depth**

For all images (whether RAW or other formats), **each step must start from the original file**, stacking previously verified parameters to avoid dynamic range and bit depth loss from intermediate JPGs.

**Step A - Generate Intermediate JPG (For validation only, not part of editing chain)**

**Core Principle: Always start from original file**

Each processing step **starts from the original file**, carrying all previously verified parameters + new parameters for the current step, generating an intermediate JPG for multimodal validation only.

- Command format examples:
  ```bash
  # Step 1: Start from original
  magick original.dng -brightness-contrast -5x20 -quality 100 step01.jpg
  
  # Step 2: Still from original, stack Step 1 params + new params
  magick original.dng -brightness-contrast -5x20 -modulate 110,80 -quality 100 step02.jpg
  
  # Step 3: Continue from original, stack Step 1+2 params + new params
  magick original.dng -brightness-contrast -5x20 -modulate 110,80 -fill "#3a5a6a" -tint 15 -quality 100 step03.jpg
  ```

- **JPG quality must be highest**: `-quality 100`
- **Strictly prohibited: `-resize` or `-crop`**: Do not change original resolution unless user explicitly requests
- **Note**: ImageMagick 7+ uses `magick` command, no need for `magick convert`

**Important**: Intermediate JPGs are for multimodal model validation only, **never used as input for next step**.

**Step B - Multimodal Validation**
- Use multimodal model to review generated intermediate JPG
- Determine if editing goal for this step is achieved
- **If goal NOT achieved**:
  - Analyze cause, adjust magick parameters
  - **Restart from original file** with all previously verified params + adjusted new params
  - **Repeat this step until达标 (standard met)**
- **If goal achieved**:
  - Write the **new** magick parameters for this step to `temp/params/stepXX_params.txt`
  - **Continue from original file** for next step with all verified params (including just recorded)

**Key Memory**:
- Each step re-reads original file
- Parameters accumulate: Step N = original + param1 + param2 + ... + paramN
- Intermediate JPGs are view-only, next step still starts from original

#### 3. Loop Execution
- Repeat "Step A → Step B" process for next editing step
- Record parameters to corresponding `stepXX_params.txt` after each step达标
- Continue until all editing steps complete

#### 4. Generate Final Image (Critical Step)

**Strictly prohibited: Use last intermediate JPG as final output**.

Correct approach:
1. Read original image
2. Read each step's parameter file `stepXX_params.txt` in sequence
3. **Build complete magick command chain**, concatenating all parameters in editing order
4. Generate final image from original in one pass:
   ```bash
   magick original.dng \
     -brightness-contrast -5x20 \
     -modulate 110,65 -fill "#2a5a6a" -tint 20 -gamma 0.95 \
     -size 4096x3072 radial-gradient:black-white -compose multiply -composite \
     -sharpen 0x1.5 \
     -attenuate 0.5 +noise gaussian \
     -quality 100 final_xxx.jpg
   ```

**Why do this?**
- Intermediate JPGs suffer JPEG compression loss from multiple saves
- Applying all parameters from original in one pass avoids layer-by-layer compression
- Final image has highest quality

#### 5. Wrap-up & Delivery

**File Saving:**
- Copy final image to `final/` directory
- Optional: Clean up intermediate files or keep for review
- Record processing log

**Deliver to User:**

1. **Final file path** (must provide)
   ```
   Editing complete! Final image saved to: {final_path}
   ```
2. Send image to user

**Important**: Regardless of `open_result_view` success, always explicitly inform user of local file path to ensure they can find the final product.

### Workflow Diagram

**Unified Processing Flow (all formats):**
```
Original
   │
   ├──► Step 1 params ──► Generate intermediate JPG ──► [Multimodal check] ──► Standard met?
   │                                                                         │
   │                                                                        No ──► Adjust params ──► Regenerate from original
   │                                                                         │
   │                                                                       Yes ──► Record params to step01_params.txt
   │
   ├──► Step 1+2 params ──► Generate intermediate JPG ──► [Multimodal check] ──► Standard met?
   │                                                                           │
   │                                                                          No ──► Adjust params ──► Regenerate from original
   │                                                                           │
   │                                                                         Yes ──► Record params to step02_params.txt
   │
   ├──► Step 1+2+3 params ──► Generate intermediate JPG ──► [Multimodal check] ──► Standard met?
   │                                                                             │
   │                                                                            ...
   ▼
[Final Generation] ──► Apply all params from original in one pass ──► Final image (highest quality)
```

**Key Points:**
- Each step starts from **original file**
- Parameters accumulate: Step N = original + param1 + param2 + ... + paramN
- Intermediate JPGs **for validation only**, never participate in next step processing

## Directory Structure

```
workspace/
└── image-editor-work/
    ├── {filename1}/        # Independent working directory for image 1
    │   ├── temp/
    │   │   ├── step01.jpg
    │   │   ├── step02.jpg
    │   │   └── params/
    │   │       ├── step01_params.txt
    │   │       └── step02_params.txt
    │   └── final/
    │       └── {filename1}_final.jpg
    ├── {filename2}/        # Independent working directory for image 2
    │   ├── temp/
    │   │   ├── step01.jpg
    │   │   └── params/
    │   │       └── step01_params.txt
    │   └── final/
    │       └── {filename2}_final.jpg
    └── ...
```

**Naming Conventions:**
- Working directory name: `{original filename (without extension)}`
- Intermediate files: `step{NN}.jpg`
- Parameter files: `step{NN}_params.txt`
- Final files: `{original filename}_final.jpg`

## Notes

- Processing RAW format requires ImageMagick with RAW decoding support
- High-resolution images take longer to process
- Recommend processing preview images first to confirm effects

## Editing Step Quality Standards (Agent Guidelines)

### Multimodal Check Points

When reviewing intermediate JPGs, watch for:

| Step Type | Check Points | Standard Met |
|-----------|--------------|--------------|
| **Contrast Adjustment** | Highlight/shadow details, overall clarity | Shadow details present, highlights not blown, image has depth |
| **Color Toning** | Color temperature, saturation, color cast | Matches target style (e.g., teal-orange has cyan-blue shadows + warm yellow highlights) |
| **Vignette** | Corner darkening degree, transition smoothness | Corners noticeably darker, edge-to-center transition smooth, not jarring |
| **Sharpening** | Edge clarity, noise control | Subject edges clear, no obvious aliasing or noise increase |
| **Grain** | Grain uniformity, natural feel | Film texture natural, doesn't destroy details, grain evenly distributed |
| **Destructive Editing** | Color banding, noise, color patches from excessive parameters | Natural color transitions, no banding, no noise beyond added grain, no artifacts |

### Parameter Adjustment Strategy

- **Insufficient effect**: Increase parameter intensity (e.g., contrast from 15 to 25)
- **Excessive effect**: Decrease parameter intensity (e.g., vignette from 80% to 60%)
- **Color cast**: Adjust hue or change tint fill color
- **Local issues**: Consider if regional processing is needed

### Important Reminders

1. **Quality first**: All intermediate JPGs must use `-quality 100`
2. **Preserve original**: Strictly prohibited from overwriting or modifying original images
3. **Parameter recording**: Write to parameter file **immediately** after step达标 to prevent loss
4. **Always start from original**: Each step starts from original file, stacking all previously verified params
5. **Intermediate JPGs for validation only**: Never use intermediate JPGs as input for next step
6. **Final generation**: Apply all parameters from original in one pass to generate final image