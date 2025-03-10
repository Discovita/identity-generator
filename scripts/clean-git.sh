#!/bin/bash

# clean-git.sh - Script to identify and optionally delete stale git branches
# 
# Usage:
#   ./clean-git.sh         - Print branches that meet deletion criteria
#   ./clean-git.sh --delete - Print and delete branches that meet criteria
#
# Deletion criteria:
#   - Latest commit is more than 14 days old

set -e

# Check if --delete flag is provided
DELETE_MODE=false
if [[ "$1" == "--delete" ]]; then
    DELETE_MODE=true
    echo "Running in DELETE mode - branches will be deleted!"
else
    echo "Running in DRY RUN mode - branches will NOT be deleted"
    echo "Use --delete flag to delete branches"
fi

# Get current date in seconds since epoch
CURRENT_DATE=$(date +%s)
TWO_WEEKS_IN_SECONDS=$((14 * 24 * 60 * 60))

# Get all local branches (including those with slashes in names)
echo "Listing all local branches..."
git branch | grep -v "^\*" | sed 's/^[ \t]*//' > /tmp/local_branches.txt
cat /tmp/local_branches.txt

# Array to store branches to delete
BRANCHES_TO_DELETE=()

echo "Analyzing branches..."
while IFS= read -r branch; do
    echo "Checking branch: $branch"
    
    # Skip master branch
    if [[ "$branch" == "master" ]]; then
        echo "  - Skipping master branch"
        continue
    fi
    
    # Check branch age
    LAST_COMMIT_DATE=$(git log -1 --format=%at "$branch" 2>/dev/null || echo "0")
    
    # If we couldn't get the commit date, skip this branch
    if [[ "$LAST_COMMIT_DATE" == "0" ]]; then
        echo "  - Could not get last commit date, skipping"
        continue
    fi
    
    BRANCH_AGE_SECONDS=$((CURRENT_DATE - LAST_COMMIT_DATE))
    DAYS_OLD=$((BRANCH_AGE_SECONDS / 86400))
    echo "  - Branch is $DAYS_OLD days old"
    
    if [[ $BRANCH_AGE_SECONDS -gt $TWO_WEEKS_IN_SECONDS ]]; then
        # Branch meets the age criteria
        LAST_COMMIT_DATE_HUMAN=$(git log -1 --format=%cd --date=human "$branch")
        BRANCHES_TO_DELETE+=("$branch")
        echo "Branch '$branch' qualifies for deletion:"
        echo "  - Last commit: $LAST_COMMIT_DATE_HUMAN ($DAYS_OLD days ago)"
    else
        echo "  - Branch is not old enough for deletion (less than 14 days)"
    fi
done < /tmp/local_branches.txt

# Clean up temp file
rm /tmp/local_branches.txt

# Print summary
echo ""
if [[ ${#BRANCHES_TO_DELETE[@]} -eq 0 ]]; then
    echo "No branches found that meet deletion criteria."
    exit 0
else
    echo "Found ${#BRANCHES_TO_DELETE[@]} branches that meet deletion criteria:"
    for branch in "${BRANCHES_TO_DELETE[@]}"; do
        echo "  - $branch"
    done
fi

# Delete branches if in delete mode
if [[ "$DELETE_MODE" == true ]]; then
    echo ""
    echo "Deleting branches..."
    for branch in "${BRANCHES_TO_DELETE[@]}"; do
        echo "Deleting local branch: $branch"
        git branch -D "$branch"
    done
    echo "Branch cleanup complete!"
else
    echo ""
    echo "To delete these branches, run: ./clean-git.sh --delete"
fi
