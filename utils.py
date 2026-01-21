from datetime import datetime


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def year_from_date(date_str):
    if not date_str:
        return 0
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").year
    except ValueError:
        return 0


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def ascii_bar(value, max_value=100, width=20):
    if max_value <= 0:
        max_value = 1
    ratio = min(max(value / max_value, 0), 1)
    filled = int(width * ratio)
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]" + f" {value:.1f}"
