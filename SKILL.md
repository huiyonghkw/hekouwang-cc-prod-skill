---
name: hekouwang-cc-prod-skill
version: 1.0.0
description: |
  CC招车（成都希格斯·定制客运 SaaS）产品介绍动画集合 —— 生产与发布 Skill。
  在 ~/Dashboard/Product.intro 维护一套「汇总页 + N 个产品详情页」的宽屏动画 HTML（V2 黏土米白），
  每个产品按「业务/背景/需求/实现/说明」五段式成页；并用零依赖脚本把版本库导出发布到阿里云 OSS。
  当需要：新增/更新 CC招车 产品介绍页、整理产品原型截图、或把站点发布到 OSS 时使用。
triggers:
  - CC招车产品介绍
  - 产品介绍页
  - Product.intro
  - 发布到OSS
  - cc-prod
  - 班线业态
  - 定制客运产品页
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
---

# CC招车 · 产品介绍集 生产与发布

> 项目根：`~/Dashboard/Product.intro`（已是 git 仓库）。本 Skill = 怎么建页 + 怎么截图 + 怎么发布。
> 详尽设计规范见仓库内 `CLAUDE.md`（本 Skill `reference/PROJECT-CLAUDE.md` 为副本，**以仓库内为准**）。

---

## 0. 一句话

为 CC招车平台每个产品模块生成一页**宽屏滚动动画 HTML**，挂到汇总页；改完用 `./deploy-oss.sh` 一键发布到 OSS。

---

## 1. 项目结构（铁律：一个汇总页 + N 个产品详情页）

```
Product.intro/
├── index.html                 # 汇总页：平台总览 + 产品宫格（每张卡链接到详情页）
├── CLAUDE.md                  # 设计规范总纲（先读）
├── deploy-oss.sh              # ⭐ 发布脚本：git archive 导出 → 上传 OSS
├── scripts/oss_upload.py      # 零依赖 OSS 上传器（自做 HMAC-SHA1 签名 + 区域自动校正）
├── .env.oss                   # OSS 凭证（gitignore，不入库）；模板 .env.oss.example
├── shared/{tokens.css,motion.js,fonts/,favicon.svg}   # 共享设计系统
└── products/<产品名>/
    ├── index.html             # 详情页（五段式）
    ├── images/                # 页面用图（入库）
    └── 源文档/                 # PRD/PDF/原始截图（⚠️ gitignore，不入库、不发布）
```

新增产品：复制 `products/_template/` → 改文案/嵌图 → 回 `index.html` 加一张产品卡（`href` 指向该详情页）。

---

## 2. 设计与动画铁律（摘自 CLAUDE.md，违反会被打回）

- **视觉 V2 黏土米白**：底 `#faf9f5`、文字 `#1a1a18`，主色黏土橙 `--accent #c15f3c`（唯一主色），辅 石板蓝 `--accent2`/赭石 `--accent3`/砖红 `--danger`/墨绿 `--ok`。永不纯黑纯白。
- **🚫 绝不用卡片左侧彩色竖条**；卡片＝四周 1px 细边框 + 柔和投影。
- **⭐ 宽屏**：内容容器 `--maxw:1440px`（在 `shared/tokens.css`，全站统一）。卡片网格/表格/截图/流程链路吃满宽屏；只有正文段落/引言（`.lead`/`.note`）限 `max-width:720px` 保可读。
- **五段式**：每个详情页必须有 ① 业务 ② 背景 ③ 需求 ④ 实现 ⑤ 说明，用 `.section-label` 编号章节。
- **动画**：`shared/motion.js` 用 **IntersectionObserver**（不是 ScrollTrigger）做滚动入场 + 2.5s 安全兜底（截图工具/无滚动环境也不会永久隐藏）。HTML 上写 `class="reveal"` / `data-stagger` / `data-count` / `data-bar` / `data-draw` 即自动接管。
- **⭐ 图片三件套**：所有截图放进 `figure.shot`（手机/竖图/弹窗）或 `figure.wide`（宽后台图），自动获得 入场动画 + 悬停上浮 + 点击全屏 lightbox（取同 figure 的 `figcaption` 作说明），页面里不用写一行 JS/额外 CSS。
- **文案据实**：上线状态写真实（已上线/开发中/规划）；涉金额/合规中立准确。
- 页面 `<head>` 引 Noto Sans SC（Google Fonts）+ `../../shared/tokens.css` + GSAP CDN（lightbox 用）；`</body>` 前引 `../../shared/motion.js`。

---

## 3. 截图规范（产品原型 / 真机）

