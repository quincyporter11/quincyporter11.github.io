from pathlib import Path
from datetime import datetime
import shutil
import yaml
import markdown

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "site"

def parse_post(path: Path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    else:
        meta, body = {}, text

    meta.setdefault("title", path.stem)
    meta.setdefault("slug", path.stem)

    if "date" in meta:
        try:
            meta["date"] = datetime.fromisoformat(str(meta["date"]))
        except Exception:
            meta["date"] = None
    else:
        meta["date"] = None

    html = markdown.markdown(
        body,
        extensions=["fenced_code", "codehilite", "tables", "toc", "attr_list"],
        extension_configs={"codehilite": {"guess_lang": False, "noclasses": False}},
        output_format="html5",
    )
    return {**meta, "html": html}

def load_posts():
    posts = []
    for md in sorted(POSTS_DIR.glob("*.md")):
        posts.append(parse_post(md))
    posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    return posts

def load_about():
    p = DATA_DIR / "about.yaml"
    if not p.exists():
        return {"name": "About", "tagline": "", "bio": "", "now": [], "links": []}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    data.setdefault("name", "About")
    data.setdefault("tagline", "")
    data.setdefault("bio", "")
    data.setdefault("now", [])
    data.setdefault("links", [])
    return data

def build():
    # clean output
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    # copy static
    shutil.copytree(STATIC_DIR, OUT_DIR / "static")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    def url_for(endpoint, **values):
        # mimic the few routes you use
        if endpoint == "static":
            filename = values.get("filename", "")
            return f"/static/{filename.lstrip('/')}"
        if endpoint == "index":
            return "/"
        if endpoint == "about":
            return "/about/"
        if endpoint == "post":
            slug = values["slug"]
            return f"/post/{slug}/"
        raise ValueError(f"Unknown endpoint: {endpoint}")

    env.globals["url_for"] = url_for

    posts = load_posts()
    about = load_about()

    # render index
    index_tpl = env.get_template("index.html")
    (OUT_DIR / "index.html").write_text(index_tpl.render(posts=posts), encoding="utf-8")

    # render about
    about_tpl = env.get_template("about.html")
    (OUT_DIR / "about" ).mkdir(exist_ok=True)
    (OUT_DIR / "about" / "index.html").write_text(about_tpl.render(me=about), encoding="utf-8")

    # render posts
    post_tpl = env.get_template("post.html")
    for p in posts:
        d = OUT_DIR / "post" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(post_tpl.render(post=p), encoding="utf-8")

    print(f"Built site to: {OUT_DIR}")

if __name__ == "__main__":
    build()
