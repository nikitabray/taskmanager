import re

def format_datetime(dt_string: str) -> str:
    pattern = r'(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})'
    pattern = r'(\d{2})'
    a = re.compile(pattern)
    print(a.findall("2021-12-22 21:57:12"))

format_datetime("dd")