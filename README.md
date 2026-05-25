<div align="center">

# 🌸🌸 JyGet — 二次元风格磁力下载器 🌸🌸

> 🚀 **比迅雷更快，比夸克更干净，比百度网盘更自由 —— 二次元磁力下载器** 🚀

[![GitHub Stars](https://img.shields.io/github/stars/MeachalLouisJunyan/jyget?style=for-the-badge&logo=github&color=ff69b4)](https://github.com/MeachalLouisJunyan/jyget)
[![License MIT](https://img.shields.io/badge/License-MIT-ff69b4?style=for-the-badge&logo=open-source-initiative&color=ff69b4)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-ff69b4?style=for-the-badge&logo=python&logoColor=white&color=ff85a2)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)]()
[![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)]()
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)]()

</div>

---

## 🌟 为什么选择 JyGet？ 🌟

受够了迅雷的 **烦人广告** 🪟？受不了夸克的 **下载限速** 🐢？对百度网盘的 **各种捆绑** 🔗 感到绝望？

**JyGet** 来了！一款 **开箱即用、粉嫩可爱、高速稳定** 的二次元磁力下载工具，让你重拾下载的自由与快乐！🎀✨

---

## 📊 功能对比 — 谁才是下载王者？ 👑

| 特性 | 🎀 **JyGet** | ⚡ 迅雷 | 🦆 夸克 | 🌀 百度网盘 |
|------|:---:|:---:|:---:|:---:|
| 🚫 **无广告** | ✅ **✔️** | ❌ 广告满天飞 | ❌ 有广告 | ❌ 广告+推广 |
| 🚀 **不限速** | ✅ **✔️ 满速下载** | ❌ 非会员限速 | ❌ 非会员限速 | ❌ 严重限速 |
| 🔓 **开源** | ✅ **MIT 开源** | ❌ 闭源 | ❌ 闭源 | ❌ 闭源 |
| 🧲 **磁力支持** | ✅ **✅ 完美支持** | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 🎀 **二次元主题** | ✅ **粉嫩可爱 💕** | ❌ 商务风格 | ❌ 冷淡风格 | ❌ 毫无审美 |
| 🧹 **无客户端捆绑** | ✅ **纯净单文件** | ❌ 捆绑一堆 | ❌ 捆绑浏览器 | ❌ 全家桶套餐 |

> 💖 **JyGet 完胜！** —— 只有 JyGet 做到了 **无广告、不限速、开源、磁力全支持** 还自带二次元可爱主题！🎉

---

## 🚀 快速安装 🚀

### 📦 方法一：pip 安装依赖

```bash
# 1️⃣ 克隆仓库 🧬
git clone https://github.com/MeachalLouisJunyan/jyget.git
cd jyget

# 2️⃣ 一键安装依赖 📥
pip install -r requirements.txt

# 3️⃣ 启动！🎮
python main.py
```

### 🔧 方法二：安装 aria2 引擎（推荐）

JyGet 基于 aria2 引擎，安装 aria2 可获得最佳下载体验：

```bash
# 🪟 Windows — 使用 winget
winget install aria2

# 🍺 macOS — 使用 Homebrew
brew install aria2

# 🐧 Linux — 使用 apt
sudo apt install aria2
```

> 💡 aria2 已安装？跳过此步！JyGet 会自动检测并使用系统中的 aria2 🎯

---

## 📸 界面预览 🎨

```
┌─────────────────────────────────────────────────┐
│  🌸 JyGet — 二次元磁力下载器          ─ □ × │
├─────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐ │
│  │                                             │ │
│  │   🌸 欢迎使用 JyGet 🌸                     │ │
│  │                                             │ │
│  │   🎀 粉色可爱的主界面                       │ │
│  │   🧲 粘贴磁力链接即可下载                   │ │
│  │   📊 实时显示下载速度                       │ │
│  │                                             │ │
│  │   [➕ 添加下载]  [⏸️ 暂停]  [▶️ 继续]      │ │
│  │                                             │ │
│  └─────────────────────────────────────────────┘ │
│  ⬇️ 下载中: 12.5 MB/s  ⬆️ 上传: 2.3 MB/s       │
│  📋 任务列表: 3 进行中 / 5 已完成               │
└─────────────────────────────────────────────────┘
```

> 🌸 *粉白渐变主色调，圆角毛玻璃效果，二次元看板娘点缀，每一处像素都透露着可爱！* 💕

<!-- TODO: 插入实际截图 — 粉色二次元风格的 GUI 界面，包含磁力链接输入框、任务列表、速度仪表盘和可爱的看板娘装饰 -->

---

## 🛠️ 技术栈 🛠️

```
🎀  JyGet
  ├── 🐍 Python 3.9+        — 核心语言，优雅简洁
  ├── ⚡ aria2              — 下载引擎，高性能低资源
  ├── 🖼️ tkinter             — GUI 框架，原生轻量
  ├── 🧵 asyncio             — 异步 IO，不卡界面
  ├── 🌐 DHT 协议            — 无 Tracker 也能连 peers
  └── 💾 JSON 持久化         — 任务列表自动保存
```

### 为什么选择这套技术栈？🤔

| 技术 | 优势 |
|------|------|
| 🐍 **Python** | 开发效率高，生态丰富，跨平台无忧 |
| ⚡ **aria2** | 命令行下载利器，轻量高速，支持多协议 |
| 🖼️ **tkinter** | 零额外依赖，原生外观，启动飞快 |
| 🌐 **DHT 网络** | 去中心化，无需 Tracker 服务器 |

---

## 🎮 使用指南 📖

| 步骤 | 操作 | 效果 |
|:----:|------|------|
| 1️⃣ | 运行 `python main.py` | 🎀 粉色主界面弹出 |
| 2️⃣ | 点击「添加下载」 | 📝 输入框出现 |
| 3️⃣ | 粘贴磁力链接或选择 `.torrent` 文件 | 🧲 自动解析任务信息 |
| 4️⃣ | 点击「开始下载」 | ⚡ 连接 DHT 网络，满速下载！ |
| 5️⃣ | 管理任务 | ⏯️ 暂停 / ▶️ 恢复 / ❌ 删除 |
| 6️⃣ | 🎉 下载完成！ | 📂 一键打开下载目录 |

---

## ⚙️ 自定义配置 🎛️

JyGet 开箱即用，但你也完全可以按需调整：

```python
# 🎨 自定义配置示例
config = {
    "max_speed_download": "0",        # ⬇️ 下载限速 (0=不限速)
    "max_speed_upload": "0",          # ⬆️ 上传限速 (0=不限速)
    "listen_port": 6881,              # 🔌 监听端口
    "save_path": "./downloads",       # 📁 下载目录
    "dht_bootstrap_nodes": [...],     # 🌐 DHT 节点列表
    "theme_pink_level": 255,          # 💖 粉色浓度 (0-255)
}
```

---

## 📂 项目结构 📂

```
jyget/
├── 🚪 main.py           # 程序入口，启动一切
├── 🎨 gui.py            # 粉嫩二次元 GUI 界面
├── ⚙️ engine.py          # aria2 引擎封装层
├── 📋 requirements.txt  # Python 依赖清单
├── 🛠️ aria2c.exe        # Windows 内置 aria2
└── 📖 README.md         # 就是本文件啦~
```

---

## 🤝 加入我们 💪

想让 JyGet 变得更好用、更可爱吗？欢迎贡献你的一份力量！

- 🐛 发现了 Bug？ → [提交 Issue](https://github.com/MeachalLouisJunyan/jyget/issues)
- 💡 有好想法？ → [发起 Discussion](https://github.com/MeachalLouisJunyan/jyget/discussions)
- 🚀 想写代码？ → **Fork → PR → Merge** 三步走！
- ⭐ 喜欢这个项目？ → **点个 Star 就是最大的支持！**

---

## 📄 开源许可 📄

本项目基于 **MIT 许可证** 开源 🎉 — 你可以自由使用、修改、分发，甚至用于商业项目。

---

<div align="center">

# 🌟🌟🌟 **感谢你的关注！** 🌟🌟🌟

> 🎀 **JyGet** — 让下载回归纯粹，用可爱点亮每一天 💖

[![GitHub](https://img.shields.io/badge/GitHub-MeachalLouisJunyan/jyget-ff69b4?style=for-the-badge&logo=github)](https://github.com/MeachalLouisJunyan/jyget)

⭐ **如果 JyGet 让你感到快乐，请给它一颗 Star ~** ⭐

<sub>Made with 💖🌸☕🐱 by 二次元爱好者</sub>

**✨ 愿世界温柔以待，愿你下载愉快 ✨**

</div>
