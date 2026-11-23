"""Tests for scripts/srs.py. Run with a Python that has fsrs>=6,<7:

    python -m unittest discover -s tests -v
"""

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

SRS = Path(__file__).resolve().parent.parent / "skills" / "learn-anything" / "scripts" / "srs.py"


def t(day, hour=9, minute=0):
    return f"2026-01-{day:02d}T{hour:02d}:{minute:02d}:00+00:00"


def run(*args):
    return subprocess.run([sys.executable, "-I", str(SRS), *map(str, args)],
                          capture_output=True, text=True)


def ok(*args):
    r = run(*args)
    assert r.returncode == 0, r.stderr
    return r.stdout


def answer(d, now, grade, item="s.know.x", question="q", rung="L5"):
    out = ok("answer", d, "--item", item, "--grade", grade, "--confidence", 2,
             "--rung", rung, "--question", question, "--response", "r", "--now", now)
    return datetime.fromisoformat(out.split("next due ")[1].strip())


def parts(d, now=t(28)):
    """`show` part table as {part: [level, passes, spaced, best_rung, failed]}."""
    lines = ok("show", d, "--now", now).splitlines()
    i = next(n for n, l in enumerate(lines) if l.startswith("part\t"))
    j = next(n for n, l in enumerate(lines) if l.startswith("item\t"))
    return {l.split("\t")[0]: l.split("\t")[1:] for l in lines[i + 1:j]}


class SrsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_failed_review_is_due_before_passed_review(self):
        with tempfile.TemporaryDirectory() as other:
            t1 = answer(self.d, t(1), 3)
            self.assertEqual(t1, answer(other, t(1), 3))
            due_fail = answer(self.d, t1.isoformat(), 1)
            due_pass = answer(other, t1.isoformat(), 3)
        self.assertLess(due_fail, due_pass)
        print(f"proved: grade 1 is due {due_fail}, grade 3 is due {due_pass}")

    def test_due_lists_only_past_due_items_with_last_question(self):
        answer(self.d, t(1), 3, item="s.know.early", question="first?")
        late = answer(self.d, t(1), 4, item="s.know.late")
        self.assertEqual(ok("due", self.d, "--now", t(1)), "")
        rows = [l.split("\t") for l in ok("due", self.d, "--now", "2027-01-01T00:00Z").splitlines()]
        self.assertEqual([r[0] for r in rows], ["s.know.early", "s.know.late"])
        self.assertEqual(rows[0][2], "first?")
        self.assertIn("s.know.late", ok("due", self.d, "--now", late.isoformat()))

    def test_answer_right_after_teaching_is_not_spaced(self):
        ok("taught", self.d, "--part", "s.know", "--now", t(1))
        answer(self.d, t(1, 9, 5), 3, question="a")       # straight after teaching
        self.assertEqual(parts(self.d)["s.know"][1:3], ["1", "0"])
        ok("taught", self.d, "--part", "o.know", "--now", t(1, 9, 6))
        answer(self.d, t(1, 9, 7), 3, item="o.know.y")     # another part in between
        answer(self.d, t(1, 9, 8), 3, question="b")
        self.assertEqual(parts(self.d)["s.know"][1:3], ["2", "1"])
        answer(self.d, t(1, 11), 3, question="c", item="s.know.z")  # 1 h+ later
        self.assertEqual(parts(self.d)["s.know"][1:3], ["3", "2"])

    def test_level_change_resets_evidence(self):
        answer(self.d, t(1), 3, question="a", rung="L2")
        answer(self.d, t(2), 4, question="b", rung="L5")
        answer(self.d, t(3), 3, question="b", rung="L5")  # same question: no new pass
        self.assertEqual(parts(self.d)["s.know"], ["-", "2", "2", "L2", "no"])
        ok("level", self.d, "--part", "s.know", "--to", 3, "--reason", "two passes", "--now", t(3))
        self.assertEqual(parts(self.d)["s.know"], ["3", "0", "0", "-", "no"])

    def test_failed_due_review_is_flagged(self):
        due = answer(self.d, t(1), 3)
        answer(self.d, due.isoformat(), 3)
        self.assertEqual(parts(self.d)["s.know"][4], "no")
        answer(self.d, t(27), 1)
        self.assertEqual(parts(self.d)["s.know"][4], "yes")

    def test_success_rate_counts_last_ten(self):
        for i in range(12):
            answer(self.d, t(1, 9, i), 1 if i < 4 else 3, question=str(i))
        self.assertIn("8/10", ok("show", self.d, "--now", t(2)))

    def test_bad_input_exits_2(self):
        good = '{"ts": "%s", "kind": "answer", "item": "s.know.x", "grade": 3, "question": "q", "rung": "L5"}' % t(2)
        cases = {
            "not json": ("x\n", ["due", self.d]),
            "missing question": (good.replace('"question": "q", ', "") + "\n", ["show", self.d]),
            "grade true": (good.replace('"grade": 3', '"grade": true') + "\n", ["show", self.d]),
            "item not a string": (good.replace('"s.know.x"', "[1]") + "\n", ["show", self.d]),
            "part not know/do": (good.replace("s.know.x", "s.see.x") + "\n", ["show", self.d]),
            "rows out of order": (good + "\n" + good.replace(t(2), t(1)) + "\n", ["show", self.d]),
            "back-dated answer": (good + "\n", ["answer", self.d, "--item", "s.know.x", "--grade", 3,
                                                 "--confidence", 1, "--rung", "L1", "--question", "q",
                                                 "--response", "r", "--now", t(1)]),
            "naive --now": ("", ["due", self.d, "--now", "2026-01-01T09:00:00"]),
            "missing dir": ("", ["due", self.d + "/nope"]),
            "grade 5": ("", ["answer", self.d, "--item", "s.know.x", "--grade", 5, "--confidence", 1,
                             "--rung", "L1", "--question", "q", "--response", "r"]),
            "bad level part": ("", ["level", self.d, "--part", "s", "--to", 2, "--reason", "r"]),
        }
        for name, (content, args) in cases.items():
            with self.subTest(name):
                (Path(self.d) / "log.jsonl").write_text(content)
                r = run(*args)
                self.assertEqual(r.returncode, 2, f"{name}: {r.stderr}")
                self.assertNotIn("Traceback", r.stderr, name)
        print(f"proved: {len(cases)} bad inputs each exit 2 without a traceback")

    def test_log_row_round_trips_and_z_suffix_parses(self):
        answer(self.d, "2026-01-01T09:00:00Z", 2)
        row = json.loads((Path(self.d) / "log.jsonl").read_text())
        self.assertEqual((row["kind"], row["grade"], row["rung"], row["ts"]),
                         ("answer", 2, "L5", t(1)))
        self.assertNotIn("next_due", row)


if __name__ == "__main__":
    unittest.main()
