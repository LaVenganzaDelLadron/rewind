# commands/search.py

from database import Database


def run(keyword):
    db = Database()

    results = db.search_events(keyword)

    print(f"\nResults for: {keyword}\n")

    if not results:
        print("No matching events found.")
        db.close()
        return

    for timestamp, category, title, details in results:
        print(
            f"{timestamp} "
            f"[{category.upper()}] "
            f"{title}"
        )

        if details:
            print(f"    {details}")

    db.close()