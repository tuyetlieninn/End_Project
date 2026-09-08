import csv
from io import StringIO
from typing import Any


def rows_from_csv(content: str) -> list[dict[str, Any]]:
    return list(csv.DictReader(StringIO(content)))
