def list_to_csv(values: list[str]) -> str:
    return ",".join(value.strip() for value in values if value.strip())


def csv_to_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]