- **命名前缀**（一眼分端）：`xcx-*` 小程序贴图 · `bx-*` 班线新乘客端 · `dd-*` 调度端 · `sj-*` 司机端 · `ht-*` 商户PC后台。按流程编号 `-01、-02…` + 中文页面名。
- **手机原型页截图（带 .phone 框）**：CDP 裁剪 `.phone` 元素，并把 `html/body` 背景设透明（`Emulation.setDefaultBackgroundColorOverride` 透明 + JS 清 `--color-bg`），否则圆角外的页面底色会变成「黑/色边」。
- **真机全屏截图**：本就是矩形，直接用，放进 `.shot` 白卡圆角即可。
- **体积**：统一 `sips --resampleWidth 786` 降到 786px 宽（手机图显示约 200–360px，2x 足够），控制仓库与加载。
- 整理散乱原名（`localhost_..._(iPhone 14 Pro Max) (3).png` / `SCR-2026...png`）：逐张 Read 识别内容后再 `mv` 成语义名；`源文档/` 不引用图则移动不破链。

---

## 4. 自检 / 渲染

页面是普通网页，浏览器直接开。要程序化验证（无断图、整页截图）：用 Chrome headless + CDP（`Emulation.setEmulatedMedia` reduce 或等 ≥2.5s 过兜底），抓 `document.images` 里 `!complete||naturalWidth===0` 的为断图（lightbox 空占位 `src=null` 属正常）。临时产物放 `.render/`（已 gitignore）。

---

## 5. 发布到 OSS（核心交付）

```bash
cd ~/Dashboard/Product.intro
./deploy-oss.sh                # 发布当前 HEAD（git archive 导出已跟踪文件 → 镜像上传）
./deploy-oss.sh --dry-run      # 只列将上传的文件
./deploy-oss.sh --no-delete    # 不镜像删除 OSS 上多余对象
./deploy-oss.sh --ref <commit> # 发布指定提交
```

- **先 commit 再发布**：脚本用 `git archive HEAD` 导出，只发已提交文件，自动排除 `.gitignore` 内容（各产品 `源文档/`、`.env.oss`、`.render/` 等），并额外剔除 `deploy-oss.sh`/`scripts/`/`.env.oss.example`（站点不需要）。
- **凭证**：放 `~/Dashboard/Product.intro/.env.oss`（已 gitignore）。当前生产配置：
  ```
  OSS_BUCKET=prds   OSS_PREFIX=CCZC/intro   OSS_IS_CNAME=false
  OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com   # ⚠️ 桶 prds 在「北京」，不是呼和浩特
  ```
  上传器会**自动校正区域**：若 endpoint 配错，读 OSS 返回的 `<Endpoint>` 自动切换。
- **访问地址（汇总页）**：`https://prds.oss-cn-beijing.aliyuncs.com/CCZC/intro/index.html`
- **零依赖**：`assets/oss_upload.py` 仅用 Python 标准库（自做 HMAC-SHA1 V1 签名、ThreadPool 并发、按扩展名设 Content-Type、对象 key 支持中文），无需装 ossutil / oss2。
- 本 Skill `assets/` 内附 `oss_upload.py` / `deploy-oss.sh` / `.env.oss.example` 副本，可移植到新项目（改 `OSS_PREFIX` 即可复用）。

> ⚠️ 安全：`.env.oss` 含 AccessKey 明文，**绝不入库**；若密钥曾在聊天/工单等处明文出现，建议到阿里云控制台**轮换 AccessKey**。

---

## 6. 平台事实口径（写文案前对齐，权威来源以 cczhaoche 仓库为准）

- 主体：成都希格斯网络科技；白标定制客运 SaaS（monorepo 多前端微应用 + Laravel 微服务）。
- **8 业态**：购票（班线）/包车/拼车/快车/出租车/带货/代办/非急救送。
- **5 端**：乘客端（小程序/H5，UniApp 重构）· 司机端 · 调度端 · 商户后台（Element UI CMS）· SaaS 平台后台（AntD Vue）。
- 合规上报：省级定制客运（甘肃/吉林/四川已开通）+ 部级网约车（交通运输部）；基准 JT/T 1523—2024。
- 权威资料：`~/Dashboard/cczhaoche/CLAUDE.md`、`~/Dashboard/cczhaoche/.claude/skills/cc-passenger-prototype-skill/SKILL.md`（班线原型）。

---

## 7. 现有产品（截至 2026-06-09）

| 产品 | 状态 | slug 目录 |
|---|---|---|
| 上岗认证 · 支付宝安心登记卡 | 已上线 | `上岗认证-支付宝安心登记卡产品` |
| 非急救护送 · 大国救护 | 建设交付 | `非急救护送业态产品` |
| 商户独立小程序代运营 | M1 已验证 | `微信开放平台第三方平台-商户独立小程序代运营产品` |
| 全新原生乘客端 · 班线业态 | 已交付 v2.0.0 | `全新原生乘客端小程序-班线业态产品` |
| 班线 · 上下车接驳模式 | 已上线 | `班线-接驳模式产品` |

新增产品后记得：① 加到汇总页产品卡；② `commit`；③ `./deploy-oss.sh` 发布。
