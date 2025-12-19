#!/usr/bin/env bash
# Simple script to create GitHub issues from the GH_ISSUES_PHASE1.md file.
# Requires: gh CLI (https://cli.github.com/) and authenticated user (gh auth login)

set -e
REPO="Debalent/RelayPoint"
FILE="EXPERIMENTS/ROADMAP/GH_ISSUES_PHASE1.md"

gawk 'BEGIN{RS="\n\n---\n\n"; i=0} NR>1{print > ("/tmp/gh_issue_" NR ".md")}' "$FILE"

for f in /tmp/gh_issue_*.md; do
  title=$(head -n 1 "$f" | sed 's/^ISSUE: //')
  body=$(sed '1d' "$f")
  echo "Creating issue: $title"
  gh issue create --repo $REPO --title "$title" --body "$body" --label "phase1"
done

echo "Done creating issues."
