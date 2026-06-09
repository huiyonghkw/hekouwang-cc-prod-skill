# CC招车 · 产品介绍动画集合（Product.intro）

> 本文件是这个项目的总纲。每次开工先读它。给 Claude / 协作者看，约定**做什么、怎么做、放哪里、用什么风格**。

---

## 1. 这个项目是什么

为 **CC招车平台**（成都希格斯网络科技的定制客运 SaaS）生成一套**HTML 动画介绍页面集合**——完整讲清平台里每一个产品模块的 **业务、背景、需求、实现、说明**。

- 视觉与动效基于两个 Skill：
  - **`hekouwang-content-factory`**（会勇禾口王内容工厂）→ 提供字体 / 配色 / 卡片 / 海报式版式（本项目默认 **V2 黏土米白**）。
  - **`hyperframes`** → 提供 GSAP 动画心智模型，以及（可选）把页面改编成 **1080×1920 竖屏短视频**。
- 产出是**带滚动动画的网页**（不是静态截图卡），所以叫「动画版本的 HTML」。

### 结构铁律：一个汇总页 + N 个产品详情页

> 每个产品都隶属平台 → **必须**有一个汇总页统领，点击任一产品卡进入它的详情页。

```
汇总页 index.html  ──►  products/<slug>/index.html（某产品详情）
（平台总览 + 产品宫格）       （业务/背景/需求/实现/说明 五段式）
```

---

## 2. CC招车平台速览（写文案前先懂）

| 维度 | 内容 |
|---|---|
| 主体 | 成都希格斯网络科技有限公司（CC系统 / 希格斯） |
| 形态 | **白标定制客运 SaaS** —— monorepo 多前端微应用 + PHP/Laravel 微服务；一套系统多租户输出，每个运营商有独立品牌的各端应用 |
| 业态（8） | **购票（班线客运）/ 包车 / 拼车 / 快车 / 出租车 / 带货 / 代办 / 非急救送** —— 乘客端 `.biz-tabs`，前 7 项为标准固定项、**非急救送为新增第 8 业态**，可标签切换 |
| 端（5） | 乘客端（微信小程序 Webview + H5，UniApp 重构中）· 司机端（UniApp）· 调度端（UniApp）· 企业商户后台（Element UI CMS）· SaaS 平台管理后台（Ant Design Vue） |
| 接入运营商 | 30+ 家（万顺叫车 / T6出行 / 大国出行 / 曲靖城际 / 沅快车 / 掌上巴士 …） |
| 关键对接 | 高德开放平台、微信支付服务商分账、保险（永丰保代） |
| 合规基准 | JT/T 1523—2024《定制客运网络平台技术要求》 |
| 合规上报 | **省级定制客运数据上报**（甘肃 / 吉林 / 四川已开通）+ **部级网约车数据上报**（交通运输部） |

**已知产品模块**（详情页围绕它们展开，需求文档投放后细化）：
一键叫车留座 · 改签功能 · 子业态标签切换筛选 · 班线定向优惠券 · 保险增值服务（开发中）· 合规零风险运营 · 司机端版本迭代 …

> 权威资料（只读参考，别改）——业态/端/技术口径以这两处为准：
> - `~/Dashboard/cczhaoche/CLAUDE.md`（工程总纲：monorepo 各端微应用与微服务，端的准确清单在此）
> - `~/Dashboard/cczhaoche/.claude/skills/cc-passenger-prototype-skill/SKILL.md`（乘客端原型 Skill：`.biz-tabs` 标准 7 业态、设计系统）
>
> 业务/运营资料（只读参考）：
> - `~/Documents/成都希格斯网络科技有限公司/CC招车平台/`（运营商档案、`CC招车产品新功能/`、原型 PDF、合规 PDF）
> - `~/Dashboard/Bear.md/01🚀CC招车出行/产品更新/`（版本更新日志、操作手册）

---

## 3. 目录结构

```
Product.intro/
├── CLAUDE.md                 # 本文件
├── index.html                # ⭐ 汇总页：平台总览 + 产品宫格（每张卡链接到详情页）
├── shared/
│   ├── tokens.css            # 设计系统：V2 黏土米白 token + 卡片/网格/动画基类
│   ├── motion.js             # GSAP ScrollTrigger 驱动（reveal/数字滚动/描线/进度条）
│   └── fonts/                # 本地内嵌 woff2（anthropicSans / anthropicMono）
├── products/
│   ├── _template/index.html  # ⭐ 产品详情页模板（五段式，照抄改内容）
│   └── <slug>/index.html     # 每个产品一个文件夹
├── requirements/             # 你投放产品需求/PRD/原型/截图的地方（一产品一子目录）
└── assets/                   # 平台级图片 / logo
```

