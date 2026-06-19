# hekouwang-cc-prod-skill

CC招车（成都希格斯·定制客运 SaaS）**产品介绍动画集合** —— 生产与发布 Claude Code Skill。

在 `~/Dashboard/Product.intro` 维护一套「汇总页 + N 个产品详情页」的宽屏滚动动画 HTML（V2 黏土米白），
每个产品按 **业务 / 背景 / 需求 / 实现 / 说明** 五段式成页；并用零依赖脚本把版本库导出发布到阿里云 OSS。

- 完整产线手册见 [`SKILL.md`](./SKILL.md)
- `assets/` —— `oss_upload.py`（零依赖 OSS 上传器，自做 HMAC-SHA1 签名 + 区域自动校正）、`deploy-oss.sh`（git archive 导出 → 镜像上传）、`.env.oss.example`
- `reference/PROJECT-CLAUDE.md` —— 项目设计规范副本

## 安装

```bash
git clone git@github.com:huiyonghkw/hekouwang-cc-prod-skill.git ~/.claude/skills/hekouwang-cc-prod-skill
```

> 凭证放项目目录的 `.env.oss`（已 gitignore，不入库）。仓库内不含任何密钥。

## 依赖与视觉

- 产品页的视觉规范（V2 黏土米白：Anthropic Sans/Mono + 思源黑体、配色 token、版式、`_build` 流水线）源自 **`hekouwang-content-factory`**（会勇禾口王内容工厂）。
  > ⚠️ `hekouwang-content-factory` 是付费 Skill，**GitHub 上为 PRIVATE 私有仓库，非授权无法 clone / 获取**；本仓库只含生产/发布流程（OSS 上传器 + 产线手册），不含其字体与视觉系统。需要授权请联系 **@huiyonghkw**。
- `oss_upload.py` / `deploy-oss.sh`：零三方依赖（标准库自实现 HMAC-SHA1 签名），可独立使用。
