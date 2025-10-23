Personal Website (Flask)

This repository contains a Flask-based version of the personal website. It mirrors the previous static pages and adds a small server-side contact form handler and Markdown rendering for the resume.

Structure
- app.py: Flask app and routes
- templates/: Jinja2 templates (base, index, about, projects, contact, resume, 404)
- static/
	- css/style.css
	- js/nav.js
	- images/: Placeholder folder. Existing images are served directly from `site/images` via the `/images/<file>` route for now.
- site/: Original static site (left as an archive)
- Resume.md: Markdown source for resume

Quick start (macOS, zsh)

1) Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the app (development)

```bash
flask --app app.py run --debug
```

Then open http://127.0.0.1:5000.

Notes
- Resume is rendered from `Resume.md` using the `Markdown` package. If `Markdown` isn't installed, the page will show a plain-text fallback.
- Contact form is a placeholder: it validates input and shows a success message; it doesn't send email or store submissions.
- Old `*.html` paths redirect to their new Flask routes for backward compatibility.

Next steps
- Move images from `site/images` to `static/images` and update the image route if you prefer all assets under `static/`.
- Add tests or CI workflow if needed.

