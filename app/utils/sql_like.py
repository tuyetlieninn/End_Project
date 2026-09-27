LIKE_ESCAPE = "\\"


def escape_like(value: str) -> str:
    """Escape SQL LIKE wildcards so user input is matched literally."""
    return (
        value.replace(LIKE_ESCAPE, LIKE_ESCAPE * 2)
        .replace("%", LIKE_ESCAPE + "%")
        .replace("_", LIKE_ESCAPE + "_")
    )