`<slug>` 用小写英文短横线，与产品对应：`yijian-liuzuo`、`gaiqian`、`ziyetai-biaoqian`、`banxian-youhuiquan`、`baoxian-zengzhi`、`hegui-zhili` …

---

## 4. 新增一个产品的标准流程

1. **读需求**：看 `requirements/<slug>/`（或第 2 节的原始资料），提炼五段内容。
2. **建页**：`cp -r products/_template products/<slug>`，把模板里的占位文案替换成真实内容。
3. **挂卡**：回到根 `index.html` 的 `#products` 宫格，确认/新增该产品卡片：状态标签（已上线/开发中/规划）、一句话、`href` 指向 `products/<slug>/index.html`。
4. **自检**：跑第 7 节的渲染检查，肉眼复核中文字体、动画入场、无溢出。
5. **（可选）短视频**：按第 8 节为该产品出竖屏短视频。

> 一个产品详情页**必须**覆盖五段：**① 业务 ② 背景 ③ 需求 ④ 实现 ⑤ 说明**。模板已按此排好序号章节。

### 五段写什么

| 段 | 回答的问题 |
|---|---|
| ① 业务 | 这个模块在平台里干什么？服务谁（乘客/司机/运营商/平台）、属哪个子业态、在订单链路哪一环 |
| ② 背景 | 为什么要做？上线前的痛点、成本、政策/合规/竞争驱动 |
| ③ 需求 | 要做到什么？可量化的验收点、边界约束、体验/合规红线 |
| ④ 实现 | 怎么落地？关键流程、三端交互、后台配置、对接（高德/微信分账/保险） |
| ⑤ 说明 | 使用须知/FAQ、上线状态与版本、与其他模块的关系 |

---

## 5. 视觉版本（默认 V2，可切换）

三套视觉来自 `hekouwang-content-factory`，结构通用、只换字体+配色。**本项目默认 V2**——黏土米白、editorial 官网质感，且与 hyperframes 视频同源，保证图文与视频同品牌。

| | 适用 | 怎么用 |
|---|---|---|
| **V2 黏土米白**（默认） | 官网调性的产品介绍，本项目主用 | 已落在 `shared/tokens.css` |
| V3 Google 财经风 | 数据极重的模块（对账/分账/报表） | 参见 Skill §13，换 token |
| V1 暗黑科技风 | 偏炫酷营销 | 参见 Skill §1–8 |

**配色语义（V2，勿乱用）**：黏土橙 `--accent #c15f3c`=核心/主 highlight（CC 品牌主色）· 石板灰蓝 `--accent2 #5c6b7a`=扩展/对比 · 赭石 `--accent3 #a07a3c`=参数/类比 · 砖红 `--danger`=风险合规 · 墨绿 `--ok`=已上线。

**字体**：拉丁/数字 = Anthropic Sans（本地 `shared/fonts/`）；中文 = 思源黑体 Noto Sans SC（Google Fonts CDN，需联网）；代码/标签 = Anthropic Mono（本地）。字体栈已配在 tokens.css。

---

## 6. 设计与动画铁律（务必遵守）

来自内容工厂 §9 实测反馈，违反会被打回：

1. **🚫 绝不用「卡片左侧彩色竖条」**——不加 `border-left:Npx solid 主色`，不用 `::before` 画左侧色条。卡片统一**四周 1px 细边框 + 柔和投影**；强调色只放小色点 / 序号 / 徽标 / 极淡背景。
2. **永不纯白纯黑**：底 `#faf9f5`，文字 `#1a1a18`。
3. **黏土橙是唯一主色**：石板蓝 / 赭石作辅，别多色乱用，保持克制。
4. **亮色靠投影出层次**：白卡放在米白底上必须有 `box-shadow`（tokens 已给 `--shadow`）。
5. **中文可读性**：正文 ≥16px、行高 1.85；标题字重 800–900。
6. **动画要克制、有目的**：滚动入场（`.reveal` / `[data-stagger]`）+ 关键数字滚动（`[data-count]`）+ 链路描线（`[data-draw]`）+ 进度条生长（`[data-bar]`）。**确定性**，不用 `Math.random()`。尊重 `prefers-reduced-motion`（motion.js 已处理降级）。
7. **⭐ 截图图片三件套（全站统一，自动接管）**：所有产品截图都放进 `figure.shot`（竖图 / 手机 / 弹窗）或 `figure.wide`（宽后台图）容器（或给任意 `img` 加 `class="zoomable"`），即自动获得 ——① **入场动画**：把 figure 放进 `.reveal` / `data-stagger` 容器随滚动淡入；② **悬停动效**：鼠标移上去容器上浮 + 投影加重、图片微放大、`zoom-in` 光标；③ **点击放大**：弹出全屏 lightbox（自动取同 figure 内 `figcaption` 作说明），点空白 / × / Esc 关闭。**样式在 `tokens.css`、行为在 `motion.js`，页面里不用写一行 JS / 额外 CSS**。新页面照用 `.shot` / `.wide` 类名即可，别自己另造图片交互。
8. **品牌只在 footer / 顶栏**：Hero 与章节标题里不堆品牌名。
9. **⭐ 宽屏布局**：页面整体走宽屏，内容容器宽度 `--maxw:1440px`（定义在 `shared/tokens.css`，全站统一）。**别回到 1100px 窄列**——大屏要把卡片网格、宽截图铺开用满。唯一例外：**正文段落 / 引言**单独限更窄的可读上限（如 `.lead`/`.note` 用 `max-width:720px`），避免一行字太长难读；图片、卡片网格、表格、流程链路则吃满 `--maxw`。改宽度只改 token 这一处。

