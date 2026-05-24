# MEMORY — 关键发现与踩坑记录

> 这是工程的"为什么"。改东西前读一遍，能少踩很多坑。

## 文件格式速查

- `.msgbnd.dcx` = **DCX 容器** → 内含 **BND4 binder** → 内含多个 **FMG 文本文件**。
- **DCX 压缩方式**：`DFLT`(= zlib，可读可写) 或 `KRAK`(= Oodle，本项目不处理)。标记在 DCX 头偏移 `0x28`。
- **FMG**（Sekiro = wide / version 2）：头 `0x28` 字节；group 每个 **16 字节**（offsetIndex, firstId, lastId, padding）——注意是 16 不是 12；字符串偏移表是 **int64**；字符串 UTF-16LE 以 `00 00` 结尾。头里 `0x14` 处是常量 `0xFF`、`0x08` 处是常量 `1`。
- **BND4** 条目头 `0x24` 字节；msgbnd 里 FMG 数据**未二次压缩**（compressedSize == uncompressedSize）；数据区按 **0x10 对齐**。

## ⭐ 最重要的发现：中文 menu 为什么之前读不了、又为什么缺内容

- **原版 Sekiro 用 Oodle(KRAK) 压缩**（和 Elden Ring 同代；解压需要游戏自带的 `oo2core_6_win64.dll`）。DS3 及更早才用 DFLT——**别把 Sekiro 和 DS3 搞混**。
- 模组工具（Yabber / WitchyBND）**重打包时默认吐 DFLT**。推论：**仓库里 KRAK 格式的文件 = mod 从没动过的原版文件**。
- Resurrection 的 `zhocn/menu` 正是 **KRAK = 原封未动的原版**——这就是它缺掉全部 mod 新增 menu 内容的根本原因（而不是文件坏了或被人乱搞）。
- **解法**：用 `sekiro-improved-chinese` 的 menu（DFLT，完全可读，且翻译质量更高）当中文底子，顺手**绕过了 Oodle**——我们根本不需要去解那个 KRAK 文件。

## Oodle 限制（仅备查，本项目用不到）

- 曾尝试用开源 reverse 实现 `ooz`（ARM 上配 `sse2neon` 编译成功），但它解 Sekiro 的 Oodle 流时**只能解出第一个 256KB 块**就失败（老 `oo2core_6` 的某个子模式它没实现）。
- 要完整解 Oodle，正路是 **Windows 上 WitchyBND + 游戏自带 dll**。本项目刻意避开这条路。

## 翻译进度

- 首轮（PR #1，merged）：999 条全部 `done`，覆盖 item 全部 + menu/001 会話 + menu/030 イベントテキスト + 几个小 menu。
- 当前：`from_improved` 20129 / `done` 999。无残留待办。
- 缺口主要包括：新小 boss 名（Nightjar Elite、Go'riku of Misen 等）、新忍义手体术（弹反 / 飞道具返 系列、秘藏练药）、新道具（鸣种锦囊、御朱印札、可重打的 boss 追忆），以及大量 mod 新增/未被 improved-chinese 收录的对话与系统提示。

## ⭐ 首轮关键术语决定（对齐 improved-chinese）

修复时如改这些务必一并 audit 全库：

| 术语 | 译法 | **不要用** |
|---|---|---|
| `ミブ` (Mibu 风船) | 水生 | ~~壬生~~ |
| `落ち谷` | 坠落谷 | ~~坠落之谷 / 坠谷~~ |
| `仙峯寺` (峯字) | 仙峯寺 | ~~仙峰寺~~ |
| `平田屋敷` | 平田庄 | ~~平田屋 / 平田屋敷 / 平田宅邸~~ |
| `体幹` | 体干 | ~~躯干 / 体力槽~~ |
| `見切り` | 看破 | ~~识破~~ |
| `シラフジ` (Snake Eyes) | 白藤 | ~~白秋~~ |
| `弾きカウンター` | 弹反 | ~~弹反击 / 反击斩~~ |
| `飛び道具返し` | 飞道具返 | ~~飞道具弹反~~ |
| `流派技` | 流派技 | ~~流派招式~~（87:4 偏好）|
| `鬼仏` | 鬼佛 | ~~鬼仏~~（JP 字别留进 CN）|
| `御子` vs `皇子` | **JP 区分使用**：狼/尼御前称御子，穴山/守军称皇子 | 不要统一 |

注：`忍具` 短形 与 `义手忍具` 全称都可接受（improved-chinese 也都用），按上下文选。

## dev 占位文本（mod 自带未实装内容）

Resurrection 的 `jp` 里夹了相当多开发者占位串（不是真对白）：

- `話す：xxx会話` — 触发场景描述，无实际台词
- `xxxダミー（"..."と話す）` — dummy 标记的占位
- `PCから話者に話しかけた_xxx` — 测试用 hook 描述
- `xxxの説明` / `xxxリマインド` — 教程/提醒占位

首轮 47 条统一包「**【未实装】xxx**」壳（commit `f5fe8ec`）。**游戏里看到这种文字不是翻译 bug，是 mod 缺内容**。若 mod 后续版本补了对白，重跑 `build_translation.py` 会把它们回炉成新 `needs_translation`。

## EN 与 JP 不一致：偏 JP

Resurrection 的 EN 是社区翻译，偶尔会偏离 JP，最离谱的是 mod 作者用 `修練やＭＯＤの評価にうってつけ` 这种打破第四面墙的 dev voice（首轮误字面译成"于修习与ＭＯＤ评价"，commit `f5fe8ec` 改成"正合修习与试玩之用"）。**翻译时优先 JP，EN 仅作参考**。

## 仓库历史

- `33bc965` — 初始对齐工作区
- `28fa8f3` (merge) — 首轮 999 条全部完成 + ＭＯＤ/dummy 修订 + 术语对齐

## 来源与时间线

- `resurrection/zhocn/item` 改于 **2023-10**，落后 jp/en（**2024-08**，对应 1.16.1 补丁）约 10 个月——这就是 item 有缺口的原因。
- `improved-chinese` 是**纯原版改进，不含任何 Resurrection 新增内容**——它只负责"定风格 + 补原版质量"，新内容仍须从 jp/en 翻。
- `improved-chinese` 还带一套更好的中文字体（`font/`），是它"观感更佳"的一部分，已纳入 build。

## 编码器（scripts/fmglib.py）

- 纯 Python、零外部依赖（DFLT 就是标准库 `zlib`）。
- 已通过 **round-trip 字节级自验**：未改动内容重打包能 byte-for-byte 还原原文件；compile 出的 dcx 解回去与 JSON 的 `cn` 完全一致。
- 唯一兜不住的是**无法实机测试**——首个 build 必须在游戏内抽查。

## 翻译时务必保留的特殊记号

- 占位符，如 `<?goodsItemNum@4300?>`（游戏会替换成实际数字）。
- 换行 `\n`。
- 全角空格 `　`(`　`)，常用于名字中"姓 名"之间。

这些在 JSON 里原样存在，翻译时**勿动**。
