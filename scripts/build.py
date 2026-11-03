"""Builds the SVG cards used in the profile README.

Run: python scripts/build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

USER = "hassaan2077"
ASSETS = Path(__file__).resolve().parent.parent / "assets"

BLUE = "#407BFF"
BLUE_SOFT = "#9DBBFF"
CARD = "#0F1424"
BORDER = "#22304F"
TEXT = "#EAF0FF"
BODY = "#C2CBE0"
MUTED = "#8793B0"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def svg(width, height, label, body, extra_style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(label)}">
  <style>
    .h {{ font: 700 22px {SANS}; fill: {TEXT} }}
    .k {{ font: 13px {SANS}; fill: {MUTED} }}
    .d {{ font: 14.5px {SANS}; fill: {BODY} }}
    .t {{ font: 600 12px {SANS}; fill: {BLUE_SOFT} }}
    .g {{ font: 600 13px {SANS}; fill: {BLUE_SOFT} }}
    .s {{ font: 600 12px {SANS}; fill: {MUTED}; letter-spacing: 1.5px }}
    .m {{ font: 12px {SANS}; fill: {MUTED} }}
    {extra_style}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#121A33"/><stop offset="1" stop-color="{CARD}"/>
    </linearGradient>
  </defs>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="url(#bg)" stroke="{BORDER}"/>
{body}
</svg>
"""


def wrap(text, max_chars):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines


def tags_row(tags, x, y):
    out = []
    for tag in tags:
        w = 16 + len(tag) * 7.2
        out.append(f'  <rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{BLUE}" fill-opacity=".14" stroke="{BLUE}" stroke-opacity=".35"/>'
                   f'<text class="t" x="{x + w / 2:.0f}" y="{y + 16}" text-anchor="middle">{escape(tag)}</text>')
        x += w + 8
    return "\n".join(out)


# ---------------------------------------------------------------- projects

PROJECTS = [
    {
        "file": "project-healthsync",
        "name": "HealthSync",
        "kind": "Final-year project · 1st position · Android app",
        "desc": "A hospital communication app that connects patients, doctors, hospital staff and admins. "
                "Real-time chat and video calls, clinical tasks routed to departments, patient health notes, "
                "AI brain-MRI analysis and an AI health assistant.",
        "tags": ["React Native", "Firebase", "PyTorch", "Flask", "Cloudflare Workers"],
        "go": "Website & screenshots",
        "wide": True,
    },
    {
        "file": "project-rag",
        "name": "Multi-Document RAG",
        "kind": "AI · Question answering",
        "desc": "Ask questions in plain English across many PDFs. Answers come only from the documents.",
        "tags": ["LangChain", "Milvus", "FastAPI"],
        "go": "View project",
    },
    {
        "file": "project-mri",
        "name": "MRI De-blurring",
        "kind": "Internship · NESCOM",
        "desc": "A convolutional autoencoder that turns blurry brain MRI scans into sharp ones.",
        "tags": ["TensorFlow", "Keras"],
        "go": "View project",
    },
    {
        "file": "project-fuzzy",
        "name": "Fuzzy Keyword Matching",
        "kind": "Client project · NLP",
        "desc": "Tags pharmaceutical publications with topics, products and diseases using fuzzy matching.",
        "tags": ["Python", "pandas", "RapidFuzz"],
        "go": "View project",
    },
    {
        "file": "project-dress",
        "name": "Dress Domain",
        "kind": "Web · Live demo",
        "desc": "An online clothing store with men, women and kids collections, product pages and a cart.",
        "tags": ["React", "React Router"],
        "go": "Live demo",
    },
    {
        "file": "project-shop",
        "name": "Shop Management System",
        "kind": "Windows desktop app",
        "desc": "Manage products, customers and employees, with separate admin and employee logins.",
        "tags": ["C#", "WinForms", "SQL Server"],
        "go": "View project",
    },
]


def project_svg(p):
    wide = p.get("wide")
    W, H = (856, 250) if wide else (424, 250)
    max_chars = 108 if wide else 44
    body = [
        f'  <rect x="24" y="24" width="6" height="26" rx="3" fill="{BLUE}"/>',
        f'  <text class="h" x="42" y="45">{escape(p["name"])}</text>',
        f'  <text class="k" x="42" y="70">{escape(p["kind"])}</text>',
    ]
    y = 104
    for line in wrap(p["desc"], max_chars)[:4]:
        body.append(f'  <text class="d" x="24" y="{y}">{escape(line)}</text>')
        y += 22
    body.append(tags_row(p["tags"], 24, H - 64))
    body.append(f'  <text class="g" x="{W - 24}" y="{H - 24}" text-anchor="end">{escape(p["go"])} →</text>')
    return svg(W, H, f'{p["name"]}: {p["desc"]}', "\n".join(body))


# ---------------------------------------------------------------- toolbox

SKILLS = [
    ("LANGUAGES", ["Python", "JavaScript", "C++", "SQL"]),
    ("AI", ["Machine Learning", "RAG", "LLMs", "LangChain", "Hugging Face", "Milvus"]),
    ("FRAMEWORKS", ["React", "React Native", "Firebase", "Flask", "REST APIs", "Docker"]),
    ("DATABASES", ["MySQL", "Firebase"]),
    ("TOOLS", ["Git", "GitHub", "VS Code", "Google Colab", "Visual Studio", "Figma"]),
]


def toolbox_svg():
    W = 856
    rows = []
    y = 40
    for title, items in SKILLS:
        rows.append(f'  <text class="s" x="24" y="{y + 16}">{title}</text>')
        rows.append(tags_row(items, 170, y))
        y += 44
    H = y + 16
    label = "Toolbox. " + ". ".join(f"{t.title()}: {', '.join(i)}" for t, i in SKILLS)
    return svg(W, H, label, "\n".join(rows))


def write(name, content):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / f"{name}.svg").write_text(content, encoding="utf-8")
    print("wrote", name)


if __name__ == "__main__":
    for p in PROJECTS:
        write(p["file"], project_svg(p))
    write("toolbox", toolbox_svg())