### 动画 API（写在 HTML 上，motion.js 自动接管）

| 写法 | 效果 |
|---|---|
| `class="reveal"` | 元素滚动进视口时淡入上移 |
| `data-stagger="0.08"`（容器） | 子元素错峰依次入场 |
| `data-count="98" data-decimals="0"` | 数字从 0 滚到目标值 |
| `data-bar="92"`（条） | 宽度从 0% 生长到 92% |
| `data-draw`（SVG path） | 描边沿路径生长 |
| `figure.shot` / `figure.wide` / `img.zoomable` | 图片自动获得悬停动效 + 点击全屏放大（lightbox），无需写 JS |

页面 `<head>` 需引入 GSAP + ScrollTrigger CDN（见模板），并在 `</body>` 前引 `shared/motion.js`。

---

## 7. 渲染 / 自检

页面是普通网页，浏览器直接开即可。要出**截图/封面**用 Chrome headless（本地字体需 `--allow-file-access-from-files`）：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --allow-file-access-from-files --disable-gpu --no-sandbox \
  --window-size=1280,900 --hide-scrollbars --force-device-scale-factor=2 \
  --screenshot="out.png" --virtual-time-budget=5000 "file://<绝对路径>/index.html"
```

- Chrome：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`　Node：v22
- 自检清单：中文是否落到思源黑体（不发虚）· 卡片有无左侧色条（必须无）· 首屏 reveal 是否显示 · 数字是否滚动到正确终值 · 窄屏（≤860px）网格是否塌成单列 · 无横向溢出。
- 临时渲染产物放 `.render/`（已是临时目录，勿提交）。

---

## 8. （可选）竖屏短视频

按内容工厂 §12 + `hyperframes` Skill，把某个产品详情页改编成 **1080×1920** 竖屏短视频（视频号/抖音/小红书视频），视觉沿用 V2，与图文同品牌。要点：

- 工作流两段式：**先出无人声静音预览 MP4 + 配音脚本.md**，用户自己录音后再合成有声成片（用户不喜欢 AI 配音）。
- 开场第一镜**绝不放品牌卡**，直接上主题钩子；品牌签收卡放片尾。封面即片头。
- 视频要**完整覆盖**详情页内容（一图一镜），别只做几个大数字。
- 渲染是长任务，用后台跑；`hyperframes` 的 `lint/validate/inspect` 三关要过。
- 视频项目单独建目录（如 `products/<slug>/video/`），别和网页混。

---

## 9. 合规红线（CC招车涉客运/支付，务必注意）

- 文案据实：上线状态写真实版本（已上线/开发中/规划），别把未上线说成已上线。
- 涉及金额/分账/保险/费率：表述中立准确，不夸大收益、不做投资诱导。
- 引用运营商名称、证照、商户号等敏感信息：只在确有授权的展示场景使用，截图注意打码。
- 合规基准对齐 JT/T 1523—2024；涉数据上报据实写：**省级定制客运上报**（甘肃/吉林/四川已开通，其余省份按实际进度，别全写成已开通）+ **部级网约车上报**（交通运输部）。

---

## 当前进度

- [x] 项目骨架 + 共享设计系统（tokens.css / motion.js / 本地字体）
- [x] 汇总页 `index.html`（平台总览 + 6 个已知模块占位卡）
- [x] 产品详情页模板 `products/_template/`
- [ ] 各产品详情页（等 `requirements/` 投放需求后逐个建）
- [ ] （可选）各产品竖屏短视频
