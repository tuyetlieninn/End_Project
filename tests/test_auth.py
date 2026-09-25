import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.session import get_db
from app.main import app

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "password",
    [
        "Aa1" + "x" * 77,  # 80 ASCII characters
        "Aa1" + "パ" * 30,  # 33 characters, 93 bytes in UTF-8
    ],
)
async def test_register_rejects_password_over_72_bytes(client, password):
    res = await client.post("/auth/register", json={"email": "long@vnext.vn", "password": password})
    assert res.status_code == 422
    assert "72 bytes" in res.text


async def test_register_and_login_with_exactly_72_byte_password(client):
    password = "Aa1" + "x" * 69
    res = await client.post("/auth/register", json={"email": "max@vnext.vn", "password": password})
    assert res.status_code == 201

    res = await client.post("/auth/login", json={"email": "max@vnext.vn", "password": password})
    assert res.status_code == 200


async def test_login_with_overlong_password_returns_401(client):
    await client.post("/auth/register", json={"email": "c@vnext.vn", "password": "Password123"})
    res = await client.post("/auth/login", json={"email": "c@vnext.vn", "password": "A" * 200})
    assert res.status_code == 401


async def test_health_reports_ok_when_tables_exist(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "db": "ok"}


async def test_health_reports_error_when_database_is_not_migrated(client):
    engine = create_async_engine("sqlite+aiosqlite://")  # empty in-memory DB, no tables
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def empty_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = empty_db
    try:
        res = await client.get("/health")
    finally:
        await engine.dispose()

    assert res.status_code == 503
    assert res.json() == {"status": "error", "db": "error"}


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


async def test_tech_tag_is_normalized_and_blank_is_rejected(client, auth_headers):
    created = await client.post("/tech-tags", json={"name": " Python "}, headers=auth_headers)
    assert created.status_code == 201
    assert created.json()["name"] == "python"

    blank = await client.post("/tech-tags", json={"name": "   "}, headers=auth_headers)
    assert blank.status_code == 422