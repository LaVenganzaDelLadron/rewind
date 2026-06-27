# commands/stats.py

from database import Database


def run():
    db = Database()

    cursor = db.cursor

    # Total events
    cursor.execute("""
        SELECT COUNT(*)
        FROM events
    """)

    total = cursor.fetchone()[0]

    print("\nRewind Statistics\n")
    print(f"Total events: {total}\n")

    # Events per category
    print("By category:")

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM events
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)

    rows = cursor.fetchall()

    for category, count in rows:
        print(f"{category.upper():15} {count}")

    # Most active day
    cursor.execute("""
        SELECT DATE(timestamp), COUNT(*)
        FROM events
        GROUP BY DATE(timestamp)
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    if result:
        date, count = result

        print("\nMost active day:")
        print(f"{date} ({count} events)")

    db.close()