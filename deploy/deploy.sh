#!/usr/bin/env bash
# Deploys the agent to Agent Engine with ADK's own deploy command. No GCS bucket is used: ADK builds a Dockerfile
# and sends the agent source inline. Settings come from codemender_agent/.env (see codemender_agent/.env.example).
# Usage: ./deploy/deploy.sh                 create a new engine
#        ./deploy/deploy.sh <ENGINE_ID>     update an existing engine (the number at the end of its resource name)
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f codemender_agent/.env ] || { echo "Missing codemender_agent/.env: copy codemender_agent/.env.example and edit it."; exit 1; }
extra=()
[ $# -ge 1 ] && extra+=(--agent_engine_id "$1")
exec adk deploy agent_engine \
  --display_name "CodeMender Scan Agent" \
  --description "Scans a git repository for security vulnerabilities and returns a PDF and Markdown report with findings and suggested fixes." \
  ${extra[@]+"${extra[@]}"} codemender_agent
