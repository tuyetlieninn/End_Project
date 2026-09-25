import pytest

pytestmark = pytest.mark.asyncio


async def test_register_success(client):
    res = await client.post("/auth/register", json={"email": "a@vnext.vn", "password": "Password123"})
    assert res.status_code == 201
    assert "idToken" in res.json()


async def test_register_duplicate_email_returns_409(client):
    await client.post("/auth/register", json={"email": "dup@vnext.vn", "password": "Password123"})
    res = await client.post("/auth/register", json={"email": "dup@vnext.vn", "password": "Password123"})
    assert res.status_code == 409


async def test_login_wrong_password_returns_401(client):
    await client.post("/auth/register", json={"email": "b@vnext.vn", "password": "Password123"})
    res = await client.post("/auth/login", json={"email": "b@vnext.vn", "password": "WrongPass1"})
    assert res.status_code == 401


async def test_projects_without_token_returns_401(client):
    res = await client.get("/projects")
    assert res.status_code == 401


async def test_duplicate_tech_tag_returns_409(client, auth_headers):
    first = await client.post("/tech-tags", json={"name": "python"}, headers=auth_headers)
    assert first.status_code == 201

    duplicate = await client.post("/tech-tags", json={"name": "Python"}, headers=auth_headers)
    assert duplicate.status_code == 409