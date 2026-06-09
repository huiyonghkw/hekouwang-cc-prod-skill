#!/usr/bin/env bash
# ============================================================
# CC招车产品介绍集 —— 导出版本库文件并发布到阿里云 OSS
#   1. 用 git archive 把【当前已提交】的文件导出到临时目录（干净，自动排除 源文档/ 等被忽略内容）
#   2. 调用 scripts/oss_upload.py（零依赖）镜像上传到 oss://$OSS_BUCKET/$OSS_PREFIX/
# 用法：
#   ./deploy-oss.sh                # 发布当前 HEAD
#   ./deploy-oss.sh --dry-run      # 只列将上传的文件，不真正上传
#   ./deploy-oss.sh --no-delete    # 不删除 OSS 上本地已不存在的对象（默认会镜像删除）
#   ./deploy-oss.sh --ref <commit> # 发布指定提交/分支
# 凭证：从同目录 .env.oss 读取（该文件已 gitignore，不入库）；也可直接用环境变量覆盖。
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

# ---- 载入凭证 ----
if [ -f .env.oss ]; then
  set -a; . ./.env.oss; set +a
fi
: "${OSS_ACCESS_KEY:?缺少 OSS_ACCESS_KEY（在 .env.oss 配置或导出环境变量）}"
: "${OSS_SECRET_KEY:?缺少 OSS_SECRET_KEY}"
: "${OSS_ENDPOINT:?缺少 OSS_ENDPOINT}"
: "${OSS_BUCKET:?缺少 OSS_BUCKET}"
export OSS_ACCESS_KEY OSS_SECRET_KEY OSS_ENDPOINT OSS_BUCKET
export OSS_PREFIX="${OSS_PREFIX:-CCZC/intro}"
export OSS_IS_CNAME="${OSS_IS_CNAME:-false}"

# ---- 解析参数 ----
REF="HEAD"; PY_FLAGS="--delete-extraneous"; DRY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY="--dry-run" ;;
    --no-delete) PY_FLAGS="" ;;
    --ref) shift; REF="$1" ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac; shift
done

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "[错误] 当前目录不是 git 仓库，请先 git init / commit"; exit 1
fi

STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
echo "→ 导出 $REF 的已跟踪文件到临时目录…"
git archive "$REF" | tar -x -C "$STAGE"
COUNT=$(find "$STAGE" -type f | wc -l | tr -d ' ')
echo "  导出 $COUNT 个文件（已自动排除 .gitignore 内容，如各产品 源文档/）"

# 不发布部署脚本与凭证模板本身（站点不需要）
rm -f "$STAGE/deploy-oss.sh" "$STAGE/.env.oss.example" 2>/dev/null || true
rm -rf "$STAGE/scripts" 2>/dev/null || true

echo "→ 上传到 oss://$OSS_BUCKET/$OSS_PREFIX/ …"
python3 scripts/oss_upload.py "$STAGE" $PY_FLAGS $DRY
