from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

try:
    import markdown  # type: ignore
except Exception:  # pragma: no cover - handled by requirements
    markdown = None  # fallback to plain text if not installed


BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")


# -----------------------------
# Routes
# -----------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        message = request.form.get("message", "").strip()

        if not name or not email or not message or len(password) < 8:
            flash("Please complete the form. Password must be at least 8 characters.", "error")
            return redirect(url_for("contact"))

        # Placeholder behavior: do not store or email, just show success
        flash("Thanks! Your message has been received (placeholder).", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


def _normalize_resume_markdown(text: str) -> str:
    """Apply heuristics to convert plain text resume into better Markdown.

    - Remove stray artifact lines (e.g., '1', 'Automatic Zoom')
    - Promote section headings to Markdown headings
    - Convert '•' bullets to '- '
    - Separate name from contact line and promote name to H1
    """
    lines = []
    for raw in text.splitlines():
        s = raw.strip()
        if s in {"1", "Automatic Zoom"}:
            continue
        lines.append(s)

    out: list[str] = []
    did_name = False
    SECTION_TITLES = {
        "EDUCATION": "Education",
        "EXPERIENCE": "Experience",
        "TECHNICAL SKILLS": "Technical Skills",
        "ADDITIONAL": "Additional",
    }

    for i, line in enumerate(lines):
        if not line:
            out.append("")
            continue

        # First line with name and contact
        if not did_name and line.upper().startswith("RJVIR ATWAL"):
            rest = line[len("RJVIR ATWAL"):].strip()
            out.append("# RJVIR ATWAL")
            if rest:
                out.append(rest)
            out.append("")
            did_name = True
            continue

        upper = line.upper()
        if upper in SECTION_TITLES:
            out.append("")
            out.append(f"## {SECTION_TITLES[upper]}")
            out.append("")
            continue

        # Convert bullets '• ' to markdown '- '
        if line.lstrip().startswith("•"):
            out.append("- " + line.lstrip().lstrip("•").strip())
            continue

        # Heuristic: make organization/location lines subheadings
        if ("University" in line or "School of" in line) and (" – " in line or " — " in line or " - " in line):
            out.append(f"#### {line}")
            continue

        out.append(line)

    # Ensure single blank lines between blocks
    normalized = []
    prev_blank = False
    for l in out:
        if l.strip() == "":
            if not prev_blank:
                normalized.append("")
            prev_blank = True
        else:
            normalized.append(l)
            prev_blank = False

    return "\n".join(normalized).strip()


def _read_resume_markdown(md_path: Path) -> str:
    raw = md_path.read_text(encoding="utf-8", errors="ignore")
    prepared = _normalize_resume_markdown(raw)
    if markdown is None:
        return f"<pre>{prepared}</pre>"
    return markdown.markdown(prepared, extensions=["extra", "sane_lists", "tables"])  # type: ignore[attr-defined]


@app.route("/resume")
def resume():
    md_path = BASE_DIR / "Resume.md"
    if not md_path.exists():
        return render_template(
            "resume.html",
            resume_html="<p><em>Resume.md not found.</em></p>",
        )
    resume_html = _read_resume_markdown(md_path)
    return render_template("resume.html", resume_html=resume_html)


# Optional: Redirect legacy .html paths to new routes for backward compatibility
@app.route("/index.html")
def legacy_index():
    return redirect(url_for("index"), code=301)


@app.route("/about.html")
def legacy_about():
    return redirect(url_for("about"), code=301)


@app.route("/projects.html")
def legacy_projects():
    return redirect(url_for("projects"), code=301)


@app.route("/contact.html")
def legacy_contact():
    return redirect(url_for("contact"), code=301)


@app.route("/resume.html")
def legacy_resume():
    return redirect(url_for("resume"), code=301)


@app.errorhandler(404)
def not_found(e):  # noqa: ANN001
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Enable reloader and debug for local development
    app.run(debug=True)
