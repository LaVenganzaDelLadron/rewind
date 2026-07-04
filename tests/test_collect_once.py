import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database import Database


class CollectOnceTests(unittest.TestCase):
    def test_collect_once_imports_existing_pacman_history(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            pacman_log = tmp_path / "pacman.log"
            pacman_log.write_text(
                "[2026-07-04T10:00:00+0800] [PACMAN] Running 'pacman -S foo'\n"
                "[2026-07-04T10:00:01+0800] [ALPM] installed foo (1.0-1)\n",
                encoding="utf-8",
            )
            db_path = tmp_path / "rewind.db"
            state_path = tmp_path / "rewind-state.json"

            with patch("collectors.packages.PACMAN_LOG", str(pacman_log)), patch(
                "database.DB_PATH", db_path
            ):
                import collectors.collect as collect_module

                collect_module = importlib.reload(collect_module)
                collect_module.collect_once(state_path=state_path)

                db = Database()
                try:
                    events = db.get_all_events()
                    self.assertTrue(
                        any(
                            event[2] == "package" and event[3] == "Installed foo"
                            for event in events
                        )
                    )
                finally:
                    db.close()

    def test_collect_once_does_not_duplicate_existing_events_on_second_run(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            pacman_log = tmp_path / "pacman.log"
            pacman_log.write_text(
                "[2026-07-04T10:00:00+0800] [PACMAN] Running 'pacman -S foo'\n"
                "[2026-07-04T10:00:01+0800] [ALPM] installed foo (1.0-1)\n",
                encoding="utf-8",
            )
            db_path = tmp_path / "rewind.db"
            state_path = tmp_path / "rewind-state.json"

            with patch("collectors.packages.PACMAN_LOG", str(pacman_log)), patch(
                "database.DB_PATH", db_path
            ):
                import collectors.collect as collect_module

                collect_module = importlib.reload(collect_module)
                collect_module.collect_once(state_path=state_path)
                collect_module.collect_once(state_path=state_path)

                db = Database()
                try:
                    events = db.get_all_events()
                    self.assertEqual(
                        sum(
                            1
                            for event in events
                            if event[2] == "package" and event[3] == "Installed foo"
                        ),
                        1,
                    )
                finally:
                    db.close()
