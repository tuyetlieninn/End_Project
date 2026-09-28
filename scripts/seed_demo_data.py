"""Fixed demo data for the Project List screen (search / filter / pagination).

Unlike generate_projects.py (random data), this always creates the same projects,
so the final demo and the Project List test cases give predictable results:

- 45 projects "Project 001" ... "Project 045" (pagination: 20 per page)
- 8 sample projects P1 ... P8 from TestCase_ProjectList (P6 is soft-deleted)
  -> 52 visible projects, 3 pages

Usage (backend running, run from the repository root):
    python scripts/seed_demo_data.py
    python scripts/seed_demo_data.py --email you@example.com --password YourPass1
Running it again does not create duplicates.
"""
import httpx

from common import base_parser, login

SAMPLES = [
    dict(customer_name="Fintech Co", project_name="Payment App", description="Hệ thống thanh toán",
         start_date="2026-01-01", is_ongoing=True, team_size=5, total_man_month=12.5, industry="金融",
         technologies=["Python", "FastAPI"], project_types=["lab"], dev_process_phases=["design", "implementation"]),
    dict(customer_name="ABC Bank", project_name="Core Banking", description="Java migration",
         start_date="2025-01-01", end_date="2025-12-31", team_size=8, total_man_month=40, industry="金融",
         technologies=["Java", "Spring"], project_types=["offshore", "new_dev"],
         dev_process_phases=["requirements", "design"]),
    dict(customer_name="Shop Online", project_name="EC Site", start_date="2025-06-01", is_ongoing=True,
         technologies=["JavaScript", "React"], project_types=["ses"], dev_process_phases=["testing"]),
    dict(customer_name="Công ty Việt Nam", project_name="在庫管理システム", description="Quản lý kho",
         start_date="2024-01-01", end_date="2024-12-31", team_size=3, total_man_month=6, industry="物流",
         technologies=["Go"], project_types=["maintenance"], dev_process_phases=["maintenance_ops", "release"]),
    dict(customer_name="Retail 50%", project_name="Discount_Campaign", start_date="2026-02-01", is_ongoing=True,
         team_size=2, total_man_month=1, industry="小売", technologies=["python"], project_types=["ses"],
         dev_process_phases=["implementation"]),
    dict(customer_name="Deleted Co", project_name="Old System", start_date="2023-01-01", end_date="2023-06-30",
         technologies=["Python"], project_types=["lab"], dev_process_phases=["design"]),
    dict(customer_name="Many Tech Inc", project_name="Platform", start_date="2024-04-01", team_size=4,
         total_man_month=10, industry="IT",
         technologies=["Python", "React", "AWS", "Docker", "PostgreSQL", "Redis"]),
    dict(customer_name="Long Name Corp", project_name="Hệ thống quản lý " * 10, description="Mô tả dài. " * 150,
         start_date="2026-01-01", is_ongoing=True, team_size=1, total_man_month=1,
         technologies=["Java"], project_types=["lab"], dev_process_phases=["implementation"]),
]


def existing_project_names(client: httpx.Client) -> set[str]:
    names: set[str] = set()
    page = 1
    while True:
        items = client.get("/projects", params={"page": page, "page_size": 100}).json()["items"]
        if not items:
            return names
        names |= {item["project_name"] for item in items}
        page += 1


def main() -> None:
    args = base_parser(__doc__).parse_args()

    with httpx.Client(base_url=args.api, timeout=15) as client:
        login(client, args.email, args.password)
        existing = existing_project_names(client)
        created = 0

        for i in range(1, 46):
            name = f"Project {i:03d}"
            if name not in existing:
                client.post("/projects", json={"customer_name": f"Customer {i:03d}", "project_name": name,
                                               "start_date": "2026-01-01"}).raise_for_status()
                created += 1

        # P6 is soft-deleted, so it never comes back from the API: if P1 exists the samples are done
        if SAMPLES[0]["project_name"] not in existing:
            for sample in SAMPLES:
                res = client.post("/projects", json=sample)
                res.raise_for_status()
                created += 1
                if sample["customer_name"] == "Deleted Co":
                    client.delete(f"/projects/{res.json()['id']}").raise_for_status()

        total = client.get("/projects").json()["total"]
    print(f"Created {created} projects. Visible now: {total} ({-(-total // 20)} pages of 20)")
    print(f"Log in to the demo with: {args.email}")


if __name__ == "__main__":
    main()
