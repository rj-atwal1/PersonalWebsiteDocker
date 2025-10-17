# Migration to Flask - Notes

## Accomplished
- Converted static site (in `site/`) to a Flask app (`app.py`) using Jinja2 templates
- Created `templates/` with: `base.html`, `index.html`, `about.html`, `projects.html`, `contact.html`, `resume.html`, `404.html`
- Created `static/` with `css/style.css` and `js/nav.js` (styles and script ported from `site/`)
- Implemented routes: `/`, `/about`, `/projects`, `/contact` (GET+POST), `/resume`
- Added legacy redirects: `/index.html`, `/about.html`, `/projects.html`, `/contact.html`, `/resume.html`
- Resume renders from `Resume.md` via `Markdown` lib, with light cleanup for copy artifacts
- Contact form: POST validates and flashes success placeholder; no data stored/sent
- Added `requirements.txt` and updated `README.md` with run instructions

## Remaining / Ideas
- Optionally move images from `site/images` to `static/images` and remove the `/images/<file>` route
- Add a basic test to ensure routes render (e.g., using `pytest` + `Flask` test client)
- Add 500 error page template and logging configuration
- Deploy steps (e.g., gunicorn, Procfile) if needed

## Features
### Flask templating
- Description: Shared base template with consistent header/nav/footer; pages extend base.
- Purpose: Avoid duplication and enable future dynamic content.
- Risks: None significant.
- Future: Extract nav to an include, add active-link highlighting.

### Markdown-based resume
- Description: Reads `Resume.md` and renders to HTML.
- Purpose: Keep resume as Markdown source; easy to update.
- Risks: If Markdown package missing, page falls back to preformatted text.
- Future: Cache compiled HTML; add styling for headings/lists.

### Contact POST handler (placeholder)
- Description: Validates form server-side, shows a flash message.
- Purpose: Demo server-side processing.
- Risks: None (no storage); future email integration would require secrets management.
- Future: Persist to CSV or send email via provider.
