def gtfs_time_to_minutes(time_str):
    """
    Convert GTFS time (HH:MM:SS) to minutes since midnight.
    Supports times > 24:00:00.
    """
    h, m, s = map(int, time_str.split(":"))
    return h * 60 + m + s / 60

def normalize_gtfs_time(t: str) -> int:
    """25:30:00 → 1530"""
    h, m, s = map(int, t.split(":"))
    return (h % 24) * 60 + m + s / 60