import importlib
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def test_env(tmp_path, monkeypatch):
    """Prepare an isolated database and image directory for each test."""
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    project_db = tmp_path / "projects.db"

    placeholder_src = Path(__file__).resolve().parent.parent / "static" / "images" / "project1-placeholder.png"
    if placeholder_src.exists():
        shutil.copy(placeholder_src, images_dir / "project1-placeholder.png")
    else:
        (images_dir / "project1-placeholder.png").write_bytes(b"")

    monkeypatch.setenv("PROJECTS_DB_PATH", str(project_db))
    monkeypatch.setenv("STATIC_IMAGES_DIR", str(images_dir))

    import DAL
    import app as app_module

    dal_module = importlib.reload(DAL)
    app_module = importlib.reload(app_module)

    dal_module.init_db(with_seed=True)

    app_module.app.config.update(TESTING=True, SECRET_KEY="test-key")
    return app_module.app, dal_module


@pytest.fixture()
def client(test_env):
    app_obj, _ = test_env
    with app_obj.test_client() as client:
        yield client


@pytest.fixture()
def dal(test_env):
    _, dal_module = test_env
    return dal_module
