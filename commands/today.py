# commands/today.py
from datetime import datetime
from database import Database


def run():
    db = Database()

    today = datetime.now().strftime("%Y-%m-%d")

    events = db.get_events_by_date(today)

    print(f"\nRewind - {today}\n")

    if not events:
        print("No events found.")
        return

    for timestamp, category, title, details in events:
        time_only = timestamp.split()[1]

        print(
            f"[{time_only}] "
            f"[{category.upper()}] "
            f"{title}"
        )

        if details:
            print(f"    {details}")

    db.close()