import httpx
import asyncio
import random
from faker import Faker
from datetime import date, timedelta

fake = Faker("ja_JP")

# ============================
# RANDOM DATE (2022 → 2026)
# ============================
def random_dates():
    start_year = random.randint(2022, 2026)
    start_month = random.randint(1, 12)
    start_day = random.randint(1, 28)
    start_date = date(start_year, start_month, start_day)

    duration_days = random.randint(30, 720)
    end_date = start_date + timedelta(days=duration_days)

    return start_date.isoformat(), end_date.isoformat()


# ============================
# CONFIG
# ============================
LOGIN_URL = "http://127.0.0.1:8000/auth/login"
PROJECT_URL = "http://127.0.0.1:8000/projects"

EMAIL = "tuyetlien0406@gmail.com" #thay bằng tk của mọi người nhé ạ
PASSWORD = "Aa1234567"

TECHS = ["react", "fastapi", "python", "aws", "docker", "typescript", "postgresql"]
PROJECT_TYPES = ["offshore", "ses", "lab", "new_dev", "maintenance"]
PHASES = ["requirements", "design", "implementation", "testing", "release", "maintenance_ops"]
INDUSTRIES = ["ITサービス", "製造業", "小売", "金融"]


# ============================
# LOGIN
# ============================
async def login():
    async with httpx.AsyncClient() as client:
        res = await client.post(LOGIN_URL, json={"email": EMAIL, "password": PASSWORD})
        return res.json()["idToken"]


# ============================
# GET ALL PROJECT IDs (ALL PAGES)
# ============================
async def get_all_project_ids(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    all_ids = []

    async with httpx.AsyncClient() as client:
        page = 1

        while True:
            res = await client.get(f"{PROJECT_URL}?page={page}&page_size=100", headers=headers)
            data = res.json()

            items = data["items"]
            if not items:
                break  # hết trang

            ids = [item["id"] for item in items]
            all_ids.extend(ids)

            print(f"Loaded page {page} → {len(ids)} projects")

            page += 1

    print(f"🎯 Total projects found: {len(all_ids)}")
    return all_ids


# ============================
# UPDATE PROJECT
# ============================
async def update_project(project_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    start_date, end_date = random_dates()

    payload = {
        "customer_name": fake.company(),
        "project_name": fake.catch_phrase(),
        "description": fake.text(),
        "start_date": start_date,
        "end_date": end_date,
        "is_ongoing": False,
        "team_size": random.randint(3, 15),
        "total_man_month": round(random.uniform(5, 50), 1),
        "source_note": fake.text(),
        "industry": random.choice(INDUSTRIES),
        "outcome_note": fake.text(),
        "team_composition_note": fake.text(),
        "technologies": random.sample(TECHS, random.randint(2, 5)),
        "project_types": random.sample(PROJECT_TYPES, random.randint(1, 2)),
        "dev_process_phases": random.sample(PHASES, random.randint(2, 5)),
    }

    async with httpx.AsyncClient() as client:
        res = await client.put(f"{PROJECT_URL}/{project_id}", json=payload, headers=headers)
        print(f"Update project {project_id} → {res.status_code}")


# ============================
# MAIN
# ============================
async def main():
    token = await login()
    ids = await get_all_project_ids(token)

    for pid in ids:
        await update_project(pid, token)

    print("🎉 DONE — All projects updated!")


asyncio.run(main())
