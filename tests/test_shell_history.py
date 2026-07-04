import tempfile
import unittest
from pathlib import Path

from collectors.shell import ShellCollector


class ShellHistoryTests(unittest.TestCase):
    def test_read_new_commands_ignores_bash_timestamp_lines(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_path = Path(tmp_dir) / ".bash_history"
            history_path.write_text(
                "#1720000000\nls\n#1720000010\npwd\n",
                encoding="utf-8",
            )

            collector = ShellCollector()
            collector.history_file = history_path

            events = collector.read_new_commands()

            self.assertEqual([event["title"] for event in events], ["ls", "pwd"])
