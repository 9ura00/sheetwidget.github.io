#!/usr/bin/env python3
"""公開用の完成品を作り、GitHub（9ura00/sheetwidget.github.io）へ送る。

  python3 publish.py           完成品を ../sheetwidget-public に作るだけ（送らない）
  python3 publish.py --push    作ってから公開リポジトリへ送る

このフォルダ（sheetwidget-lp）は「コメント付きの元データ」で、ローカルにだけ置く。
GitHub には送らない（送り先の remote も外してある）。公開側に出すのは、
  - 開発用のファイル（build.py / publish.py / img/make-og.py など）を除いたもの
  - HTML の中のコメント（HTML・JavaScript・CSS・Liquid）を取り除いたもの
だけにする。配信しているHTMLは「ソースを表示」で誰でも読めるので、
開発メモを公開しないためには、配信物そのものからコメントを消すしかない。

コメントの削除は html-minifier-terser（HTML/JS/CSSを構文として読む道具）で行う。
単純な置き換えで「//」を消すと、URL（https://）や文字列の中身まで壊すため。
改行や字下げはそのまま残し、コードの書き換え（短縮・変数名の変更）もしない。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "sheetwidget-public")
PUBLIC_REPO = "github.com/9ura00/sheetwidget.github.io.git"
GH = os.path.expanduser("~/.local/bin/gh")

# 公開しないもの（開発用）。ここに無いものは git で管理している限り公開する
PRIVATE = {"build.py", "publish.py", "img/make-og.py", ".gitignore",
           "package.json", "package-lock.json", "strip-comments.mjs"}

# Jekyll の Liquid を含むレイアウトは、構文解析にかけると {{ }} や {% %} を壊しうる。
# ここだけは HTML / CSS / Liquid のコメントを範囲を決めて取り除く（中にJSの // は無い）
LIQUID_LAYOUTS = {"_layouts/default.html", "_layouts/legal.html"}

STRIP_JS = r"""
import { minify } from 'html-minifier-terser';
import fs from 'fs';
for (const f of process.argv.slice(2)) {
  const src = fs.readFileSync(f, 'utf8');
  const out = await minify(src, {
    removeComments: true,
    collapseWhitespace: false,
    minifyCSS: { level: { 1: { specialComments: 0 }, 2: false }, format: 'beautify' },
    minifyJS: { compress: false, mangle: false, format: { comments: false, beautify: true } },
  });
  fs.writeFileSync(f, out);
}
"""


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, **kw)


def tracked_files():
    out = run(["git", "ls-files"], cwd=SRC, capture_output=True).stdout.split("\n")
    return [f for f in out if f and f not in PRIVATE]


def strip_liquid_layout(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", s, flags=re.S)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    open(path, "w", encoding="utf-8").write(s)


def ensure_stripper():
    # 削除用の道具はサイトとは別の場所（~/.cache）に入れる。リポジトリに混ぜないため
    tool = os.path.expanduser("~/.cache/sheetwidget-strip")
    if not os.path.exists(os.path.join(tool, "node_modules", "html-minifier-terser")):
        os.makedirs(tool, exist_ok=True)
        with open(os.path.join(tool, "package.json"), "w") as f:
            f.write('{"name": "sheetwidget-strip", "private": true, "type": "module"}')
        run(["npm", "i", "html-minifier-terser@7"], cwd=tool, capture_output=True)
    with open(os.path.join(tool, "strip.mjs"), "w") as f:
        f.write(STRIP_JS)
    return tool


def build_output():
    # 公開用フォルダの中身を毎回作り直す（.git だけは残す）
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        if name == ".git":
            continue
        p = os.path.join(OUT, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    files = tracked_files()
    for f in files:
        dst = os.path.join(OUT, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(SRC, f), dst)

    html = [f for f in files if f.endswith(".html") and f not in LIQUID_LAYOUTS]
    tool = ensure_stripper()
    run(["node", os.path.join(tool, "strip.mjs")] + [os.path.join(OUT, f) for f in html], cwd=tool)
    for f in LIQUID_LAYOUTS:
        if f in files:
            strip_liquid_layout(os.path.join(OUT, f))
    return files


def check_no_comments(files):
    """取り残しがないかを確かめる。見つかったら送らずに止める。"""
    bad = []
    for f in files:
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(OUT, f), encoding="utf-8").read()
        if "<!--" in s or re.search(r"\{%-?\s*comment", s):
            bad.append(f)
        # JS/CSS のコメント記号が行頭に残っていないか（URL内の // は行頭には来ない）
        elif re.search(r"^\s*(//|/\*)", s, flags=re.M):
            bad.append(f)
    if bad:
        sys.exit(f"コメントが残っている: {bad}")


def push():
    token = run([GH, "auth", "token", "--user", "9ura00"], capture_output=True).stdout.strip()
    url = f"https://x-access-token:{token}@{PUBLIC_REPO}"
    if not os.path.exists(os.path.join(OUT, ".git")):
        run(["git", "init", "-q", "-b", "main"], cwd=OUT)
    run(["git", "add", "-A"], cwd=OUT)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=OUT).returncode == 0:
        print("変更なし")
        return
    # 公開側のコミットメッセージは固定にする。元データ側のメッセージには
    # 作業の経緯が書かれることがあり、それも公開したくないため
    run(["git", "commit", "-q", "-m", "Update site"], cwd=OUT)
    run(["git", "push", "-q", url, "main:main"], cwd=OUT)
    print("送信しました")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    args = ap.parse_args()
    files = build_output()
    check_no_comments(files)
    print(f"{len(files)} ファイルを {OUT} に作成")
    if args.push:
        push()


if __name__ == "__main__":
    main()
