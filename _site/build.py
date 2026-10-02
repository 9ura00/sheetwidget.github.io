#!/usr/bin/env python3
"""index.html から各言語のページ（/en/, /ko/ …）と sitemap.xml を生成する。

なぜ生成するのか
----------------
本文は index.html 内の I18N 辞書から JavaScript で流し込んでいる。表示は問題ないが、
HTMLソースには文字が1つも無いため、クローラーがJSを実行しない場合に中身が空に見える。
また言語ごとの独立したURLが無いと、7言語ぶんの評価が1つのURLに潰れてしまう。

そこで各言語について、
  1. 本文を静的に埋め込んだ（JSなしでも読める）完全なページを
  2. 自分自身を指す canonical と、7言語＋x-default の相互 hreflang 付きで
  3. その言語の title / description / OGP と FAQ 構造化データを持たせて
出力する。表示時は従来どおり JS が同じ内容で上書きするので、挙動は変わらない。

何度実行しても同じ結果になる（data-i の中身と、マーカーで囲んだ範囲を毎回置き換える）。

使い方:
  python3 build.py            生成のみ（noindex のまま＝検索に出さない）
  python3 build.py --publish  公開用。noindex を外し、App Store の実URLを埋める

--publish を分けているのは、noindex の解除と App Store リンクの差し替えを
別々にやると必ずどちらかを忘れるため。審査通過後に1回だけ実行する。
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sheetwidget.com"

# 言語コード → (出力先ディレクトリ, html lang属性, 正規URL)
#
# 英語をルートに置く理由: Googlebot は Accept-Language を送らないため、常に
# 「英語圏の初訪問者」としてサイトを見る。ルートを日本語にすると Googlebot が
# 毎回 /en/ へ転送され、トップページ自体が評価されなくなる。
# App Store の primary locale も en-US で、流入も英語圏が主軸。
LANGS = {
    "en":  (None,  "en",      f"{SITE}/"),
    "ja":  ("ja",  "ja",      f"{SITE}/ja/"),
    "ko":  ("ko",  "ko",      f"{SITE}/ko/"),
    "zht": ("zht", "zh-Hant", f"{SITE}/zht/"),
    "es":  ("es",  "es",      f"{SITE}/es/"),
    "de":  ("de",  "de",      f"{SITE}/de/"),
    "fr":  ("fr",  "fr",      f"{SITE}/fr/"),
}
# 言語版を持たない訪問者に見せる版。ルート（英語）。
X_DEFAULT = f"{SITE}/"

# 規約・プライバシーのURL。本体と同じ構成（英語はルート直下、他は言語ディレクトリ配下）。
def legal_url(kind, lang):
    return f"{SITE}/{kind}/" if lang == "en" else f"{SITE}/{lang}/{kind}/"

# 転送だけを置くURL。
# /en/ の転送は 2026-10-02 にやめた（どこからもリンクされていないため）。
#
# 規約の旧URL（/privacy-ko/ 形式）はここに無い。あの形は一度も一般公開されて
# いないアプリのためだけの互換で、審査を差し戻して新URLのビルドを出す以上、
# 踏む人がいないため置かない。必要になったらここに1行足せば復活する。
ALIASES = {}
# hreflang の値は html lang とは別（zht → zh-Hant）
HREFLANG = {k: v[1] for k, v in LANGS.items()}

APP_STORE_URL = "https://apps.apple.com/app/id6795254414"
NOINDEX = '<meta name="robots" content="noindex">'


def load_i18n(html):
    """index.html に直書きされた I18N 辞書を node で評価して取り出す。

    JSのオブジェクトリテラルは JSON ではない（クォートが単一、末尾カンマ、
    HTML断片入り）ので、正規表現でパースせず node にそのまま解釈させる。
    """
    i = html.index("const I18N = {")
    j = html.index("let LANG = (function()")
    src = html[i:j].rstrip().rstrip(";") + "\nconsole.log(JSON.stringify(I18N));"
    out = subprocess.run([node_bin(), "-e", src], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"I18N の取り出しに失敗:\n{out.stderr}")
    return json.loads(out.stdout)


def node_bin():
    for p in ("node", os.path.expanduser("~/.nvm/versions/node/v24.17.0/bin/node")):
        if subprocess.run(["command", "-v", p], capture_output=True, shell=False,
                          executable="/bin/bash").returncode == 0 or os.path.exists(p):
            return p
    return "node"


def close_tag_end(html, open_end, tag):
    """開始タグの直後 open_end から、対応する閉じタグの開始位置を返す。

    値にも同じタグ名（<span> など）が入りうるので、単純な非貪欲マッチでは
    途中の </span> を拾って壊れる。入れ子を数えて対応を取る。
    """
    depth = 1
    pat = re.compile(rf"<(/?){tag}\b", re.I)
    pos = open_end
    while depth:
        m = pat.search(html, pos)
        if not m:
            raise ValueError(f"{tag} の閉じタグが見つからない")
        depth += -1 if m.group(1) else 1
        pos = m.end()
    return html.rindex("<", open_end, pos)


def fill_data_i(html, dic):
    """data-i="key" を持つ要素の中身を、その言語の文言で埋める。

    表示時は JS が同じ値で innerHTML を上書きするので見た目は変わらない。
    ここで埋めるのは、JSを実行しない読み手（クローラー等）のため。
    """
    out, pos, n = [], 0, 0
    pat = re.compile(r"<(\w+)([^>]*\sdata-i=\"([\w]+)\"[^>]*)>")
    while True:
        m = pat.search(html, pos)
        if not m:
            break
        tag, key = m.group(1), m.group(3)
        end = close_tag_end(html, m.end(), tag)
        out.append(html[pos:m.end()])
        out.append(dic.get(key, html[m.end():end]))
        if key in dic:
            n += 1
        pos = end
    out.append(html[pos:])
    return "".join(out), n


def head_meta(html, lang, dic):
    """head の言語依存部分（title・description・OGP・canonical）を差し替える。"""
    _, _, url = LANGS[lang]
    title, desc = dic["docTitle"], dic["metaDesc"]
    # SNSのクローラは閲覧者の言語を見ないので、言語別の絵を出し分けても
    # 共有した人の言語に固定されるだけになる。共有用は言語非依存の1枚に統一する。
    og = f"{SITE}/img/og.png"
    rep = [
        (r"<title>.*?</title>", f"<title>{title}</title>"),
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{desc}">'),
        (r'<link rel="canonical" href="[^"]*">',
         f'<link rel="canonical" href="{url}">'),
        (r'<meta property="og:title" content="[^"]*">',
         f'<meta property="og:title" content="{title}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{desc}">'),
        (r'<meta property="og:image" content="[^"]*">',
         f'<meta property="og:image" content="{og}">'),
        (r'<meta property="og:url" content="[^"]*">',
         f'<meta property="og:url" content="{url}">'),
        (r'<meta property="og:locale" content="[^"]*">',
         f'<meta property="og:locale" content="{dic["ogLocale"]}">'),
        (r'<meta name="twitter:title" content="[^"]*">',
         f'<meta name="twitter:title" content="{title}">'),
        (r'<meta name="twitter:description" content="[^"]*">',
         f'<meta name="twitter:description" content="{desc}">'),
        (r'<meta name="twitter:image" content="[^"]*">',
         f'<meta name="twitter:image" content="{og}">'),
    ]
    for pat, new in rep:
        html, k = re.subn(pat, lambda _: new, html, count=1, flags=re.S)
        if not k:
            sys.exit(f"[{lang}] head の置換に失敗: {pat}")

    # hreflang は全ページで同一（相互参照が成立していないと Google に無視される）
    block = "\n".join(
        [f'<link rel="alternate" hreflang="x-default" href="{X_DEFAULT}">']
        + [f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{LANGS[l][2]}">'
           for l in LANGS])
    html, k = re.subn(r'<link rel="alternate" hreflang="x-default".*?hreflang="fr"[^>]*>',
                      lambda _: block, html, count=1, flags=re.S)
    if not k:
        sys.exit(f"[{lang}] hreflang の置換に失敗")
    return html


def strip_tags(s):
    """構造化データ用に、文言からHTMLタグを落とす。<br> は改行にする。"""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&nbsp;", " ").replace("​", "").strip()


def structured_data(lang, dic):
    """アプリ情報と FAQ の JSON-LD。FAQ は検索結果に出る数少ない枠なので必ず入れる。"""
    _, _, url = LANGS[lang]
    app = {
        "@context": "https://schema.org", "@type": "MobileApplication",
        "name": "Sheet Widget", "operatingSystem": "iOS",
        "applicationCategory": "UtilitiesApplication", "url": url,
        "inLanguage": HREFLANG[lang],
        "description": strip_tags(dic["metaDesc"]),
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
        # ストアの掲載ページと結び付ける。installUrl は検索結果のアプリ枠に効き、
        # sameAs は「このサイトとあのアプリは同一の存在だ」と示すための対応付け。
        "installUrl": APP_STORE_URL,
        "sameAs": [APP_STORE_URL],
    }
    qa = []
    for i in range(1, 9):
        q, a = dic.get(f"q{i}"), dic.get(f"a{i}")
        if q and a:
            qa.append({"@type": "Question", "name": strip_tags(q),
                       "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}})
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "inLanguage": HREFLANG[lang], "mainEntity": qa}
    j = json.dumps
    return ('<!-- BUILD:LD -->\n'
            f'<script type="application/ld+json">{j(app, ensure_ascii=False)}</script>\n'
            f'<script type="application/ld+json">{j(faq, ensure_ascii=False)}</script>\n'
            '<!-- /BUILD:LD -->')


def put_ld(html, block):
    """構造化データをマーカーごと差し替える。初回は既存の JSON-LD を置き換える。"""
    if "<!-- BUILD:LD -->" in html:
        return re.sub(r"<!-- BUILD:LD -->.*?<!-- /BUILD:LD -->", lambda _: block,
                      html, count=1, flags=re.S)
    return re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda _: block, html, count=1, flags=re.S)


# ルートに置く振り分け。各言語ページ自体は決して転送しないので、
# どの版にもURLを直接叩けば到達できる（クローラーも含む）。
# Googlebot は Accept-Language を送らずブラウザ言語も英語相当のため、
# ここで転送されずルート＝英語版を評価する。
REDIRECT = """<script>
/* ルートのみ：ブラウザの言語に合う版へ振り分ける。
   サイト内から来た場合（言語切替で戻ってきた場合を含む）は転送しない。 */
