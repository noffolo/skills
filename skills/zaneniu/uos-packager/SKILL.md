# UOS/deepin 应用打包规范

UOS/deepin 应用基于统信打包规范，使用 deb 格式，所有应用文件必须安装到 `/opt/apps/${appid}/` 目录下。

## 核心规则

### 1. 应用标识（appid）

必须使用**倒置域名**规则，支持小写字母和点号。

```
org.deepin.browser
com.example.myapp
org.mysuite.editor
```

### 2. 目录结构

```
${appid}/
├── entries/          # 资源映射到系统目录
│   ├── applications/ # desktop 文件 → /usr/share/applications
│   ├── icons/        # 图标文件 → /usr/share/icons
│   ├── doc/          # 文档 → /usr/share/doc（商店版本≥7.6.2）
│   ├── fonts/files/  # 字体 → /usr/share/fonts
│   ├── help/         # 帮助手册 → /usr/share/help
│   ├── locale/       # 翻译文件 → /usr/share/locale
│   └── mime/         # MIME 数据库 → /usr/share/mime
├── files/            # 应用文件（无限制，建议 bin/ 子目录放可执行文件）
│   └── bin/
└── info             # 应用描述文件（JSON）
```

### 3. info 文件（必需）

```json
{
    "appid": "org.deepin.browser",
    "name": "浏览器",
    "version": "1.1.2",
    "arch": ["amd64", "arm64"],
    "permissions": {
        "autostart": false,
        "notification": false,
        "trayicon": false,
        "clipboard": false,
        "account": false,
        "bluetooth": false,
        "camera": false,
        "audio_record": false,
        "installed_apps": false
    },
    "support-plugins": [],
    "plugins": []
}
```

**字段说明：**

| 字段 | 说明 | 要求 |
|------|------|------|
| appid | 应用唯一标识 | 必填，倒置域名 |
| name | 应用默认名称 | 必填 |
| version | 版本号 | 必填，格式 `{MAJOR}.{MINOR}.{PATCH}.{BUILD}`，纯数字 |
| arch | 支持的架构 | 必填，支持：amd64, arm64, loongarch64, mips64el, sw_64 |
| permissions | 沙箱权限 | 布尔值，默认 false |

### 4. Desktop Entry 文件

路径：`entries/applications/${appid}.desktop`
编码：**必须 UTF-8**（其他编码会导致中文乱码）

```ini
[Desktop Entry]
Categories=Network;WebBrowser;
Name=Browser
Name[zh_CN]=浏览器
Keywords=deepin;uniontech;browser
Keywords[zh_CN]=深度;统信;浏览器
Comment=Access the Internet.
Comment[zh_CN]=访问互联网。
Exec=/opt/apps/org.deepin.browser/files/bin/your_app
Icon=org.deepin.browser
Type=Application
Terminal=false
StartupWMClass=org.deepin.browser
StartupNotify=true
MimeType=audio/aac;application/aac;
```

**必填字段：** `[Desktop Entry]`、`Name`、`Exec`、`Icon`、`Type`、`Terminal`、`StartupNotify`

**Categories 可选值：**

| 值 | 启动器分类 |
|---|-----------|
| Network | 网络应用 |
| Chat | 社交沟通 |
| Audio | 音乐欣赏 |
| AudioVideo | 视频播放 |
| Graphics | 图形图像 |
| Game | 游戏娱乐 |
| Office | 办公学习 |
| Reading | 阅读翻译 |
| Development | 编程开发 |
| System | 系统管理 |

### 5. 图标

矢量格式（推荐 SVG）：
```
entries/icons/hicolor/scalable/apps/${appid}.svg
```

非矢量格式（PNG，分辨率 16/24/32/48/128/256/512）：
```
entries/icons/hicolor/24x24/apps/${appid}.png
entries/icons/hicolor/48x48/apps/${appid}.png
entries/icons/hicolor/128x128/apps/${appid}.png
```

