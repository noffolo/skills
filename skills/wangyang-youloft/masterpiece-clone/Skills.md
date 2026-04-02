# Skills.md

## Skill Name
masterpiece-clone

---

## Description
**MasterPiece Clone** — A professional visual language expert and image-to-image workflow. It decomposes high-end editorial photography into refined descriptive prompts and clones visual styles with high precision.

It leverages the **Pixify** engine to process your inputs through:
- **Prompt Analysis** (image_to_text_gpt5)
- **MasterPiece Generation** (nano_banana_pro)

---

## Service Overview

- 🌐 **Product Website / Console**:  
  https://ai.ngmob.com  
  *(For product access, workflow management, and obtaining your API Key)*

- 🔗 **API Base URL**:  
  https://api.ngmob.com  
  *(Used strictly for API requests and workflow execution)*

---

## Use Cases

- **MasterPiece Cloning**: Replicate the lighting, composition, and texture of a target image.
- **Visual Language Extraction**: Automatically generate clean, descriptive prompts for AI image-to-image workflows.
- **Editorial Transformation**: Convert standard portraits into high-end, cinematic editorial content.
- **Privacy-Safe Tagging**: Analyze subject features without capturing sensitive identity data (gender, age, specific facial features).

---

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| Image Input | string (URL) | ✅ | Reference image for style/content decomposition |
| Image Input 1 | string (URL) | ✅ | Target subject or secondary reference image |
| Text Input | string | ✅ | Task instructions for the visual language expert |

---

## How to Use

When the user requests to execute this workflow, follow these steps:

### 1. Collect Input Parameters

Gather the required inputs from the user according to the table above.

### 2. Call the Workflow API

```bash
echo '{
  "inputs": {
    "Image Input": "https://example.com/adopted_20260324081228_0.png",
    "Image Input 1": "https://example.com/20251219_200547_ivy_runway_fullbody.png",
    "Text Input": "你是一位视觉语言专家。请将输入的【摄影大片】拆解为一段高度精炼、纯描述性的英文短段落..."
  }
}' | curl -X POST https://api.ngmob.com/api/v1/workflows/Awtk0EnhqBGkoOExvseI/run \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @-
```

### 3. Poll Task Status (Recommended: every 3–5 seconds)

Use the returned `task_id` to query task status:

```bash
curl https://api.ngmob.com/api/v1/workflows/executions/{task_id} \
  -H "Authorization: Bearer $API_KEY"
```

---

## Preview

| Input 1 (Reference) | Input 2 (Subject) | Result (MasterPiece) |
| :---: | :---: | :---: |
| ![Reference](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/adopted_20260324081228_0_compressed.png) | ![Subject](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/20251219_200547_ivy_runway_fullbody_916_dramatic_013_compressed450.png) | ![Result](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/generated-kM43NBVXDjluTGUiozmE-0_compressed.png) |

---

### Example (Recommended)

```json
{
  "Image Input": "https://example.com/adopted_20260324081228_0.png",
  "Image Input 1": "https://example.com/20251219_200547_ivy_runway_fullbody_916_dramatic_013.png",
  "Text Input": "任务指令：
你是一位视觉语言专家。请将输入的【摄影大片】拆解为一段高度精炼、纯描述性的英文短段落，用于闭源 AI 图生图工作流。

核心规则（严禁违反）：

人物特征真空化： 严禁描述发色、发型、肤色、面部特征、年龄或性别。请统一使用 "The person" 或 "The subject" 代称。

拒绝列表与参数： 严禁输出 "Negative prompt"、"Parameters"、"Optional tags" 或任何技术参数（如 ISO, f/1.8）。

拒绝引言： 禁止任何开场白，直接输出提示词正文。

空间与风格： 重点描述：构图（景别）、光影特效（如色散/虹彩）、服装材质、背景细节。

输出示例（仅参考结构）：
A high-end editorial portrait, medium shot. The subject is wearing a [服装]. Vivid [光影描述] streaks across the frame. The background features [背景]. Cinematic lighting with [色彩倾向].

请开始对附件图进行拆解："
}
```

---

🤖 Generated with [Pixify](https://ai.ngmob.com)
