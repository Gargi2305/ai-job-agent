import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "JobPilot"

_sheet = None
_seen_cache = None  # 🔥 cache


def get_sheet():
    global _sheet
    if _sheet:
        return _sheet

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    client = gspread.authorize(creds)

    _sheet = client.open(SHEET_NAME).sheet1
    return _sheet


def load_seen_jobs():
    global _seen_cache

    if _seen_cache is not None:
        return _seen_cache  # 🔥 use cache

    sheet = get_sheet()
    records = sheet.get_all_records()

    seen = set()
    for r in records:
        title = r.get("Title") or r.get("title")
        company = r.get("Company") or r.get("company")

        if title and company:
            key = f"{title}_{company}"
            seen.add(key)

    _seen_cache = seen
    return seen


def save_job(job):
    global _seen_cache

    seen = load_seen_jobs()
    key = f"{job['title']}_{job['company']}"

    if key in seen:
        return

    sheet = get_sheet()

    sheet.append_row([
        job.get("title"),
        job.get("company"),
        job.get("score"),
        job.get("link"),
        (job.get("description") or "")[:300]
    ])

    # 🔥 update cache immediately (no re-read needed)
    seen.add(key)