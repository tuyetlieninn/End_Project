<<<<<<< HEAD
def list_to_csv(items: list[str]) -> str:
    # Nối mảng thành chuỗi CSV, VD: ["React","Node.js"] -> "React,Node.js"
    return ",".join(items) if items else ""


def csv_to_list(csv_str: str) -> list[str]:
    # Chuyển ngược lại: "React,Node.js" -> ["React","Node.js"]
    if not csv_str:
        return []
    return csv_str.split(",")
=======
import csv
from io import StringIO
from typing import Any


def rows_from_csv(content: str) -> list[dict[str, Any]]:
    return list(csv.DictReader(StringIO(content)))


def list_to_csv(values: list[str]) -> str:
    return ",".join(value.strip() for value in values if value.strip())


def csv_to_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
