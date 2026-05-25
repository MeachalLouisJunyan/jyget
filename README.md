
<div align="center">

# 🌸 JyGet — 二次元风格磁力下载器

> ✨ **Anime 主题 | 轻量 | 高速 | 基于 aria2**

[![GitHub](https://img.shields.io/badge/GitHub-JyGet-ff69b4?style=flat-square&logo=github)](https://github.com/MeachalLouisJunyan/jyget)
[![Python](https://img.shields.io/badge/Python-3.8+-ffb6c1?style=flat-square&logo=python)](https://python.org)
[![aria2](https://img.shields.io/badge/engine-aria2-ff85a2?style=flat-square)](https://aria2.github.io)

</div>

---

## 📖 简介

**JyGet** 是一款主打 **二次元风格** 的磁力链接 / BitTorrent 下载工具，基于 `aria2` 引擎构建，拥有粉嫩可爱的动画主题 GUI。

无论是追番、下资源还是日常 BT 下载，JyGet 都能给你带来既赏心悦目又高效稳定的下载体验~ 🎀

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 🧲 **磁力链接** | 直接粘贴 magnet 链接即可开始下载 |
| 📂 **种子文件** | 支持加载 `.torrent` 文件 |
| ⏯️ **暂停 / 恢复** | 随时暂停或继续下载任务 |
| 🧵 **多线程** | 充分利用带宽，满速下载 |
| 🌐 **DHT 节点发现** | 无需 Tracker 也能找到 peers |
| 🎀 **Anime 粉嫩 GUI** | 二次元主题，可爱到不想关 |
| 🚦 **速度限制** | 自定义下载/上传速度上限 |
| ⚙️ **aria2 引擎** | 成熟稳定，高性能核心 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 操作系统：Windows / macOS / Linux

### 安装与运行

```bash
# 1️⃣ 克隆仓库
git clone https://github.com/MeachalLouisJunyan/jyget.git
cd jyget

# 2️⃣ 安装依赖
pip install -r requirements.txt

# 3️⃣ 启动 JyGet 🎉
python main.py
```

---

## 🎮 使用指南

1. **启动程序** → 弹出粉色可爱主界面 💖
2. **添加下载** → 粘贴磁力链接或选择 `.torrent` 文件
3. **开始下载** → 自动连接 DHT 网络，寻找 peers
4. **管理任务** → 暂停 / 恢复 / 限速 / 删除
5. **完成！** 🎉

---

## 🛠️ 配置

JyGet 默认开箱即用，你也可以在 `gui.py` 或 `engine.py` 中调整以下参数：

- ⬆️ 上传速度上限
- ⬇️ 下载速度上限
- 🔌 监听端口
- 📁 下载保存路径
- 🌐 DHT 引导节点

---

## 📦 依赖

项目依赖见 [`requirements.txt`](requirements.txt)，核心依赖：

- `aria2c` — 下载引擎
- `tkinter` / `PyQt` — GUI 框架（视具体实现）
- 标准库模块 — 无需额外安装

---

## 📁 项目结构

```
jyget/
├── main.py          # 🚪 程序入口
├── gui.py           # 🎨 图形界面（Anime 主题）
├── engine.py        # ⚙️ aria2 下载引擎封装
├── requirements.txt # 📋 Python 依赖
├── aria2c.exe       # 🔧 aria2 可执行文件（Windows）
└── README.md        # 📖 本文件
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！一起让 JyGet 变得更可爱更好用~ 💪🌸

---

## 📄 许可证

本项目基于 **MIT 许可证** 开源。

---

<div align="center">

**🌟 如果喜欢 JyGet，别忘了给个 Star ~ ⭐**

[👉 前往 GitHub](https://github.com/MeachalLouisJunyan/jyget)

<sub>Made with 💖 & ☕</sub>

</div>
