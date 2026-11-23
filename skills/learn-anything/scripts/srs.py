#!/usr/bin/env python3
"""Review log and FSRS schedule for the learn-anything skill.

    srs.py answer DIR --item SUBSKILL.PART.CONCEPT --grade 1-4 --confidence 1-3
                      --rung L1-L5 --question TEXT --response TEXT
    srs.py taught DIR --part SUBSKILL.PART
    srs.py level  DIR --part SUBSKILL.PART --to 0-5 --reason TEXT
    srs.py due    DIR
    srs.py show   DIR

Every command takes --now ISO8601 (default: the current time).
DIR/log.jsonl is append-only, in time order, and is the only state: schedules
and level evidence are replayed from it. Grades map to FSRS ratings
1 Again, 2 Hard, 3 Good, 4 Easy. Times print in local time.
Exit status: 0 ok, 2 bad input or malformed log.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NoReturn

from fsrs import Card, Rating, Scheduler

PARTS = ("know", "do")
RUNGS = ("L1", "L2", "L3", "L4", "L5")
SPACING = timedelta(hours=1)


def die(msg) -> NoReturn:
    print(f"srs.py: {msg}", file=sys.stderr)
    sys.exit(2)


def parse_time(text):
    t = datetime.fromisoformat(text.replace("Z", "+00:00"))  # 3.10 rejects "Z"
    if t.tzinfo is None:
        raise ValueError(f"timestamp without a timezone: {text}")
    return t.astimezone(timezone.utc)


def local(t):
    return t.astimezone().isoformat(timespec="minutes")


def check_part(part):
    if not isinstance(part, str) or part.count(".") != 1 or part.split(".")[1] not in PARTS:
        raise ValueError(f"part must be SUBSKILL.know or SUBSKILL.do: {part!r}")


def part_of(item):
    if not isinstance(item, str) or item.count(".") < 2:
        raise ValueError(f"item must be SUBSKILL.PART.CONCEPT: {item!r}")
    part = ".".join(item.split(".")[:2])
    check_part(part)
    return part


def is_int(x, lo, hi):
    return type(x) is int and lo <= x <= hi  # bool is not a grade


def validate(row):
    if not isinstance(row, dict):
        raise TypeError("row is not a JSON object")
    row["ts"] = parse_time(row["ts"])
    kind = row["kind"]
    if kind == "answer":
        row["part"] = part_of(row["item"])
        if not is_int(row["grade"], 1, 4):
            raise ValueError("grade must be an integer 1-4")
        if not isinstance(row["question"], str) or row.get("rung") not in RUNGS:
            raise ValueError("question must be text and rung one of L1-L5")
    elif kind == "taught":
        check_part(row["part"])
    elif kind == "level":
        check_part(row["part"])
        if not is_int(row["level"], 0, 5):
            raise ValueError("level must be an integer 0-5")
    else:
        raise ValueError(f"unknown kind {kind!r}")
    return row



def read_log(path):
    rows = []
    if not path.exists():
        return rows
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = validate(json.loads(line))
            if rows and row["ts"] < rows[-1]["ts"]:
                raise ValueError("row is older than the row before it")
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            die(f"{path}:{n}: malformed row: {e}")
        rows.append(row)
    return rows


def replay(rows):
    """Schedule every item; mark each answer `review` (was due) and `spaced`.

    An answer is spaced (unprompted recall) when its part was never taught, or
    another part was answered after the last teaching, or SPACING has passed.
    """
    scheduler = Scheduler(enable_fuzzing=False)
    cards, taught, cleared = {}, {}, set()
    for row in rows:
        if row["kind"] == "taught":
            taught[row["part"]] = row["ts"]
            cleared.discard(row["part"])
        elif row["kind"] == "answer":
            p, item = row["part"], row["item"]
            row["spaced"] = (p not in taught or p in cleared
                             or row["ts"] - taught[p] >= SPACING)
            row["review"] = item in cards and cards[item].due <= row["ts"]
            cards[item], _ = scheduler.review_card(
                cards.get(item) or Card(), Rating(row["grade"]), review_datetime=row["ts"])
            cleared.update(q for q in taught if q != p)
    return cards


def show(rows, cards):
    answers = [r for r in rows if r["kind"] == "answer"]
    recent = answers[-10:]
    if recent:
        ok = sum(r["grade"] >= 3 for r in recent)
        print(f"success (grade >= 3) in last {len(recent)} answers: {ok}/{len(recent)}")
    print("part\tlevel\tpasses\tspaced_passes\tbest_rung\tfailed_due_review")
    for p in sorted({r["part"] for r in rows if r["kind"] != "taught"}):
        level, since = "-", []
        for r in rows:
            if r["part"] != p:
                continue
            if r["kind"] == "level":
                level, since = r["level"], []
            elif r["kind"] == "answer":
                since.append(r)
        passed = [r for r in since if r["grade"] >= 3]
        passes = len({r["question"] for r in passed})
        spaced = len({r["question"] for r in passed if r["spaced"]})
        best = min((r["rung"] for r in passed), default="-")
        failed = any(r["review"] and r["grade"] == 1 for r in since)
        print(f"{p}\t{level}\t{passes}\t{spaced}\t{best}\t{'yes' if failed else 'no'}")
    print("item\tgrades\tnext_due\tlast_question")
    for item in sorted(cards):
        mine = [r for r in answers if r["item"] == item]
        grades = "".join(str(r["grade"]) for r in mine)
        print(f"{item}\t{grades}\t{local(cards[item].due)}\t{mine[-1]['question']}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    cmds = {name: sub.add_parser(name) for name in ("answer", "taught", "level", "due", "show")}
    for s in cmds.values():
        s.add_argument("dir", type=Path)
        s.add_argument("--now", help="ISO 8601 time with timezone (default: now)")
    a_ = cmds["answer"]
    a_.add_argument("--item", required=True)
    a_.add_argument("--grade", type=int, choices=(1, 2, 3, 4), required=True)
    a_.add_argument("--confidence", type=int, choices=(1, 2, 3), required=True)
    a_.add_argument("--rung", choices=RUNGS, required=True)
    a_.add_argument("--question", required=True)
    a_.add_argument("--response", required=True)
    for name in ("taught", "level"):
        cmds[name].add_argument("--part", required=True)
    cmds["level"].add_argument("--to", type=int, choices=range(6), required=True)
    cmds["level"].add_argument("--reason", required=True)
    a = p.parse_args()

    if not a.dir.is_dir():
        die(f"no such data directory: {a.dir}")
    path = a.dir / "log.jsonl"
    try:
        now = parse_time(a.now) if a.now else datetime.now(timezone.utc)
    except ValueError as e:
        die(str(e))
    rows = read_log(path)

    if a.cmd in ("answer", "taught", "level"):
        if rows and now < rows[-1]["ts"]:
            die(f"--now {now.isoformat()} is older than the last row; the log is append-only")
        row = {"ts": now.isoformat(), "kind": a.cmd}
        if a.cmd == "answer":
            row.update(item=a.item, grade=a.grade, confidence=a.confidence, rung=a.rung,
                       question=a.question, response=a.response[:200])
        elif a.cmd == "taught":
            row.update(part=a.part)
        else:
            row.update(part=a.part, level=a.to, reason=a.reason)
        try:
            validate(dict(row))
        except ValueError as e:
            die(str(e))
        with path.open("a") as f:
            f.write(json.dumps(row) + "\n")
        if a.cmd == "answer":
            print(f"{a.item}\tnext due {local(replay(read_log(path))[a.item].due)}")
    elif a.cmd == "due":
        cards = replay(rows)
        last_q = {r["item"]: r["question"] for r in rows if r["kind"] == "answer"}
        for item, card in sorted(cards.items(), key=lambda kv: kv[1].due):
            if card.due <= now:
                print(f"{item}\t{local(card.due)}\t{last_q[item]}")
    else:
        show(rows, replay(rows))


if __name__ == "__main__":
    main()
