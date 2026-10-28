# KEV Deadline Tracker

## The business risk first

When a vulnerability is added to the CISA Known Exploited Vulnerabilities catalog, federal agencies get a firm due date, and everyone else gets a warning that attackers are already using it. Missing that date is not a paperwork problem. It means a known, actively exploited flaw stays open in production, with the exposure, incident cost, and audit finding that follow.

This tool is a simple deadline list: what is due, when, and how many days are left. Nothing fancy, nothing that can silently break. A list you actually look at beats a dashboard nobody opens.

## How it differs from kev-watcher

kev-watcher diffs the KEV catalog to find what changed. This tracker does not diff anything. It holds the deadline list and reports what is due soon and what is already past due.

## Run it

```bash
python kev_tracker.py
python kev_tracker.py --days 14
python kev_tracker.py --overdue
```

## Example entries

The starter list includes two example entries: PHP2Shell, due October 29, 2026, and PolyShell / Brotli, due November 10, 2026. Add your own entries to `deadlines.json` in the same format: name, due date (YYYY-MM-DD), and a note.

## Verify before you act

Always confirm a due date against the current CISA Known Exploited Vulnerabilities catalog before acting on it. Catalog dates can change, and this list is only as current as its last update.

## Requirements

Python 3.8 or later. No third party packages.

## Author

Kevin Swaney, Principal Cybersecurity Engineer. More at [kevintswaney.com](https://kevintswaney.com).
