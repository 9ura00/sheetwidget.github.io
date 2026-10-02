#!/usr/bin/env python3
"""OG画像(1200x630)を全言語ぶん生成する。

デザインは既存版から実測して再現している：
  背景 #FBFAF6 / 48px方眼 #ECEAE2 / 上部に8pxの緑帯 / 中央にアプリアイコン
  太字の見出し2行 / 下部に緑のブランド名
文言を変えたい時は HEADLINES を直すだけでよい。実行は `python3 img/make-og.py`。
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (251, 250, 246)
GRID = (236, 234, 226)
GREEN = (24, 128, 56)
INK = (27, 29, 31)
CELL = 48
BAR_H = 8
BRAND = "Sheet Widget"

# 2行の見出し。長すぎると自動で縮むが、意味の切れ目で手で割った方がきれい。
HEADLINES = {
    "ja": ["スプレッドシートを、", "ホーム画面に。"],
    "en": ["Your Google Sheets,", "on your Home Screen."],
    "de": ["Deine Google-Tabellen,", "auf dem Home-Bildschirm."],
    "es": ["Tus hojas de Google,", "en la pantalla de inicio."],
    "fr": ["Vos feuilles Google,", "sur votre écran d’accueil."],
    "ko": ["구글 스프레드시트를,", "홈 화면에."],
    "zht": ["把 Google 試算表,", "放到主畫面。"],
}
# 出力名だけ既存に合わせる（ja は og.png も兼ねる）
EXTRA_COPIES = {"ja": ["og.png"]}

LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"
# 日本語は「ヒラギノ角ゴシック(Hiragino Sans)」。名前の似た "Hiragino Sans GB"
# は簡体字中国語版で、一部の漢字が中国語の字形になり日本語として不自然になる。
JA = "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc"
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font_for(lang, size):
    """日本語はヒラギノ角ゴシック、韓中は Hiragino Sans GB、他は Helvetica Neue Bold。"""
    if lang == "ja":
        return ImageFont.truetype(JA, size, index=0)    # Hiragino Sans W7
    if lang in ("ko", "zht"):
        return ImageFont.truetype(CJK, size, index=2)   # W6 = 太字
    return ImageFont.truetype(LATIN, size, index=1)     # Bold


def draw_grid(d, ox=0, oy=BAR_H):
    """(ox, oy) を左上の角として CELL 間隔の方眼を引く。"""
    for x in range(ox, W, CELL):
        d.line([(x, oy), (x, H)], fill=GRID, width=1)
    for y in range(oy, H, CELL):
        d.line([(ox, y), (W, y)], fill=GRID, width=1)


def fit(d, lines, lang, start=76, margin=64):
    """2行とも収まる最大の字号を返す。"""
    size = start
    while size > 28:
        f = font_for(lang, size)
        if all(d.textlength(t, font=f) <= W - margin * 2 for t in lines):
            return f
        size -= 2
    return font_for(lang, 28)


def build(lang, lines, icon):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    draw_grid(d)
    d.rectangle([0, 0, W, BAR_H - 1], fill=GREEN)

    # icon.png は角丸のない正方形なので、iOS 相当(辺の22.37%)の角丸で抜く
    ic = icon.resize((144, 144), Image.LANCZOS)
    mask = Image.new("L", (144 * 4, 144 * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 144 * 4 - 1, 144 * 4 - 1],
                                           radius=int(144 * 4 * 0.2237), fill=255)
    ic.putalpha(mask.resize((144, 144), Image.LANCZOS))
    im.paste(ic, (W // 2 - 72, 48), ic)

    f = fit(d, lines, lang)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.18)
    top = 250 - lh // 2
    for i, t in enumerate(lines):
        d.text((W // 2, top + i * lh), t, font=f, fill=INK, anchor="ma")

    fb = font_for(lang, 34) if lang not in ("ja", "ko", "zht") else font_for("en", 34)
    d.text((W // 2, 545), BRAND, font=fb, fill=GREEN, anchor="ma")
    return im


# ── 言語に依存しないカード ──────────────────────────────────
# SNSのクローラは閲覧者の言語を見ないため、言語別の見出しを載せると
# どの言語で共有しても英語版か日本語版のどちらかに固定されてしまう。
# そこで共有用の1枚は文字を商品名だけにし、表計算らしさは
# 行番号と列見出し（数字とアルファベット＝どの言語でも読める）で出す。

HEAD_BAND = (243, 241, 235)   # 列見出し・行番号の帯
HEAD_LINE = (223, 220, 210)   # 帯の境界
HEAD_INK  = (150, 146, 136)   # 帯の文字
SEL       = (26, 115, 232)    # 選択枠。LPの --sel と同じ
SEL_FILL  = (237, 242, 250)   # 選択範囲の塗り。LPの rgba(26,115,232,.08) を背景に焼いた色

# 帯の幅をセル幅と同じにすると、帯の内側の罫線がそのまま方眼の原点になる。
# 帯だけ別の幅にすると列見出しと列がずれるので、ここは必ず CELL と揃える。
BAND = CELL
ORIGIN_X = BAND               # 方眼の左端。以降 CELL 間隔で罫線が入る
ORIGIN_Y = BAR_H + BAND       # 方眼の上端


def draw_sheet_chrome(d):
    """表計算の外枠。上に列見出し(A,B,C…)、左に行番号(1,2,3…)を敷く。"""
    d.rectangle([0, BAR_H, W, ORIGIN_Y], fill=HEAD_BAND)
    d.rectangle([0, BAR_H, ORIGIN_X, H], fill=HEAD_BAND)
    f = ImageFont.truetype(LATIN, 19, index=0)
    # 見出しはセルの中央に置く。罫線とセルの対応がずれて見えないようにする。
    for i, x in enumerate(range(ORIGIN_X, W, CELL)):
        d.text((x + CELL / 2, BAR_H + BAND / 2), chr(65 + i),
               font=f, fill=HEAD_INK, anchor="mm")
    for i, y in enumerate(range(ORIGIN_Y, H, CELL)):
        d.text((ORIGIN_X / 2, y + CELL / 2), str(i + 1),
               font=f, fill=HEAD_INK, anchor="mm")
    d.line([(ORIGIN_X, BAR_H), (ORIGIN_X, H)], fill=HEAD_LINE, width=1)
    d.line([(0, ORIGIN_Y), (W, ORIGIN_Y)], fill=HEAD_LINE, width=1)


def build_neutral(icon):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    draw_grid(d, ORIGIN_X, ORIGIN_Y)
    draw_sheet_chrome(d)
    d.rectangle([0, 0, W, BAR_H - 1], fill=GREEN)

    # 選択範囲は罫線にぴったり載せる。列は6本目〜19本目で中心が画像の中央、
    # 行は3本目〜9本目で中心が方眼部分の中央にくる。
    x1, x2 = ORIGIN_X + CELL * 5, ORIGIN_X + CELL * 18
    y1, y2 = ORIGIN_Y + CELL * 3, ORIGIN_Y + CELL * 9
    d.rounded_rectangle([x1, y1, x2, y2], radius=3, fill=SEL_FILL, outline=SEL, width=4)
    # 右下の選択ハンドル。LPと同じく白フチを付ける
    d.rectangle([x2 - 8, y2 - 8, x2 + 8, y2 + 8], fill=SEL, outline=(255, 255, 255), width=2)

    # アイコンと商品名をひとかたまりとして、枠の中央に置く
    icon_px, gap = 132, 22
    f = ImageFont.truetype(LATIN, 60, index=1)
    tb = d.textbbox((0, 0), BRAND, font=f, anchor="ma")
    text_h = tb[3] - tb[1]
    block = icon_px + gap + text_h
    top = (y1 + y2) / 2 - block / 2

    ic = icon.resize((icon_px, icon_px), Image.LANCZOS)
    mask = Image.new("L", (icon_px * 4, icon_px * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, icon_px * 4 - 1, icon_px * 4 - 1],
                                           radius=int(icon_px * 4 * 0.2237), fill=255)
    ic.putalpha(mask.resize((icon_px, icon_px), Image.LANCZOS))
    im.paste(ic, (W // 2 - icon_px // 2, int(top)), ic)
    d.text((W // 2, top + icon_px + gap - tb[1]), BRAND, font=f, fill=INK, anchor="ma")
    return im


def main():
    icon = Image.open("img/icon.png").convert("RGBA")
    # 既定は共有用の1枚だけ。言語別が要るときは --per-language を付ける。
    if "--per-language" in sys.argv:
        for lang, lines in HEADLINES.items():
            im = build(lang, lines, icon)
            for name in [f"og-{lang}.png"] + EXTRA_COPIES.get(lang, []):
                im.save(f"img/{name}")
                print("wrote img/" + name)
        return
    build_neutral(icon).save("img/og.png")
    print("wrote img/og.png")


if __name__ == "__main__":
    main()
