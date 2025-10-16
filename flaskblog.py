from pathlib import Path
from datetime import datetime
import yaml
import markdown
import time
from flask import Flask, render_template, abort

# run
# (venv) PS C:\Users\quinc\Desktop\python\code_blog> flask --app flaskblog.py run --debug

# initialize main variables
app = Flask(__name__)

POSTS_DIR = Path(__file__).parent / "posts"
ABOUT_YAML = Path(__file__).parent / "data" / "about.yaml"

def parse_post(path: Path):
    """
    Parse a Markdown file with YAML front matter:
    ---
    title: ...
    slug: ...
    date: YYYY-MM-DD
    tags: [...]
    ---
    <markdown body>
    """
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        # split front matter
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    else:
        meta, body = {}, text

    meta.setdefault("title", path.stem)
    meta.setdefault("slug", path.stem)
    # normalize date
    if "date" in meta:
        try:
            meta["date"] = datetime.fromisoformat(str(meta["date"]))
        except Exception:
            meta["date"] = None
    else:
        meta["date"] = None

    # convert markdown -> HTML with code highlighting
    html = markdown.markdown(
        body,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "noclasses": False}
        },
        output_format="html5",
    )
    return {**meta, "html": html}

def load_posts():
    posts = []
    for md in sorted(POSTS_DIR.glob("*.md")):
        try:
            posts.append(parse_post(md))
        except Exception as e:
            print(f"Failed to parse {md.name}: {e}")
    # sort newest first when date exists
    posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    return posts

# cache and change detection
ALL_POSTS = []
INDEX_BY_SLUG = {}
_posts_sig = None

def _posts_signature() -> tuple:
    files = sorted(POSTS_DIR.glob("*.md"))
    if not files:
        return (0, ())
    latest_mtime = max(int(f.stat().st_mtime) for f in files)
    names = tuple(f.name for f in files)
    return (latest_mtime, names)

def _rebuild_posts_cache():
    global ALL_POSTS, INDEX_BY_SLUG
    ALL_POSTS = load_posts()
    INDEX_BY_SLUG = {p["slug"]: p for p in ALL_POSTS}

# ---- ABOUT cache & signature ----
ABOUT = {}
_about_sig = None  # last modified time

def _about_signature() -> int:
    try:
        return int(ABOUT_YAML.stat().st_mtime)
    except FileNotFoundError:
        return 0

def _load_about_yaml() -> dict:
    """Load about.yaml and apply safe defaults."""
    try:
        data = yaml.safe_load(ABOUT_YAML.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        data = {}
    # defaults
    data.setdefault("name", "About")
    data.setdefault("tagline", "")
    data.setdefault("bio", "")
    data.setdefault("now", [])
    data.setdefault("links", [])
    # optional: ensure types
    if not isinstance(data.get("now"), list):
        data["now"] = [str(data["now"])]
    if not isinstance(data.get("links"), list):
        data["links"] = []
    return data

# ---- Unified auto-reload throttle ----
_last_check = 0
def _maybe_reload_content():
    global _posts_sig, _about_sig, _last_check, ABOUT
    now = time.time()
    if now - _last_check < 1.0:  # throttle checks to once per second
        return
    _last_check = now

    # posts
    psig = _posts_signature()
    if psig != _posts_sig:
        print("Detected change in posts/, rebuilding cache...")
        _rebuild_posts_cache()
        _posts_sig = psig

    # about.yaml
    asig = _about_signature()
    if asig != _about_sig:
        print("Detected change in data/about.yaml, reloading...")
        ABOUT = _load_about_yaml()
        _about_sig = asig

@app.before_request
def _refresh_dynamic_content():
    _maybe_reload_content()

# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html", posts=ALL_POSTS)

@app.route("/post/<slug>")
def post(slug):
    p = INDEX_BY_SLUG.get(slug)
    if not p:
        abort(404)
    return render_template("post.html", post=p)

@app.route("/about")
def about():
    # ABOUT is auto-loaded & cached; just pass to template
    return render_template("about.html", me=ABOUT)

# Optional: initialize caches once at startup so first request is warm
def _init_caches():
    global _posts_sig, _about_sig, ABOUT
    _rebuild_posts_cache()
    _posts_sig = _posts_signature()
    ABOUT = _load_about_yaml()
    _about_sig = _about_signature()

_init_caches()