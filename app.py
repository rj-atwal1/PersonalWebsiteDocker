from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from DAL import add_project, delete_project, get_all_projects, init_db

try:
    import markdown  # type: ignore
except Exception:  # pragma: no cover - handled by requirements
    markdown = None  # type: ignore[assignment]

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

# Ensure database schema exists before serving requests.
init_db(with_seed=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    project_rows = get_all_projects()
    return render_template("projects.html", projects=project_rows)


@app.route("/projects/new", methods=["GET", "POST"])
@app.route("/add", methods=["GET", "POST"])
@app.route("/contact", methods=["GET", "POST"])
def project_form():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        image_filename = request.form.get("image_filename", "").strip()
        repo_url = request.form.get("repo_url", "").strip() or None
        demo_url = request.form.get("demo_url", "").strip() or None

        errors: list[str] = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not image_filename:
            errors.append("Image file name is required. Upload the image into static/images first.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("project_form.html")

        add_project(title, description, image_filename, repo_url, demo_url)
        flash(f"Added '{title}' to the project list.", "success")
        return redirect(url_for("projects"))

    return render_template("project_form.html")


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project_view(project_id: int):
    removed = delete_project(project_id)
    if removed:
        flash("Project removed.", "success")
    else:
        flash("Project could not be deleted. It may have already been removed.", "error")
    return redirect(url_for("projects"))


def _normalize_resume_markdown(text: str) -> str:
    """Heuristics to convert plain text resume into better Markdown."""
    lines = []
    for raw in text.splitlines():
        s = raw.strip()
        if s in {"1", "Automatic Zoom"}:
            continue
        lines.append(s)

    out: list[str] = []
    did_name = False
    section_titles = {
        "EDUCATION": "Education",
        "EXPERIENCE": "Experience",
        "TECHNICAL SKILLS": "Technical Skills",
        "ADDITIONAL": "Additional",
    }

    for line in lines:
        if not line:
            out.append("")
            continue
        if not did_name and line.upper().startswith("RJVIR ATWAL"):
            rest = line[len("RJVIR ATWAL"):].strip()
            out.append("# RJVIR ATWAL")
            if rest:
                out.append(rest)
            out.append("")
            did_name = True
            continue
        upper = line.upper()
        if upper in section_titles:
            out.extend(["", f"## {section_titles[upper]}", ""])
            continue
        if line.lstrip().startswith("•"):
            out.append("- " + line.lstrip().lstrip("•").strip())
            continue
        if ("University" in line or "School of" in line) and (" – " in line or " — " in line or " - " in line):
            out.append(f"#### {line}")
            continue
        out.append(line)

    normalized: list[str] = []
    prev_blank = False
    for line in out:
        if not line.strip():
            if not prev_blank:
                normalized.append("")
            prev_blank = True
        else:
            normalized.append(line)
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
        return render_template("resume.html", resume_html="<p><em>Resume.md not found.</em></p>")
    resume_html = _read_resume_markdown(md_path)
    return render_template("resume.html", resume_html=resume_html)


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
    return redirect(url_for("project_form"), code=301)


@app.route("/resume.html")
def legacy_resume():
    return redirect(url_for("resume"), code=301)


@app.errorhandler(404)
def not_found(error: Exception):  # noqa: ANN001
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
