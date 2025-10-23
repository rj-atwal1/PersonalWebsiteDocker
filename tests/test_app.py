def test_projects_page_displays_seed_data(client):
    response = client.get("/projects")
    assert response.status_code == 200
    body = response.data.decode()
    assert "Project Portfolio" in body
    assert "4 Circles Racing Webpage" in body


def test_add_project_flow(client, dal):
    payload = {
        "title": "My Database Project",
        "description": "End-to-end workflow test.",
        "image_filename": "static/images/new-project.png",
        "repo_url": "https://example.com/repo",
        "demo_url": "https://example.com/demo",
    }
    response = client.post("/projects/new", data=payload, follow_redirects=True)
    assert response.status_code == 200
    body = response.data.decode()
    assert "Added 'My Database Project' to the project list." in body
    assert "My Database Project" in body

    titles = {project["title"] for project in dal.get_all_projects()}
    assert "My Database Project" in titles


def test_delete_project_removes_entry(client, dal):
    client.post(
        "/projects/new",
        data={
            "title": "Disposable Project",
            "description": "Project slated for removal in test.",
            "image_filename": "Disposable.png",
        },
        follow_redirects=True,
    )

    project = next(p for p in dal.get_all_projects() if p["title"] == "Disposable Project")

    response = client.post(f"/projects/delete/{project['id']}", follow_redirects=True)
    assert response.status_code == 200
    body = response.data.decode()
    assert "Project removed." in body
    assert "Disposable Project" not in body
    assert all(p["title"] != "Disposable Project" for p in dal.get_all_projects())
