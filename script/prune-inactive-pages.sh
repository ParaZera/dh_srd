#!/usr/bin/env bash
# prune-inactive-pages.sh
# Delete every deployment whose *latest* status is **inactive**
#
# Usage:
#   ./prune-inactive-pages.sh                 # current repo
#   ./prune-inactive-pages.sh owner/repo      # explicit repo
#   ./prune-inactive-pages.sh owner/repo env  # explicit repo + env name
#
# Needs: gh ≥ 2.45, jq, a token with repo → Deployments (write).

set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
ENV_NAME="${2:-github-pages}"     # filter to the Pages environment

echo "🔍  Scanning '$REPO' (environment: $ENV_NAME)"

gh api "repos/$REPO/deployments?environment=$ENV_NAME" \
       --paginate --jq '.[].id' |
while read -r DEPLOY_ID; do
  # Most-recent status (per_page=1 returns newest first)
  STATE=$(gh api \
          "repos/$REPO/deployments/$DEPLOY_ID/statuses?per_page=1" \
          --jq '.[0].state // "none"')

  if [[ "$STATE" == "inactive" ]]; then
    echo "🗑️   Deleting deployment $DEPLOY_ID (state: inactive)"
    gh api -X DELETE "repos/$REPO/deployments/$DEPLOY_ID"
  else
    echo "⏭️   Keeping deployment $DEPLOY_ID (state: $STATE)"
  fi
done

echo "🏁  Done – only inactive deployments were removed."