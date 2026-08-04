#!/usr/bin/env python3
"""Build the hosted prompt library for GitHub Pages, Sceptic's Desk brand.

Adding a prompt: add an entry to PROMPTS and re-run. Pages, the index,
and the QR payload list all follow automatically.
"""
import html, pathlib, re, shutil, json

OUT = pathlib.Path("/mnt/user-data/outputs/site")
A = "&#8217;"

# ---------------------------------------------------------------- content
# Numbering follows the GUIDE's scheme (the QR codes point at these),
# which is separate from the Prompt Vault's 1-42 numbering.
PROMPTS = {
    1: dict(
        cat="Learn any concept", phase="Learn",
        title="The infinite patient tutor",
        blurb="Turns any unfamiliar term into a plain-English explanation you can actually "
              "check, with the weakness included.",
        body="Explain [concept] to a beginner: what it is, a simple example, why traders use "
             "it, and its biggest weakness. Under 200 words.",
        swap="Replace [concept] with the term you&#8217;re stuck on.",
        note="Add &#8220;tell me where you&#8217;re uncertain&#8221; to any answer you plan to "
             "act on.",
    ),
    16: dict(
        cat="Position size", phase="Improve",
        title="Size a trade correctly",
        blurb="Works out the exact size so the loss at your stop equals the risk you chose, "
              "rather than the risk you felt like taking.",
        body="Account &pound;[X], 1% risk. [instrument] entry [E], stop [S]. Give the exact "
             "position size, show the steps.",
        swap="Replace [X], [instrument], [E], and [S] with your own numbers.",
        note="Check the arithmetic against the Position Size Calculator before you act on it. "
             "An AI can be confidently wrong about numbers.",
    ),
    19: dict(
        cat="Journal review", phase="Improve",
        title="Your AI trading coach",
        blurb="Reads a month of your journal and names the pattern costing you the most, "
              "using your real numbers.",
        body="Act as a blunt trading coach. Here&#8217;s my journal: [paste]. Find my patterns "
             "and my #1 fix for next month.",
        swap="Replace [paste] with your journal export.",
        note="Ask it not to flatter you. A coach that agrees with everything is worth nothing.",
    ),
}

PHASE_COLOUR = {"Learn": "#5B8EEA", "Build": "#32D48B",
                "Test": "#EFAF43", "Improve": "#EC745B"}

