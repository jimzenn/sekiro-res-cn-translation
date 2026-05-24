# sekiro-res-cn-translation

把 **sekiro-improved-chinese**（更贴原意的原版简中重译）合并进重制 mod **Sekiro: Resurrection**，
产出一套统一、贴原意、并覆盖 Resurrection 全部新增内容的简体中文。

成品在 `build/`，可直接覆盖进 Resurrection 的 mod 目录（`msg/zhocn/` + `font/`）。

**懒人一键更新（Windows）**：下载 [`sekiro-launcher.bat`](./sekiro-launcher.bat) 双击即可，
自动从 GitHub 拉最新 `build/` 覆盖到默认 Sekiro 安装路径下的 `mods/`。
路径不是默认的就改脚本顶部的 `SEKIRO_MODS` 变量。

- 工作流程、翻译规范、提交规矩 → 见 [`CLAUDE.md`](./CLAUDE.md)
- 文件格式、关键发现、踩坑记录 → 见 [`MEMORY.md`](./MEMORY.md)

纯 Python 工具链（`scripts/`），无 Windows / Oodle 依赖。