### 6. 文件系统权限

- **系统目录**：只读，不依赖其内容
- **应用数据目录**：使用 XDG 环境变量

| 环境变量 | 路径 |
|----------|------|
| `$XDG_DATA_HOME` | `~/.local/share` |
| `$XDG_CONFIG_HOME` | `~/.config` |
| `$XDG_CACHE_HOME` | `~/.cache` |

应用数据路径：`$XDG_DATA_HOME/${appid}`（例：`~/.local/share/org.deepin.browser`）

**禁止直接写入 `$HOME`！**

### 7. DEBIAN 钩子脚本规范

- **禁止修改系统文件**的 postinst/prerm 脚本无法上架商店
- `rm -rf` 使用变量或外部输入时**必须加双引号**

```bash
# ✅ 正确
rm -rf "$INSTALL_DIR/tmp"

# ❌ 错误
rm -rf $TEMP_PATH/*
```

- **禁止** `rm -rf /*`、`rm -rf /`
- 建议用 `shellcheck` 检查脚本语法

```bash
sudo apt install shellcheck
shellcheck DEBIAN/postinst DEBIAN/prerm DEBIAN/postrm
```

## 完整打包流程

### Step 1：创建目录结构

```bash
APPID="org.example.myapp"
mkdir -p ${APPID}/{entries/applications,entries/icons/hicolor/scalable/apps,files/bin}
```

### Step 2：编写 info 文件

```json
{
    "appid": "${APPID}",
    "name": "MyApp",
    "version": "1.0.0",
    "arch": ["amd64"],
    "permissions": {
        "autostart": false,
        "notification": false,
        "trayicon": false,
        "clipboard": false,
        "account": false,
        "bluetooth": false,
        "camera": false,
        "audio_record": false,
        "installed_apps": false
    },
    "support-plugins": [],
    "plugins": []
}
```

### Step 3：编写 desktop 文件

```ini
[Desktop Entry]
Name=MyApp
Name[zh_CN]=我的应用
Comment=My Application
Exec=/opt/apps/${APPID}/files/bin/myapp
Icon=${APPID}
Type=Application
Terminal=false
StartupNotify=true
Categories=Development;
```

### Step 4：放置应用文件

```
files/bin/myapp          # 可执行文件
files/lib/libfoo.so      # 依赖库（如有）
```

### Step 5：生成 deb

```bash
# 在 ${APPID} 父目录执行
dpkg-deb --build ${APPID} ${APPID}_1.0.0_amd64.deb
```

或使用标准 debian 目录结构：

```
${APPID}/
├── DEBIAN/
│   ├── control
│   └── postinst (如需要)
├── opt/apps/${APPID}/
│   ├── entries/
│   ├── files/
│   └── info
└── usr/share/applications/${APPID}.desktop  # 或通过 entries/ 映射
```

### debian/control 示例

```
Package: org.example.myapp
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <you@example.com>
Description: My Application
```

## 支持的 CPU 架构

| 架构 | CPU 系列 |
|------|---------|
| amd64 | x86: 海光、兆芯、Intel、AMD |
| arm64 | ARM64: 飞腾、鲲鹏、海思麒麟、瑞芯微 |
| loongarch64 | 龙芯 3A5000/3B5000+ |
| mips64el | 龙芯 3A4000/3A3000 及更早 |
| sw_64 | 申威 CPU |

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 快捷方式不显示 | Exec 路径无效 / desktop 编码非 UTF-8 | 检查路径；保存为 UTF-8 |
| 图标不显示 | Icon 路径错误 | 使用相对名称或确认绝对路径 |
| 安装被拒 | postinst/prerm 修改了系统文件 | 删除或重写钩子脚本 |
| info 文件无效 | JSON 格式错误（多余空格/字段拼写错误） | 严格 JSON 格式校验 |
| 中文乱码 | desktop 文件非 UTF-8 编码 | 保存为 UTF-8 编码 |
