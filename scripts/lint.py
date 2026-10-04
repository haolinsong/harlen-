#!/usr/bin/env python3
"""第二大脑 · 体检脚本（只读，不修改任何文件）。

用法：
    python3 scripts/lint.py            # 在库根目录或任意位置执行均可

退出码：0 = 无错误；1 = 存在错误级问题（断链、缺字段、index 不一致等）。
"""

import os
import re
import sys
import datetime
from collections import defaultdict

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(VAULT, "wiki")
TODAY = datetime.date.today()

errors, warns, notes = [], [], []


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def walk_md(root):
    out = []
    for base, dirs, files in os.walk(root):
        # Skill 示例和依赖文档不是知识页面，不能掩盖真正的断链。
        dirs[:] = [d for d in dirs if d not in {
            ".obsidian", ".git", ".trash", ".agents", ".codex", "node_modules",
        }]
        out += [os.path.join(base, f) for f in files if f.endswith(".md")]
    return sorted(out)


def split_front(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5:]


def parse_fm(block):
    data, key = {}, None
    for line in (block or "").splitlines():
        if re.match(r"^\s*-\s+", line) and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.strip()[2:].strip().strip('"'))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [v.strip().strip('"') for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = val.strip('"')
    return data


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def rel(path):
    return os.path.relpath(path, VAULT)


# ---------- 收集 ----------
wiki_md = walk_md(WIKI)
raw_md = walk_md(os.path.join(VAULT, "raw"))
output_md = walk_md(os.path.join(VAULT, "outputs"))
pages = {os.path.splitext(os.path.basename(p))[0]: p for p in walk_md(VAULT)}
managed_page_names = {
    os.path.splitext(os.path.basename(p))[0] for p in wiki_md + output_md
}

REQUIRED_COMMON = ["title", "type", "created", "updated"]
REQUIRED_BY_TYPE = {
    "concept": ["tags", "aliases", "sources"],
    "entity": ["tags", "aliases", "sources"],
    "howto": ["tags", "aliases", "sources", "verified"],
    "source": ["tags", "sources"],
    "overview": ["tags"],
    "index": ["tags"],
    "log": ["tags"],
}
STALE_DAYS = {"high": 90, "medium": 180, "low": 365}

# ---------- 0. 目录完整性 ----------
for rel_dir in ["raw", "raw/assets", "raw/personal", "wiki", "wiki/sources",
                "wiki/concepts", "wiki/howto", "wiki/entities",
                "outputs", "scripts"]:
    if not os.path.isdir(os.path.join(VAULT, rel_dir)):
        errors.append(f"目录缺失: {rel_dir}/")

# ---------- 1. frontmatter ----------
ingested_raw = set()
alias_map = defaultdict(list)
for path in wiki_md:
    name = os.path.splitext(os.path.basename(path))[0]
    block, body = split_front(read(path))
    if block is None:
        errors.append(f"{rel(path)} 缺少 frontmatter")
        continue
    fm = parse_fm(block)
    ptype = fm.get("type", "")
    if ptype not in REQUIRED_BY_TYPE:
        errors.append(f"{rel(path)} 的 type 无法识别: {ptype!r}")
    for key in REQUIRED_COMMON + REQUIRED_BY_TYPE.get(ptype, []):
        if key not in fm:
            errors.append(f"{rel(path)} 缺 frontmatter 字段: {key}")
    for alias in fm.get("aliases", []) if isinstance(fm.get("aliases"), list) else []:
        alias_map[alias].append(name)
    for src in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
        ingested_raw.add(src)

    # 正文长度
    if ptype in {"concept", "entity", "howto", "source"}:
        if len(re.sub(r"\s", "", body)) < 100:
            warns.append(f"{rel(path)} 正文不足 100 字，疑似 stub")

    # 时效
    vol = fm.get("domain_volatility", "high")
    base = fm.get("last_reviewed") or fm.get("updated") or fm.get("created")
    if base and isinstance(base, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", base):
        try:
            age = (TODAY - datetime.date.fromisoformat(base)).days
            limit = STALE_DAYS.get(vol if isinstance(vol, str) else "high", 90)
            if age > limit:
                warns.append(f"{rel(path)} 已 {age} 天未复核（阈值 {limit} 天）")
        except ValueError:
            pass
    if ptype == "howto":
        verified = fm.get("verified")
        if isinstance(verified, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", verified):
            age = (TODAY - datetime.date.fromisoformat(verified)).days
            if age > 90:
                warns.append(f"{rel(path)} 的 howto 已 {age} 天未验证，操作步骤可能失效")

# ---------- 1.5 输出页（outputs/ 层） ----------
for path in output_md:
    block, body = split_front(read(path))
    if block is None:
        errors.append(f"{rel(path)} 缺少 frontmatter")
        continue
    fm = parse_fm(block)
    if fm.get("type") != "output":
        errors.append(f"{rel(path)} 的 type 应为 output")
    for key in ["title", "type", "tags", "aliases", "created", "updated", "related"]:
        if key not in fm:
            errors.append(f"{rel(path)} 缺 frontmatter 字段: {key}")
    name = os.path.splitext(os.path.basename(path))[0]
    for alias in fm.get("aliases", []) if isinstance(fm.get("aliases"), list) else []:
        alias_map[alias].append(name)
    output_rel = os.path.relpath(path, os.path.join(VAULT, "outputs"))
    top_dir = output_rel.split(os.sep, 1)[0]
    if top_dir != "维护" and re.match(r"^\d{4}-\d{2}-\d{2}-", name):
        errors.append(f"{rel(path)} 普通输出页不应使用日期前缀，应合并到稳定主题页")
    if re.search(r"[\\/:*?\"<>|#^\[\]%]", name):
        errors.append(f"文件名含禁用字符: {name}")
    if len(re.sub(r"\s", "", body)) < 100:
        warns.append(f"{rel(path)} 正文不足 100 字，输出页应能独立读懂")

# ---------- 2. 链接 ----------
link_targets = set(pages) | set(alias_map)
inbound = defaultdict(set)
for path in wiki_md + output_md:
    name = os.path.splitext(os.path.basename(path))[0]
    for target in set(re.findall(r"\[\[([^\]|#]+)", strip_code(read(path)))):
        target = target.strip()
        if target not in link_targets:
            errors.append(f"{rel(path)} 断链: [[{target}]]")
        elif target != name:
            inbound[target].add(name)

# ---------- 3. 孤立页 ----------
for path in wiki_md:
    name = os.path.splitext(os.path.basename(path))[0]
    if name in {"index", "log", "overview", "QUESTIONS"}:
        continue
    if not inbound.get(name) and name not in strip_code(read(os.path.join(WIKI, "index.md"))):
        warns.append(f"{rel(path)} 无任何入链（孤立页）")

# ---------- 4. index 一致性 ----------
index_links = {t.strip() for t in re.findall(r"\[\[([^\]|#]+)", strip_code(read(os.path.join(WIKI, "index.md"))))}
for path in wiki_md:
    name = os.path.splitext(os.path.basename(path))[0]
    if name in {"index", "log", "overview", "QUESTIONS"}:
        continue
    if name not in index_links:
        errors.append(f"{rel(path)} 未被 index.md 收录")
for target in index_links:
    if target not in link_targets:
        errors.append(f"index.md 收录了不存在的页面: [[{target}]]")
for path in output_md:
    name = os.path.splitext(os.path.basename(path))[0]
    if name not in index_links:
        warns.append(f"{rel(path)} 未在 index.md 的输出区登记")

# ---------- 5. 命名纪律 ----------
for alias, owners in alias_map.items():
    if len(set(owners)) > 1:
        errors.append(f"别名冲突: {alias} 同时指向 {', '.join(sorted(set(owners)))}")
    if alias in managed_page_names and alias not in owners:
        errors.append(f"别名冲突: {alias} 同时是页面名和其他页面的别名")
for path in wiki_md:
    name = os.path.splitext(os.path.basename(path))[0]
    if re.search(r"[\\/:*?\"<>|#^\[\]%]", name):
        errors.append(f"文件名含禁用字符: {name}")

# ---------- 6. 来源覆盖 ----------
for path in raw_md:
    r = rel(path)
    if os.path.basename(path) in {"README.md"} or ".gitkeep" in r:
        continue
    if r not in ingested_raw:
        notes.append(f"raw 中的文件尚未被任何页面引用: {r}")

# ---------- 7. log 格式 ----------
log_text = read(os.path.join(WIKI, "log.md"))
entries = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\]\s+(\S+)\s+\|\s+(.+)$", log_text, re.M)
for header in re.findall(r"^## .*$", log_text, re.M):
    if not re.match(r"^## \[\d{4}-\d{2}-\d{2}\] \S+ \| .+$", header):
        errors.append(f"log.md 条目格式异常: {header}")

# ---------- 报告 ----------
print("=" * 66)
print(f"第二大脑 · 体检报告   {TODAY}")
print("=" * 66)
print(f"wiki 页面 {len(wiki_md)}  |  输出页 {len(output_md)}  |  raw 文件 {len(raw_md)}  |  log 条目 {len(entries)}")
print()
for label, items in [("❌ 错误", errors), ("⚠️  警告", warns), ("ℹ️  提示", notes)]:
    if items:
        print(f"{label} ({len(items)})")
        for item in items:
            print(f"    {item}")
        print()
if not (errors or warns):
    print("✅ 未发现错误或警告。")
sys.exit(1 if errors else 0)
