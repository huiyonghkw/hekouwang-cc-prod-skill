# 更新日志 · hekouwang-cc-prod-skill

本文件记录本 Skill 的所有版本变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`。

**变更分类**
- `功能` 新增能力 · `变更` 默认/行为调整 · `优化` 既有能力打磨 · `修复` 缺陷修正 · `移除` 删除

---

## [1.0.0]

首个有记录的版本（frontmatter 已声明 `version: 1.0.0`，此前以 git 历史维护，无 CHANGELOG）。

### 既有能力（首版基线）
- **产品介绍页产线**：在 `~/Dashboard/Product.intro` 维护「汇总页 + N 个产品详情页」的宽屏动画 HTML
  （V2 黏土米白），每个产品按「业务/背景/需求/实现/说明」五段式成页。
- **原型截图整理**：把 CC招车（成都希格斯·定制客运 SaaS）产品原型图归位到各详情页。
- **一键发布 OSS**：零依赖脚本 `assets/deploy-oss.sh` + `assets/oss_upload.py` 把版本库导出发布到
  阿里云 OSS，配置走 `assets/.env.oss.example`。
- **项目护栏**：`reference/PROJECT-CLAUDE.md` 落地到目标项目，约束目录/视觉/发布口径。
