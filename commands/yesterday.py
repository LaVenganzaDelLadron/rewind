# commands/yesterday.py

from datetime import datetime, timedelta
from database import Database


def run():
    db = Database()

    yesterday = (
        datetime.now() - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    events = db.get_events_by_date(yesterday)

    print(f"\nRewind - {yesterday}\n")

    if not events:
        print("No events found.")
        db.close()
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