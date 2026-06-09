#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零依赖阿里云 OSS 上传器（仅用 Python 标准库，自做 HMAC-SHA1 V1 签名）。
把一个本地目录递归上传到 oss://{BUCKET}/{PREFIX}/，自动按扩展名设置 Content-Type。

用法：
    OSS_ACCESS_KEY=... OSS_SECRET_KEY=... OSS_ENDPOINT=oss-cn-huhehaote.aliyuncs.com \
    OSS_BUCKET=prds OSS_PREFIX=CCZC/intro \
    python3 oss_upload.py <本地目录> [--delete-extraneous] [--dry-run]

环境变量：
    OSS_ACCESS_KEY / OSS_SECRET_KEY   必填，AccessKey
    OSS_ENDPOINT                      必填，如 oss-cn-huhehaote.aliyuncs.com
    OSS_BUCKET                        必填，如 prds
    OSS_PREFIX                        目标前缀，如 CCZC/intro（默认空＝桶根）
    OSS_IS_CNAME                      true 时把 ENDPOINT 当自定义域名直连（默认 false＝虚拟主机 bucket.endpoint）

说明：本脚本走虚拟主机风格 https://{bucket}.{endpoint}/{key}，对象 key 可含中文（URL 路径按 UTF-8 百分号编码，
签名用未编码的 CanonicalizedResource）。--delete-extraneous 会删除目标前缀下、本地已不存在的对象（镜像同步）。
"""
import os, sys, hmac, hashlib, base64, mimetypes, urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
from email.utils import formatdate
from concurrent.futures import ThreadPoolExecutor, as_completed

# 扩展名 → Content-Type（补齐 mimetypes 缺失/不准的几个）
EXTRA_CT = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".ico": "image/x-icon",
    ".mp4": "video/mp4", ".md": "text/markdown; charset=utf-8",
}

def env(k, default=None, required=False):
    v = os.environ.get(k, default)
    if required and not v:
        sys.exit(f"[错误] 缺少环境变量 {k}")
    return v

def content_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in EXTRA_CT:
        return EXTRA_CT[ext]
    guessed, _ = mimetypes.guess_type(path)
    return guessed or "application/octet-stream"

class OSS:
    def __init__(self):
        self.ak = env("OSS_ACCESS_KEY", required=True)
        self.sk = env("OSS_SECRET_KEY", required=True)
        self.endpoint = env("OSS_ENDPOINT", required=True).replace("https://", "").replace("http://", "").rstrip("/")
        self.bucket = env("OSS_BUCKET", required=True)
        self.prefix = (env("OSS_PREFIX", "") or "").strip("/")
        self.is_cname = (env("OSS_IS_CNAME", "false") or "").lower() == "true"
        self.host = self.endpoint if self.is_cname else f"{self.bucket}.{self.endpoint}"

    def resolve_endpoint(self):
        """探测桶真实区域：若所配 endpoint 与桶不符，OSS 会在错误里返回正确 <Endpoint>，自动切换。"""
        if self.is_cname:
            return
        try:
            date, auth = self._sign("GET", "")
            req = urllib.request.Request(f"https://{self.host}/?max-keys=1", method="GET")
            req.add_header("Date", date); req.add_header("Authorization", auth); req.add_header("Host", self.host)
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")
            if "<Endpoint>" in body:
                ep = body.split("<Endpoint>")[1].split("</Endpoint>")[0].strip()
                if ep and ep != self.endpoint:
                    print(f"[自动校正] 桶 {self.bucket} 实际区域端点：{ep}（原配置 {self.endpoint}）")
                    self.endpoint = ep
                    self.host = f"{self.bucket}.{ep}"
        except Exception:
            pass

    def _sign(self, verb, key, content_type="", content_md5=""):
        date = formatdate(usegmt=True)
        canonical_resource = f"/{self.bucket}/{key}" if key else f"/{self.bucket}/"
        string_to_sign = f"{verb}\n{content_md5}\n{content_type}\n{date}\n{canonical_resource}"
        sig = base64.b64encode(hmac.new(self.sk.encode(), string_to_sign.encode("utf-8"), hashlib.sha1).digest()).decode()
        return date, f"OSS {self.ak}:{sig}"

    def _url(self, key, query=""):
        path = "/" + urllib.parse.quote(key, safe="/")
        return f"https://{self.host}{path}" + (("?" + query) if query else "")

    def put(self, key, data, ctype):
        date, auth = self._sign("PUT", key, ctype)
        req = urllib.request.Request(self._url(key), data=data, method="PUT")
        req.add_header("Date", date)
        req.add_header("Authorization", auth)
        req.add_header("Content-Type", ctype)
        req.add_header("Host", self.host)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status

    def delete(self, key):
        date, auth = self._sign("DELETE", key)
        req = urllib.request.Request(self._url(key), method="DELETE")
        req.add_header("Date", date); req.add_header("Authorization", auth); req.add_header("Host", self.host)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status

    def list_keys(self):
        """列出目标前缀下所有对象 key（分页）。"""
        keys, marker = [], ""
        while True:
            q = f"prefix={urllib.parse.quote(self.prefix + '/')}&marker={urllib.parse.quote(marker)}&max-keys=1000"
            date, auth = self._sign("GET", "", "")
            # list 走 bucket 根资源签名： CanonicalizedResource = /bucket/
            req = urllib.request.Request(f"https://{self.host}/?{q}", method="GET")
            req.add_header("Date", date); req.add_header("Authorization", auth); req.add_header("Host", self.host)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            ns = "{http://doc.oss-aliyun.com/spec/2006-03-01/}"
            root = ET.fromstring(body)
            # 命名空间可能存在也可能不存在，做兼容
            def findall(tag):
                res = root.findall(f"{ns}{tag}")
                return res if res else root.findall(tag)
            for c in findall("Contents"):
                k = c.find(f"{ns}Key"); k = k if k is not None else c.find("Key")
                if k is not None: keys.append(k.text)
            trunc = root.find(f"{ns}IsTruncated") or root.find("IsTruncated")
            nm = root.find(f"{ns}NextMarker") or root.find("NextMarker")
            if trunc is not None and trunc.text == "true":
                marker = nm.text if nm is not None else (keys[-1] if keys else "")
            else:
                break
        return keys

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit("用法: python3 oss_upload.py <本地目录> [--delete-extraneous] [--dry-run]")
    root = os.path.abspath(args[0])
    if not os.path.isdir(root):
        sys.exit(f"[错误] 目录不存在: {root}")
    dry = "--dry-run" in flags
    oss = OSS()
    if not dry:
        oss.resolve_endpoint()

    # 收集本地文件
    files = []
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n == ".DS_Store":
                continue
            full = os.path.join(dirpath, n)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            key = f"{oss.prefix}/{rel}" if oss.prefix else rel
            files.append((full, key))

    print(f"目标: oss://{oss.bucket}/{oss.prefix}/  (host={oss.host})")
    print(f"本地: {root}  共 {len(files)} 个文件")
    if dry:
        for _, k in sorted(files, key=lambda x: x[1]):
            print("  [dry] PUT", k)
        return

    ok, fail = 0, []
    def upload(item):
        full, key = item
        with open(full, "rb") as f:
            data = f.read()
        oss.put(key, data, content_type(full))
        return key
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(upload, it): it for it in files}
        for fu in as_completed(futs):
            it = futs[fu]
            try:
                k = fu.result(); ok += 1
                print(f"  ✓ {k}")
            except urllib.error.HTTPError as e:
                fail.append((it[1], f"HTTP {e.code} {e.read().decode('utf-8','ignore')[:200]}"))
            except Exception as e:
                fail.append((it[1], str(e)))

    # 镜像删除（可选）
    if "--delete-extraneous" in flags:
        local_keys = {k for _, k in files}
        try:
            remote = oss.list_keys()
            extra = [k for k in remote if k not in local_keys]
            for k in extra:
                oss.delete(k); print(f"  ✗ 删除多余 {k}")
            print(f"镜像同步：删除 {len(extra)} 个本地已不存在的对象")
        except Exception as e:
            print(f"[警告] 列举/删除阶段失败（上传不受影响）: {e}")

    print(f"\n完成：成功 {ok} / {len(files)}" + (f"，失败 {len(fail)}" if fail else ""))
    for k, err in fail:
        print(f"  失败 {k}: {err}")
    base = f"https://{oss.host}/{oss.prefix}/index.html" if oss.prefix else f"https://{oss.host}/index.html"
    print(f"\n访问地址（汇总页）：{base}")
    if fail:
        sys.exit(1)

if __name__ == "__main__":
    main()
