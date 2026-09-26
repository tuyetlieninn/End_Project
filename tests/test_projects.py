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


@pytest.mark.parametrize(
    "payload",
    [
        {"customer_name": "ABC", "project_name": "Test", "start_date": "abc"},
        {
            "customer_name": "ABC",
            "project_name": "Test",
            "start_date": "2026-05-01",
            "end_date": "2026-01-01",
        },
        {
            "customer_name": "ABC",
            "project_name": "Test",
            "start_date": "2026-05-01",
            "end_date": "2026-06-01",
            "is_ongoing": True,
        },
    ],
)
async def test_create_rejects_invalid_project_period(client, auth_headers, payload):
    response = await client.post("/projects", json=payload, headers=auth_headers)
    assert response.status_code == 422


async def test_create_normalizes_and_deduplicates_technologies(client, auth_headers):
    response = await client.post(
        "/projects",
        json={
            "customer_name": "ABC",
            "project_name": "Test",
            "start_date": "2026-01-01",
            "technologies": [" Python ", "python", "FastAPI"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["technologies"] == ["python", "fastapi"]


async def test_get_missing_project_returns_404(client, auth_headers):
    response = await client.get("/projects/999999", headers=auth_headers)
    assert response.status_code == 404


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


async def create_project(client, auth_headers, **fields):
    payload = {"customer_name": "Customer", "project_name": "Project", "start_date": "2026-01-01"}
    payload.update(fields)
    response = await client.post("/projects", json=payload, headers=auth_headers)
    assert response.status_code == 201
    return response.json()


@pytest.mark.parametrize("start_date", ["2026-W01-1", "20260101", "2026-02-30", "２０２６-０１-０１"])
async def test_create_rejects_non_calendar_date_formats(client, auth_headers, start_date):
    response = await client.post(
        "/projects",
        json={"customer_name": "ABC", "project_name": "Test", "start_date": start_date},
        headers=auth_headers,
    )
    assert response.status_code == 422


async def test_update_rejects_end_date_before_start_date(client, auth_headers):
    project = await create_project(client, auth_headers)
    response = await client.put(
        f"/projects/{project['id']}",
        json={
            "customer_name": "Customer",
            "project_name": "Project",
            "start_date": "2026-05-01",
            "end_date": "2026-01-01",
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    ("keyword", "expected"),
    [("%", ["Retail 50%"]), ("_", ["Discount_Campaign"]), ("\\", ["Path C:\\temp"])],
)
async def test_search_treats_like_wildcards_as_literal_characters(
    client, auth_headers, keyword, expected
):
    for name in ("Retail 50%", "Discount_Campaign", "Path C:\\temp", "Plain Name"):
        await create_project(client, auth_headers, customer_name=name)

    response = await client.get("/projects", params={"q": keyword}, headers=auth_headers)

    assert [item["customer_name"] for item in response.json()["items"]] == expected


async def test_technology_filter_matches_whole_tag_only(client, auth_headers):
    await create_project(client, auth_headers, project_name="Java", technologies=["java", "spring"])
    await create_project(client, auth_headers, project_name="JS", technologies=["javascript"])

    response = await client.get("/projects?technology=java", headers=auth_headers)
    assert [item["project_name"] for item in response.json()["items"]] == ["Java"]

    response = await client.get("/projects?technology=JAVA&technology=react", headers=auth_headers)
    assert [item["project_name"] for item in response.json()["items"]] == ["Java"]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("project_type=a", []),
        ("project_type=lab", ["Lab"]),
        ("dev_process_phase=maintenance", []),
        ("dev_process_phase=maintenance_ops", ["Ops"]),
        ("technology=java,spring", []),
    ],
)
async def test_type_and_phase_filters_match_whole_code_only(client, auth_headers, query, expected):
    await create_project(
        client,
        auth_headers,
        project_name="Lab",
        project_types=["lab"],
        technologies=["java", "spring"],
    )
    await create_project(
        client, auth_headers, project_name="Ops", dev_process_phases=["maintenance_ops"]
    )

    response = await client.get(f"/projects?{query}", headers=auth_headers)

    assert [item["project_name"] for item in response.json()["items"]] == expected


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
