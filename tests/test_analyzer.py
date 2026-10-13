import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.analyzer import analyze_log


class TestLogAnalyzer(unittest.TestCase):

    def run_analyzer(self, content):
        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / "test.log"
            log_path.write_text(content, encoding="utf-8")

            with patch("builtins.print") as mocked_print:
                result = analyze_log(log_path)

            output = "\n".join(
                str(call.args[0]) for call in mocked_print.call_args_list
            )
            return result, output

    def test_alert_after_five_failures(self):
        content = "".join(
            f"LOGIN_FAILED ip=192.0.2.10 user=user{i}\n"
            for i in range(5)
        )
        result, output = self.run_analyzer(content)

        self.assertEqual(result, 0)
        self.assertIn("[ALERTE] 192.0.2.10 : 5", output)

    def test_no_alert_below_threshold(self):
        content = (
            "LOGIN_FAILED ip=192.0.2.20 user=alice\n"
            "LOGIN_FAILED ip=192.0.2.20 user=bob\n"
        )
        result, output = self.run_analyzer(content)

        self.assertEqual(result, 0)
        self.assertIn("[OK]", output)
        self.assertNotIn("[ALERTE]", output)

    def test_successful_login_is_ignored(self):
        content = "LOGIN_SUCCESS ip=192.0.2.30 user=alice\n"
        result, output = self.run_analyzer(content)

        self.assertEqual(result, 0)
        self.assertIn("Échecs analysés : 0", output)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.log"

            with patch("builtins.print") as mocked_print:
                result = analyze_log(missing_path)

        self.assertEqual(result, 2)
        self.assertIn("[ERROR]", str(mocked_print.call_args))


if __name__ == "__main__":
    unittest.main()
