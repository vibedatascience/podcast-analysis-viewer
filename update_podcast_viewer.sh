#!/bin/bash

# Podcast Viewer Auto-Update Script
# This script regenerates index.html and pushes to GitHub

# Set the working directory
cd /Users/rahulchaudhary/podcast-analysis-viewer || exit 1

# Run the podcast viewer generator
echo "$(date): Running podcast_viewer.py..."
/Users/rahulchaudhary/opt/anaconda3/bin/python3 podcast_viewer.py

# Check if there are changes to commit
if git diff --quiet index.html; then
    echo "$(date): No changes detected in index.html"
    exit 0
fi

# Add and commit the changes
echo "$(date): Changes detected, committing..."
git add index.html

git commit -m "Auto-update: Regenerate podcast viewer index.html

Automated update generated at $(date '+%Y-%m-%d %H:%M:%S')

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
echo "$(date): Pushing to GitHub..."
git push origin main

echo "$(date): Update complete!"
