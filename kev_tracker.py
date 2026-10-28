#!/usr/bin/env python3
"""CISA KEV deadline tracker: a simple list with due dates.

This tool is different from kev-watcher. kev-watcher diffs the KEV
catalog to find what changed. This tool is just the deadline list:
what is due, when, and how many days are left, so nothing slips past
a federal due date unnoticed.

Usage:
    python kev_tracker.py                  # all deadlines, soonest first
    python kev_tracker.py --days 14        # only deadlines within 14 days
    python kev_tracker.py --overdue        # only past due items
    python kev_tracker.py --file deadlines.json

Deadlines live in deadlines.json next to this script. Add entries there
in the same format: name, due_date (YYYY-MM-DD), and an optional note.
Always verify a due date against the current CISA Known Exploited
Vulnerabilities catalog before acting on it.
Requires Python 3.8 or later. No third party packages.
"""

import argparse
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path, encoding="utf-8") as handle:
        entries = json.load(handle)
    out = []
    for entry in entries:
        year, month, day = (int(part) for part in entry["due_date"].split("-"))
        due = date(year, month, day)
        out.append((entry["name"], due, entry.get("note", "")))
    return sorted(out, key=lambda item: item[1])


def main(argv=None):
    parser = argparse.ArgumentParser(description="List CISA KEV federal due dates.")
    parser.add_argument("--file", default=os.path.join(HERE, "deadlines.json"),
                        help="deadline list in JSON format")
    parser.add_argument("--days", type=int, default=None,
                        help="only show deadlines within this many days")
    parser.add_argument("--overdue", action="store_true", help="only show past due items")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    args = parser.parse_args(argv)
    if args.version:
        print("kev-deadline-tracker 1.0.0")
        return 0
    today = date.today()
    entries = load(args.file)
    shown = []
    for name, due, note in entries:
        delta = (due - today).days
        if args.overdue and delta >= 0:
            continue
        if args.days is not None and not (0 <= delta <= args.days):
            continue
        shown.append((name, due, delta, note))
    print("=" * 60)
    print("CISA KEV DEADLINE TRACKER (today: %s)" % today.isoformat())
    print("=" * 60)
    if not shown:
        print("No deadlines match this filter.")
        return 0
    for name, due, delta, note in shown:
        if delta < 0:
            status = "OVERDUE by %d day(s)" % abs(delta)
        elif delta == 0:
            status = "DUE TODAY"
        else:
            status = "due in %d day(s)" % delta
        print("%-24s %-12s %s" % (name, due.isoformat(), status))
        if note:
            print("    %s" % note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
