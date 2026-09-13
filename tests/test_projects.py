import pytest

pytestmark = pytest.mark.asyncio


async def test_create_and_get_project(client, auth_headers):
    res = await client.post(
        "/projects",
        json={"customer_name": "ABC", "project_name": "Test", "start_date": "2026-01-01"},
        headers=auth_headers,
    )
    assert res.status_code == 201
    project_id = res.json()["id"]

    res2 = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert res2.status_code == 200
    assert res2.json()["customer_name"] == "ABC"


async def test_soft_delete_hides_project(client, auth_headers):
    res = await client.post(
        "/projects",
        json={"customer_name": "X", "project_name": "Y", "start_date": "2026-01-01"},
        headers=auth_headers,
    )
    project_id = res.json()["id"]

    del_res = await client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert del_res.status_code == 204

    get_res = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert get_res.status_code == 404


async def test_filter_and_search(client, auth_headers):
    await client.post(
        "/projects",
        json={
            "customer_name": "Fintech Co",
            "project_name": "Payment App",
            "start_date": "2026-01-01",
            "technologies": ["python"],
            "project_types": ["lab"],
        },
        headers=auth_headers,
    )

    res = await client.get("/projects?q=Fintech", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["total"] >= 1

    res2 = await client.get("/projects?technology=python", headers=auth_headers)
    assert res2.status_code == 200
    assert res2.json()["total"] >= 1


async def test_tech_tags_autocomplete(client, auth_headers):
    await client.post(
        "/projects",
        json={
            "customer_name": "A",
            "project_name": "B",
            "start_date": "2026-01-01",
            "technologies": ["FastAPI"],
        },
        headers=auth_headers,
    )
    res = await client.get("/tech-tags?q=fast", headers=auth_headers)
    assert res.status_code == 200
    assert "fastapi" in res.json()