def list_to_csv(values: list[str]) -> str:
    # Nối mảng thành chuỗi CSV, tự loại khoảng trắng thừa mỗi phần tử
    return ",".join(value.strip() for value in values if value.strip())


def csv_to_list(value: str) -> list[str]:
    # Chuyển ngược lại, cũng tự loại khoảng trắng thừa
    return [item.strip() for item in value.split(",") if item.strip()]