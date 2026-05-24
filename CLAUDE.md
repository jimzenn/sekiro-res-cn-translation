# Sekiro: Resurrection — 简体中文翻译工程 (sekiro-res-cn-translation)

## 这个仓库在干什么

把 `sekiro-improved-chinese`（一个只做"把原版简中重译得更贴原意"的 mod）合并进大型重制 mod **Sekiro: Resurrection**，产出一套**统一、贴原意、且覆盖 Resurrection 全部新增内容**的简体中文。

最终产物 = `build/`，可直接覆盖进 Sekiro Resurrection 的 mod 目录（`build/msg/zhocn/` + `build/font/` 盖进去即可）。

背景与所有踩坑见 `MEMORY.md`，**动手前先读它**。

## 条目状态（`translation/*.json` 里的 `status`）

首轮 999 条已全部完成，当前只剩两种 status：

- `from_improved`（20129）— 来自改善版的原版译文，**权威基准，需要认真讨论才能动**。不是绝对不可动——发现确凿问题（术语不一致、原文理解偏差、改善版本身的内部矛盾等）可以回炉，但默认保留，改动前先把理由摆出来与用户对齐。`風船 → 纸气球` 这次的整套术语统一即是先例（见 git log，关键词 kamifūsen）。
- `done`（999）— Claude 首轮翻的 Resurrection 新增/缺口部分。**非权威**，发现问题随时回炉。

历史 status `needs_polish` / `needs_translation` 现已无残留（git 历史里能查到首轮原貌）。

## 当前阶段：调整与修复

首轮覆盖完了，未来工作模式不是"翻新内容"而是**实战发现 + 局部修复**：

- **实战触发**：游戏里看到不通顺/串字/术语漂移的，定位到 id，改 `cn` 即可（status 保持 `done`）。
- **术语一致性 audit**：怀疑某术语用得不齐，跑临时脚本扫一遍 `done` 条目里的变体，参见 commit `c36eecf`（平田屋→平田庄 / 流派招式→流派技）的方法。
- **风格回炉**：某段 `done` 翻得不对味，参照同上下文 `from_improved` 重译。

## ⚠️ 已知薄弱点（首轮自查得出）

这些是 999 条 `done` 里最不放心的地方，碰到问题优先怀疑：

- **menu/001 65000100+** 段 — id 段历史上是 dev dummy 区，但部分有真对白；首轮当 vanilla 翻了，可能误判。
- **【未实装】壳条目**（约 47 条，主要在 menu/001）— mod 本身没写对白，仅有开发者描述串。游戏里若看到这种文字，**不是翻译 bug，是 mod 缺内容**。详见 MEMORY.md 的"dev 占位"段。
- **mod 内部说明字段**（item/020 id 1001 / 1100~1110 之流）— 真·开发者占位串，照字面译了，不影响游戏可见文本。

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
{ "id": 911042, "status": "done",
  "cn": "赤备武士  山县昌繁",                        // ← 工作/输出值，只改这个
  "en": "Redguard Elite - Masashige Yamagata",
  "jp": "赤備え武者　山縣昌繁",
  "cn_improved": null,                              // 改善版有没有（参考，勿改）
  "cn_resurrection": "赤备军精英 山县昌茂" }          // Resurrection 原中文（参考，勿改）
```

修复时**只改 `cn`**。其余字段是参照，别动。`status` 已是 `done` 的就保持 `done`。

## 翻译规范（修复时同样适用）

- **风格基准 = 改善版**。修一条前先 grep 同上下文的 `from_improved` 词条，对腔调（贴原意、克制、有古意）。
- **术语必须一致**：沿用既有译法（详见 MEMORY.md 的"首轮关键术语决定"清单）；拿不准时直接在 `from_improved` 里搜同类词。
- **来源取舍**：原版相关内容以**日文**为准（官方中文本就译自日文），英文作参考；Resurrection 新增内容多为**英文先写**，则以英文为源、日文参考。`jp` 为 `null` 的词条说明该内容只有英文，照英文翻即可。**`jp` 与 `en` 语义有出入时优先 jp**（首轮发现 mod 的 EN 常有改动甚至打破第四面墙，参见 ＭＯＤ 引用那次回炉）。
- **务必原样保留**：占位标签如 `<?goodsItemNum@4300?>`、换行 `\n`、全角空格 `　`(`　`)、以及任何格式控制符——别翻译、别删、别改位置。
- 描述类长文本注意**行宽与换行**，参考同类 `from_improved` 词条的断行习惯，避免单行过长在游戏里溢出。
- **dev 占位 / `ダミー` / `話す：xxx` / `リマインド` 等开发者描述**：包「【未实装】xxx」壳，不字面译。

## 生成 build 并提交（重要规矩）

1. 改完 `translation/*.json` 后跑：`python3 scripts/compile_build.py`（生成 `build/`，末尾会自校验：把成品解回去逐条比对 `cn`，输出 `OK` 才算成功）。
2. **`sources/` 与 `build/` 每次提交都要同步**：凡改了 `translation/` 就重新 compile，把 `build/` 一起 commit，保证仓库里永远有一份可直接用的成品。
3. 工具用法：`python3 scripts/build_translation.py` 会**从 sources 重新生成对齐 JSON**——注意它会覆盖 `translation/`，仅在需要重置/重新对齐时用，平时改翻译不要跑它。

## 技术约束

- 所有输出用 **DFLT(zlib)** 压缩，游戏能正常读（不需要、也不要用 Oodle）。
- **不要碰** `sources/resurrection/msg/zhocn/menu.msgbnd.dcx`——那是原版 Oodle(KRAK) 文件，本项目用改善版 menu 当底，已不需要它（详见 MEMORY.md）。
- ⚠️ **此环境无法实机测试**：首次出 build 后，请在游戏里抽查关键文本（boss 名、新道具说明、新对话）确认不串字、不溢出、占位符正常。
