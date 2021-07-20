import re


def format_time(time: str):
    am_pm = "AM"
    time_hours = int(time[:2])
    time_minutes = int(time[3:])
    if time_hours >= 12:
        time_hours -= 12
        am_pm = "PM"
    if len(str(time_hours)) == 1:
        time_hours = f"0{time_hours}"
    if len(str(time_minutes)) == 1:
        time_minutes = f"0{time_minutes}"
    return f"{time_hours}:{time_minutes} {am_pm}"


def check_if_offset_or_api(string: str):
    pattern = r'^[+\-]+\d+:\d+$'
    if re.match(pattern, string):
        return True
    else:
        return False