# ---------------------------------------------------------------- styles
CSS = """
:root{
  --navy:#0B1636;--navy2:#101E44;--navy3:#0A1430;--line:#26315A;--line2:#1B274C;
  --gold:#EFAF43;--gold-soft:#ECC165;
  --white:#F4F7FF;--body:#B7C1DB;--muted:#828DAF;--faint:#5C668C;
  --sans:'Space Grotesk',system-ui,-apple-system,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%}
body{background:var(--navy);color:var(--body);font-family:var(--sans);line-height:1.55;
  min-height:100vh;padding:22px 18px 40px;
  background-image:linear-gradient(rgba(123,150,220,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(123,150,220,.05) 1px,transparent 1px);
  background-size:34px 34px}
.wrap{max-width:640px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;
  padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:26px}
.mark{text-decoration:none;display:block}
.mark .the{font-family:var(--mono);font-size:9px;letter-spacing:.34em;color:var(--gold);
  display:block;margin-bottom:5px}
.mark .nm{font-weight:700;font-size:17px;color:var(--white);line-height:1.05;
  text-transform:uppercase;letter-spacing:.01em}
.mark .desc{font-family:var(--mono);font-size:8px;letter-spacing:.2em;color:var(--muted);
  text-transform:uppercase;margin-top:7px;padding-top:6px;border-top:1px solid var(--line)}
.rail{font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--faint);
  text-transform:uppercase;text-align:right;flex:none}
.tags{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.tag{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
  border-radius:5px;padding:4px 9px;border:1px solid currentColor}
.tag.num{color:var(--gold)}
h1{font-size:clamp(25px,7vw,33px);font-weight:700;color:var(--white);letter-spacing:-.02em;
  line-height:1.12;margin-bottom:12px}
.blurb{font-size:16px;color:#AEB8D6;margin-bottom:24px}
.label{font-family:var(--mono);font-size:10px;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gold);margin-bottom:9px}
.prompt{background:var(--navy2);border:1px solid var(--line);border-radius:12px;
  padding:18px 18px;font-family:var(--mono);font-size:14px;line-height:1.72;
  color:var(--body);white-space:pre-wrap;word-break:break-word}
.prompt b{color:var(--gold);font-weight:400}
button.copy{width:100%;margin-top:14px;background:var(--gold);color:#0B1636;border:0;
  border-radius:11px;padding:16px;font-family:var(--sans);font-size:16px;font-weight:700;
  cursor:pointer;letter-spacing:.01em}
button.copy:active{transform:translateY(1px)}
button.copy.done{background:#32D48B}
.swap{font-size:14px;color:var(--muted);margin-top:12px}
.note{border-left:2px solid var(--gold);background:var(--navy2);border-radius:0 10px 10px 0;
  padding:14px 16px;margin-top:24px;font-size:14.5px}
.note .l{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gold);margin-bottom:6px}
.rule{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--faint);text-align:center;margin-top:30px;line-height:1.9}
.rule b{color:var(--gold-soft)}
footer{margin-top:34px;padding-top:18px;border-top:1px solid var(--line);
  font-family:var(--mono);font-size:10.5px;line-height:1.9;color:var(--faint);
  letter-spacing:.02em}
footer a{color:var(--muted)}
.list{display:flex;flex-direction:column;gap:10px;margin-top:6px}
.item{display:flex;gap:14px;align-items:center;background:var(--navy2);
  border:1px solid var(--line);border-radius:11px;padding:14px 16px;text-decoration:none}
.item:hover{border-color:var(--gold)}
.item .n{font-family:var(--mono);font-size:16px;color:var(--gold);font-weight:700;
  min-width:30px;flex:none}
.item .t{color:var(--white);font-weight:700;font-size:15.5px;line-height:1.3}
.item .c{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);margin-top:4px}
.item .go{margin-left:auto;color:var(--gold);flex:none;font-size:17px}
@media(max-width:420px){body{padding:18px 14px 34px}.rail{display:none}}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?'
             'family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700'
             '&display=swap" rel="stylesheet">')

BRACKET = re.compile(r"\[([^\]]+)\]")


def head(title, desc, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en-GB"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0B1636">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{FONT_LINK}
<link rel="stylesheet" href="{up}assets/style.css">
</head><body><div class="wrap">"""


def header(depth, rail):
    up = "../" * depth or "./"
    return f"""<header>
<a class="mark" href="{up}"><span class="the">THE</span>
<div class="nm">Sceptic{A}s<br>Desk</div>
<div class="desc">AI Trading, Demystified</div></a>
<div class="rail">{rail}</div></header>"""


FOOTER = f"""<footer>
Educational content, not financial advice. Most retail traders lose money.
Practise on a demo account and only risk what you can afford to lose.<br>
An AI is your analyst, not your decision-maker. Verify everything.<br>
&copy; 2026 The Sceptic{A}s Desk.
</footer></div>
<script>
document.querySelectorAll('button.copy').forEach(function(b){{
  b.addEventListener('click',function(){{
    var t=document.getElementById(b.dataset.target).innerText;
    var done=function(){{b.textContent='Copied. Now paste it into your AI.';
      b.classList.add('done');
      setTimeout(function(){{b.textContent='Copy prompt';b.classList.remove('done');}},2600);}};
    if(navigator.clipboard&&navigator.clipboard.writeText){{
      navigator.clipboard.writeText(t).then(done,fallback);
    }} else {{ fallback(); }}
    function fallback(){{
      var a=document.createElement('textarea');a.value=t;a.style.position='fixed';
      a.style.opacity='0';document.body.appendChild(a);a.select();
      try{{document.execCommand('copy');done();}}catch(e){{
        b.textContent='Press and hold the prompt to copy';}}
      document.body.removeChild(a);
    }}
  }});
}});
</script></body></html>"""


