#!/usr/bin/env python3
"""Refuses to let a commit through if a tracked text file looks as though it carries a personal name or
contact detail next to a participant ID. Install as a pre-commit hook:
    cp tools/check_no_pii.py .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
It is a coarse guard, not a substitute for the data management plan."""
import re, subprocess, sys
files = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=AM"], capture_output=True, text=True).stdout.split()
bad = []
pat_id = re.compile(r"\bP\d{2}\b")
pat_name_like = re.compile(r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\b")
pat_contact = re.compile(r"\b\d{3}[-. ]\d{3}[-. ]\d{4}\b|\b[\w.+-]+@[\w-]+\.\w+\b|\b\d{1,5}\s+[A-Z][a-z]+\s+(St|Ave|Rd|Dr|Ln|Blvd)\b")
for f in files:
    if not f.endswith((".csv", ".md", ".txt", ".json", ".py")) or f.startswith("data/synthetic/"):
        continue
    try:
        txt = open(f, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    for i, line in enumerate(txt.splitlines(), 1):
        if pat_id.search(line) and (pat_name_like.search(line) or pat_contact.search(line)):
            bad.append(f"{f}:{i}")
if bad:
    print("Possible personal data next to a participant ID; commit refused:\n  " + "\n  ".join(bad))
    sys.exit(1)
