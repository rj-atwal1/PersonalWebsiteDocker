"""Data access layer for the projects portfolio website."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Sequence

DB_PATH = Path(__file__).with_name("projects.db")
STATIC_IMAGES_DIR = Path(__file__).with_name("static") / "images"
DEFAULT_IMAGE = "project1-placeholder.png"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_filename TEXT NOT NULL,
    repo_url TEXT,
    demo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_PROJECTS: Sequence[tuple[str, str, str, str | None, str | None]] = (
    (
        "4 Circles Racing Webpage",
        "Our first full HTML site featuring navigation, CSS animations, and hover interactions.",
        "4Circles.png",
        "https://github.com/rj-atwal1/4CirclesWebsite",
        "https://ratwal.pages.iu.edu/FCRE6/index.html",
    ),
    (
        "Student Question Website",
        "A safe space for students to ask questions anonymously and improve classroom inclusion.",
        "Project 2 Screen.png",
        "https://github.com/rj-atwal1/Student-Question-Website",
        "https://ratwal.pages.iu.edu/sandbox/index.html",
    ),
    (
        "Portfolio Placeholder",
        "Use this slot for your next project. Update it or delete it once you add your own entry.",
        "project1-placeholder.png",
        None,
        None,
    ),
)


def _get_connection() -> sqlite3.Connection:
    """Return a SQLite connection configured for row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(with_seed: bool = True) -> None:
    """Create the database file and schema; optionally seed starter rows."""
    with _get_connection() as conn:
        conn.executescript(SCHEMA_SQL)
        if with_seed:
            existing = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
            if existing == 0:
                conn.executemany(
                    """
                    INSERT INTO projects (title, description, image_filename, repo_url, demo_url)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    SEED_PROJECTS,
                )
        conn.commit()


def _normalize_filename(filename: str | None) -> str:
    if not filename:
        return ""
    clean = filename.strip()
    if not clean:
        return ""
    return Path(clean).name


def _resolve_image(filename: str | None) -> str:
    """Return a valid image filename, falling back to a placeholder when needed."""
    clean = _normalize_filename(filename)
    if not clean:
        return DEFAULT_IMAGE
    candidate = STATIC_IMAGES_DIR / clean
    if candidate.exists():
        return clean
    return DEFAULT_IMAGE


def get_all_projects() -> list[dict[str, object]]:
    """Return all projects sorted from newest to oldest."""
    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, description, image_filename, repo_url, demo_url
            FROM projects
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()
        projects: list[dict[str, object]] = []
        for row in rows:
            record = dict(row)
            raw_filename = record.get("image_filename")
            record["image_filename"] = _resolve_image(raw_filename if isinstance(raw_filename, str) else None)
            projects.append(record)
        return projects


def add_project(
    title: str,
    description: str,
    image_filename: str,
    repo_url: str | None = None,
    demo_url: str | None = None,
) -> int:
    """Insert a project and return its new primary key."""
    clean_repo = repo_url.strip() if repo_url else None
    clean_demo = demo_url.strip() if demo_url else None
    normalized_image = _normalize_filename(image_filename)
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO projects (title, description, image_filename, repo_url, demo_url)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title.strip(),
                description.strip(),
                normalized_image or DEFAULT_IMAGE,
                clean_repo,
                clean_demo,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def delete_project(project_id: int) -> bool:
    """Remove a project by id. Returns True when a row is deleted."""
    with _get_connection() as conn:
        cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cursor.rowcount > 0


def add_many(projects: Iterable[tuple[str, str, str, str | None, str | None]]) -> int:
    """Bulk insert helper primarily used for tests or scripts."""
    with _get_connection() as conn:
        cursor = conn.executemany(
            """
            INSERT INTO projects (title, description, image_filename, repo_url, demo_url)
            VALUES (?, ?, ?, ?, ?)
            """,
            projects,
        )
        conn.commit()
        return cursor.rowcount


# Ensure the database exists when the module is imported so the app can rely on it.
init_db(with_seed=True)