(function(){
  try{
    if(sessionStorage.getItem('sw_pick')) return;
    if(document.referrer && new URL(document.referrer).origin === location.origin) return;
  }catch(_){}
  var n = (navigator.language || '').toLowerCase(), to = null;
  if(n.indexOf('ja') === 0)      to = '/ja/';
  else if(n.indexOf('ko') === 0) to = '/ko/';
  else if(n.indexOf('zh') === 0) to = '/zht/';
  else if(n.indexOf('es') === 0) to = '/es/';
  else if(n.indexOf('de') === 0) to = '/de/';
  else if(n.indexOf('fr') === 0) to = '/fr/';
  if(to) location.replace(to + location.search + location.hash);
})();
</script>"""


def alias_page(target):
    """旧URL用の転送ページ。検索に出す必要はないので noindex にし、
    canonical で転送先を指す。JSが無くても meta refresh とリンクで到達できる。"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0;url={target}">
<title>Sheet Widget</title>
</head>
<body>
<p><a href="{target}">Sheet Widget</a></p>
<script>location.replace("{target}" + location.search + location.hash);</script>
</body>
</html>
"""


def legal_path(kind, lang):
    """ページ内リンク用の相対パス。英語はルート直下、他は言語ディレクトリ配下。"""
    sub = LANGS[lang][0]
    return f"/{sub}/{kind}/" if sub else f"/{kind}/"


def localize_legal_links(html, lang):
    """フッターの規約リンクを、その言語版の実URLに焼き込む。

    実行時にも applyLang() が同じ書き換えをするが、それはJavaScript前提で、
    言語切替のたびに張り直すためのもの。静的HTMLの側が英語のままだと、
    JSを待たずに押した人とクローラだけが英語版へ飛ぶ。両方を正にしておく。
    """
    return re.sub(
        r'<a href="[^"]*" data-legal="(terms|privacy)"',
        lambda m: f'<a href="{legal_path(m.group(1), lang)}" data-legal="{m.group(1)}"',
        html)


def localize_alts(html, dic):
    """画像の代替テキストをその言語に。alt は innerHTML ではないので data-i では埋まらない。

    スマホ画面とウィジェットの2枚だけが中身を説明する画像。アイコン類は名前だけで足りる。
    """
    pairs = [(r'(<img src="/img/phone-home\.webp" alt=")[^"]*(")', dic["altPhone"]),
             (r'(<img class="shotWidget" id="shotWidget" src="/img/widget-budget\.webp" alt=")[^"]*(")', dic["altWidget"])]
    for pat, alt in pairs:
        html, k = re.subn(pat, lambda m: m.group(1) + alt + m.group(2), html, count=1)
        if not k:
            sys.exit(f"代替テキストの置換に失敗: {pat}")
    return html


def build_sitemap():
    """トップ・各言語ページ・規約類を列挙する。言語ページには hreflang も添える。"""
    alt = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{HREFLANG[l]}" href="{LANGS[l][2]}"/>'
        for l in LANGS)
    alt = f'    <xhtml:link rel="alternate" hreflang="x-default" href="{X_DEFAULT}"/>\n' + alt
    today = __import__("datetime").date.today().isoformat()
    urls = "\n".join(f"  <url>\n    <loc>{LANGS[l][2]}</loc>\n    <lastmod>{today}</lastmod>\n{alt}\n  </url>" for l in LANGS)
    legal = "\n".join(
        f"  <url><loc>{legal_url(kind, l)}</loc><lastmod>{today}</lastmod></url>"
        for kind in ("privacy", "terms") for l in LANGS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f"{urls}\n{legal}\n</urlset>\n")


def publish(html):
    """検索に出す状態にする。noindex を外し、CTA に App Store の実URLを張る。"""
    html = html.replace(
        "<!-- ▼リリース時にこの1行を削除（検索エンジンからの非公開設定） -->\n" + NOINDEX + "\n", "")
    html = html.replace(NOINDEX + "\n", "")
    return html.replace("const APP_STORE_URL = '';",
                        f"const APP_STORE_URL = '{APP_STORE_URL}';")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true",
                    help="noindex を外し App Store の実URLを埋める（審査通過後に1回だけ）")
    args = ap.parse_args()

    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    if args.publish:
        src = publish(src)
        # 規約・プライバシー14ページは Jekyll のレイアウト側に noindex がある。
        # ここで一緒に外さないと、公開後もその14ページだけ検索に出ない。
        lay = os.path.join(ROOT, "_layouts", "legal.html")
        t = open(lay, encoding="utf-8").read()
        open(lay, "w", encoding="utf-8").write(publish(t))
        print("  公開モード: noindex 解除 / App Store URL を設定（規約レイアウト含む）")
    i18n = load_i18n(src)

    for lang in LANGS:
        dic = i18n[lang]
        html = head_meta(src, lang, dic)
        html = put_ld(html, structured_data(lang, dic))
        html, n = fill_data_i(html, dic)
        html = localize_legal_links(html, lang)
        html = localize_alts(html, dic)
        html = re.sub(r'<html lang="[^"]*">', f'<html lang="{LANGS[lang][1]}">', html, count=1)

        # そのURLが何語なのかをページ自身に持たせる（ブラウザ設定より優先）
        head = f"<script>window.__SW_LANG='{lang}';</script>\n"
        subdir = LANGS[lang][0]
        if subdir:
            os.makedirs(os.path.join(ROOT, subdir), exist_ok=True)
            path = os.path.join(ROOT, subdir, "index.html")
        else:
            head += REDIRECT + "\n"   # 振り分けはルートだけ
            path = os.path.join(ROOT, "index.html")
        # 生成物を再入力にしても増殖しないよう、マーカーごと入れ替える
        html = re.sub(r"<!-- BUILD:HEAD -->.*?<!-- /BUILD:HEAD -->\n?", "", html, flags=re.S)
        html = html.replace(
            "</head>", f"<!-- BUILD:HEAD -->\n{head}<!-- /BUILD:HEAD -->\n</head>", 1)
        open(path, "w", encoding="utf-8").write(html)
        print(f"  {(subdir or '.') + '/index.html':22} 文言 {n} 箇所を静的化  {len(html):,} 文字")

    for path, target in ALIASES.items():
        os.makedirs(os.path.join(ROOT, path), exist_ok=True)
        open(os.path.join(ROOT, path, "index.html"), "w", encoding="utf-8").write(alias_page(target))
        print(f"  {path + '/index.html':22} → {target} へ転送")

    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(build_sitemap())
    print(f"  {'sitemap.xml':22} {len(LANGS)} 言語 + 規約 {len(LANGS)*2} ページ")


if __name__ == "__main__":
    main()
