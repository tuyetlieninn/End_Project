def list_to_csv(items: list[str]) -> str:
    # Nối mảng thành chuỗi CSV, VD: ["React","Node.js"] -> "React,Node.js"
    return ",".join(items) if items else ""


def csv_to_list(csv_str: str) -> list[str]:
    # Chuyển ngược lại: "React,Node.js" -> ["React","Node.js"]
    if not csv_str:
        return []
    return csv_str.split(",")