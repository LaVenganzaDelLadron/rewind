from datetime import date

from data.history import History


def show_today():
    history = History()
    commands = history.get_commands_for_day(date.today())

    print(f"Commands run on {date.today().isoformat()}:")
    if not commands:
        print("No commands found for today.")
        return

    for index, command in enumerate(commands, start=1):
        print(f"{index}. {command}")