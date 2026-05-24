# Sekiro: Resurrection — 简体中文翻译工程 (sekiro-res-cn-translation)

## 这个仓库在干什么

把 `sekiro-improved-chinese`（一个只做"把原版简中重译得更贴原意"的 mod）合并进大型重制 mod **Sekiro: Resurrection**，产出一套**统一、贴原意、且覆盖 Resurrection 全部新增内容**的简体中文。

最终产物 = `build/`，可直接覆盖进 Sekiro Resurrection 的 mod 目录（`build/msg/zhocn/` + `build/font/` 盖进去即可）。

背景与所有踩坑见 `MEMORY.md`，**动手前先读它**。

## 工作分三类（看 `translation/*.json` 里的 `status`）

- `from_improved` — 来自改善版的原版译文，已是基准，**通常不用动**。
- `needs_polish` — Resurrection 已翻过的 mod 专有词条，需按改善版风格**润色**。
- `needs_translation` — Resurrection 新增、还没有中文的词条，需**从日/英新翻**（`cn` 当前是英/日兜底值）。

当前待办（建库时统计）：**item 51 polish + 50 translation；menu 898 translation；合计 ≈ 999 条。** 其余 2 万多条吃改善版。

## 仓库结构

```
sources/        原始 .dcx（只读输入）：improved-chinese + resurrection 的 zhocn/jp/en
translation/    ← 真·工作区，每个 FMG 一个 JSON。改这里。
  item/  menu/
scripts/        fmglib.py（解码/编码库）/ build_translation.py（重生成对齐JSON）/ compile_build.py（JSON→.dcx）
build/          成品 .dcx + 字体。初始为空，第一轮翻译后用 compile_build.py 生成。
```

## translation JSON 格式

```json
{ "id": 911042, "status": "needs_polish",
  "cn": "赤备军精英 山县昌茂",                       // ← 工作/输出值，只改这个
  "en": "Redguard Elite - Masashige Yamagata",
  "jp": "赤備え武者　山縣昌繁",
  "cn_improved": null,                              // 改善版有没有（参考，勿改）
  "cn_resurrection": "赤备军精英 山县昌茂" }          // Resurrection 原中文（参考，勿改）
```

翻译时**只改 `cn`**，完成后把 `status` 改成 `done`。其余字段是参照，别动。

## 翻译规范

- **风格基准 = 改善版**。动手前先扫一遍 `from_improved` 词条，熟悉它的腔调（贴原意、克制、有古意）。
- **术语必须一致**：如 流派技 / 忍义手 / 回生 / 体干 / 苇名 等沿用既有译法；拿不准时直接在 `from_improved` 词条里搜同类词。
- **来源取舍**：原版相关内容以**日文**为准（官方中文本就译自日文），英文作参考；Resurrection 新增内容多为**英文先写**，则以英文为源、日文参考。`jp` 为 `null` 的词条说明该内容只有英文，照英文翻即可。
- **务必原样保留**：占位标签如 `<?goodsItemNum@4300?>`、换行 `\n`、全角空格 `　`(`　`)、以及任何格式控制符——别翻译、别删、别改位置。
- 描述类长文本注意**行宽与换行**，参考同类 `from_improved` 词条的断行习惯，避免单行过长在游戏里溢出。

## 生成 build 并提交（重要规矩）

1. 改完 `translation/*.json` 后跑：`python3 scripts/compile_build.py`（生成 `build/`，末尾会自校验：把成品解回去逐条比对 `cn`，输出 `OK` 才算成功）。
2. **`sources/` 与 `build/` 每次提交都要同步**：凡改了 `translation/` 就重新 compile，把 `build/` 一起 commit，保证仓库里永远有一份可直接用的成品。
3. 工具用法：`python3 scripts/build_translation.py` 会**从 sources 重新生成对齐 JSON**——注意它会覆盖 `translation/`，仅在需要重置/重新对齐时用，平时改翻译不要跑它。

## 技术约束

- 所有输出用 **DFLT(zlib)** 压缩，游戏能正常读（不需要、也不要用 Oodle）。
- **不要碰** `sources/resurrection/msg/zhocn/menu.msgbnd.dcx`——那是原版 Oodle(KRAK) 文件，本项目用改善版 menu 当底，已不需要它（详见 MEMORY.md）。
- ⚠️ **此环境无法实机测试**：首次出 build 后，请在游戏里抽查关键文本（boss 名、新道具说明、新对话）确认不串字、不溢出、占位符正常。
