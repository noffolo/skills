# AI Image Generator

基于 AI Artist API 的图片与视频生成工具，支持异步任务处理和多种生成模型。

## 🚀 快速开始

### 1. 获取 API Key

访问 [https://staging.kocgo.vip/index](https://staging.kocgo.vip/index) 注册并登录，然后在控制台创建你的 API Key。

### 2. 设置 API Key

```bash
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

### 3. 验证配置

```bash
python3 scripts/test_config.py
```

### 4. 生成图片

```bash
python3 scripts/generate_image.py "一只可爱的猫"
```

## 📖 完整文档

详细使用说明请查看 [SKILL.md](SKILL.md)

## ⚠️ 重要提示

- **必须设置自己的 API Key** - 不要使用默认的 Key
- 首次使用前请运行 `test_config.py` 验证配置
- 支持图片和视频生成，详见文档

## 🎨 支持的模型

### 图片模型
- **SEEDREAM5_0** - 高质量图片生成（默认）
- **NANO_BANANA_2** - 轻量快速生成

### 视频模型
- **SEEDANCE_1_5_PRO** - 文生视频，支持音频
- **SORA2** - 图生视频，支持首尾帧控制

## 📝 使用示例

```bash
# 生成图片
python3 scripts/generate_image.py "风景画"

# 使用特定模型
python3 scripts/generate_image.py "一只狗" --model NANO_BANANA_2

# 生成视频
python3 scripts/generate_image.py "海边日落" --model SEEDANCE_1_5_PRO

# 下载图片到本地
python3 scripts/generate_image.py "猫咪" --download
```

## 🔧 环境要求

- Python 3.6+
- requests 库

## 📄 许可证

请遵守 AI Artist API 的使用条款。
