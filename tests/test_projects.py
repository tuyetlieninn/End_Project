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


async def test_projects_pagination_returns_correct_page_and_filtered_total(client, auth_headers):
    for index in range(5):
        response = await client.post(
            "/projects",
            json={
                "customer_name": "Pagination Customer",
                "project_name": f"Pagination Project {index + 1}",
                "start_date": "2026-01-01",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201

    # This project must not be included in the filtered count.
    await client.post(
        "/projects",
        json={
            "customer_name": "Other Customer",
            "project_name": "Unrelated Project",
            "start_date": "2026-01-01",
        },
        headers=auth_headers,
    )

    response = await client.get(
        "/projects?q=Pagination&page=2&page_size=2", headers=auth_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"items", "total", "page", "page_size"}
    assert body["total"] == 5
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert [item["project_name"] for item in body["items"]] == [
        "Pagination Project 3",
        "Pagination Project 4",
    ]


async def test_projects_pagination_uses_default_page_and_page_size(client, auth_headers):
    response = await client.get("/projects", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 1
    assert body["page_size"] == 20


@pytest.mark.parametrize(
    ("query", "invalid_field"),
    [
        ("page=0", "page"),
        ("page=-1", "page"),
        ("page=not-a-number", "page"),
        ("page_size=0", "page_size"),
        ("page_size=-1", "page_size"),
        ("page_size=101", "page_size"),
        ("page_size=not-a-number", "page_size"),
    ],
)
async def test_projects_pagination_rejects_invalid_query_parameters(
    client, auth_headers, query, invalid_field
):
    response = await client.get(f"/projects?{query}", headers=auth_headers)

    assert response.status_code == 422
    assert any(error["loc"][-1] == invalid_field for error in response.json()["detail"])


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
