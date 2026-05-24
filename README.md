# sekiro-res-cn-translation

把 **Chinese Translation Redone**（社区俗称"猫粮汉化"，更贴原意的原版简中重译）合并进重制 mod **Sekiro: Resurrection**，
产出一套统一、贴原意、并覆盖 Resurrection 全部新增内容的简体中文。

成品在 `build/`，可直接覆盖进 Resurrection 的 mod 目录（`msg/zhocn/` + `font/`）。

- 工作流程、翻译规范、提交规矩 → 见 [`CLAUDE.md`](./CLAUDE.md)
- 文件格式、关键发现、踩坑记录 → 见 [`MEMORY.md`](./MEMORY.md)

纯 Python 工具链（`scripts/`），无 Windows / Oodle 依赖。

## 致谢 / Credits

没有以下两份上游 Nexus mod 就没有这份汉化。请在任何转载/再分发中保留对它们的致谢。

### 应用对象 — [Sekiro: Resurrection](https://www.nexusmods.com/sekiro/mods/723)（Nexus #723）

重制游戏机制的大型 overhaul mod，本项目仅翻译其 `msg/zhocn/` 文本（基于其 `jp/` 与 `en/` 原文），
不修改其玩法、动画、视效或其他 asset。

- **Author**：Ionian
- **Co-developer**：Mikiri / totallynotshinobi
- **Nexus uploader**：It4444
- **S:R Team file credits**（按原页面 Permissions and credits）：
  - Graphic Design：edpratti（Discord）
  - In-game Lighting：[dmc99](https://www.nexusmods.com/sekiro/users/65651661)
  - Quality of life & programming：PhantomKunai（Discord）
  - Animation：[zpdmiller](https://www.nexusmods.com/sekiro/users/75509258)、[.itsigor](https://www.nexusmods.com/sekiro/users/105103343)、[Matalayudasleazy](https://www.nexusmods.com/sekiro/users/54843437?tab=about+me)
  - VFX：[Leo Ashina](https://www.nexusmods.com/sekiro/users/177475032)
  - Misc Contributions：Abacabb（Texture）、Katalash（DsMapStudio）、Meowmaritus（Dsanimstudio）、Foxyhooligans、Kirfnir

### 翻译风格基准与原版译文来源 — [Chinese Translation Redone (Simplified & Traditional)](https://www.nexusmods.com/sekiro/mods/170)（Nexus #170）

社区俗称"猫粮汉化"。本项目复用其全部原版简中文本（20129 条 `from_improved`）作为术语与风格权威，
并复用其附带的字体包（源流明朝、青柳隷書しも、汉仪雪君）。重译风格（贴 JP 原意、古风、术语规范）
是本项目的根。

- **Author**：CatFood Can（罐装猫粮）
- **Nexus uploader**：ranaragua
- **Version referenced**：0.9.1（2021-06-21）

## 许可 / License

详见 [`LICENSE`](./LICENSE)。要点：

- 本仓库**原创**部分（`scripts/` 工具链 + `translation/*.json` 中 `status == "done"` 的新增/缺口翻译）
  以 **CC BY-NC-SA 4.0** 授权。
- 上游素材保留各自授权，再分发须同时遵守：
  - **CatFood Can**：非商用；转载注明作者；**修改前须事先获得作者许可**。
  - **Ionian / S:R Team**：使用 asset 须注明原作者；不得在小幅修改后将作品声称为自己原创。
- 字体均为免费可用（源流明朝、青柳隷書しも 为免费可商用；汉仪雪君为个人免费）。

本项目为**非营利同人作品**，与 FromSoftware、Activision、Ionian、CatFood Can 均无任何官方关联。