def prompt_page(n, p):
    body = BRACKET.sub(lambda m: f"<b>[{m.group(1)}]</b>", p["body"])
    plain = re.sub(r"&#8217;", "'", p["body"])
    plain = re.sub(r"&pound;", "\u00a3", plain)
    plain = re.sub(r"&#8220;|&#8221;", '"', plain)
    colour = PHASE_COLOUR[p["phase"]]
    desc = html.escape(re.sub("<[^>]+>", "", p["blurb"]))
    return (head(f"#{n} {p['cat']} \u00b7 The Sceptic\u2019s Desk", desc, 3)
            + header(3, f"Prompt {n:02d}")
            + f"""
<div class="tags"><span class="tag num">Prompt {NUM(n)}</span>
<span class="tag" style="color:{colour}">{p['phase']}</span>
<span class="tag" style="color:var(--muted)">{p['cat']}</span></div>
<h1>{p['title']}</h1>
<p class="blurb">{p['blurb']}</p>
<div class="label">The prompt</div>
<div class="prompt" id="p{n}">{body}</div>
<button class="copy" data-target="p{n}">Copy prompt</button>
<p class="swap">{p['swap']}</p>
<div class="note"><div class="l">Before you act on the answer</div>{p['note']}</div>
<div class="rule">Do I understand why? &middot; Can I verify it? &middot;
What if it{A}s wrong?<br><b>If you can{A}t answer all three, you don{A}t act yet.</b></div>
"""
            + FOOTER)


def NUM(n):
    return f"{n:02d}"


def index_page():
    items = ""
    for n, p in sorted(PROMPTS.items()):
        items += (f'<a class="item" href="p/{n}/"><span class="n">{NUM(n)}</span>'
                  f'<span><span class="t">{p["title"]}</span>'
                  f'<span class="c">{p["cat"]}</span></span>'
                  f'<span class="go">&#8594;</span></a>')
    return (head("Prompt library \u00b7 The Sceptic\u2019s Desk",
                 "Scan-and-go prompts from AI Trading, Demystified.", 2)
            + header(2, "Prompt library")
            + f"""
<h1>Prompt library</h1>
<p class="blurb">The scan-and-go prompts from <i>AI Trading, Demystified</i>. Open one, copy it,
paste it into your AI assistant, and swap the bracketed parts for your own detail.</p>
<div class="list">{items}</div>
<div class="rule">An AI is your analyst, not your decision-maker.</div>
""" + FOOTER)


def home_page():
    return (head("The Sceptic\u2019s Desk \u00b7 AI Trading, Demystified",
                 "Process-first trading education. No signals, no hype.", 0)
            + header(0, "")
            + f"""
<h1>AI Trading,<br>Demystified</h1>
<p class="blurb">Use artificial intelligence to research smarter, build strategies, and sharpen
your trading. Without the hype, and without pretending it{A}s a money machine.</p>
<div class="list">
<a class="item" href="prompts/"><span class="n">&#9656;</span>
<span><span class="t">Prompt library</span>
<span class="c">Scan-and-go prompts from the guide</span></span>
<span class="go">&#8594;</span></a></div>
<div class="rule">Test ideas. Never opinions.</div>
""" + FOOTER)


def notfound_page():
    return (head("Not found \u00b7 The Sceptic\u2019s Desk", "Page not found.", 0)
            + header(0, "404")
            + f"""
<h1>That page isn{A}t here</h1>
<p class="blurb">The link may be from an older edition. The prompt library has everything that
the codes in the guide point to.</p>
<div class="list"><a class="item" href="/prompts/"><span class="n">&#9656;</span>
<span><span class="t">Prompt library</span><span class="c">All prompts</span></span>
<span class="go">&#8594;</span></a></div>
""" + FOOTER)


# ---------------------------------------------------------------- write
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "assets").mkdir(parents=True)
(OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
(OUT / "index.html").write_text(home_page(), encoding="utf-8")
(OUT / "404.html").write_text(notfound_page(), encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

pd = OUT / "prompts"
pd.mkdir()
(pd / "index.html").write_text(index_page(), encoding="utf-8")
for n, p in PROMPTS.items():
    d = pd / "p" / str(n)
    d.mkdir(parents=True)
    (d / "index.html").write_text(prompt_page(n, p), encoding="utf-8")

print("built site:")
for f in sorted(OUT.rglob("*")):
    if f.is_file():
        print(f"  {f.relative_to(OUT)}  ({f.stat().st_size:,}b)")
