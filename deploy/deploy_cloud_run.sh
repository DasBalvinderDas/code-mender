#!/usr/bin/env bash
# Deploy the CodeMender analysis agent as an A2A server on Cloud Run.
# Usage: PROJECT=my-proj REGION=us-central1 [BUCKET=my-reports-bucket] ./deploy/deploy_cloud_run.sh
set -euo pipefail
: "${PROJECT:?set PROJECT}"; REGION="${REGION:-us-central1}"; SVC="${SVC:-codemender-agent}"

gcloud run deploy "$SVC" --project "$PROJECT" --region "$REGION" --source . \
  --no-allow-unauthenticated --memory 2Gi --timeout 900 \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_CLOUD_LOCATION=$REGION,CODEMENDER_REPORT_BUCKET=${BUCKET:-}"

URL=$(gcloud run services describe "$SVC" --project "$PROJECT" --region "$REGION" --format='value(status.url)')
# The agent card must advertise its real URL.
gcloud run services update "$SVC" --project "$PROJECT" --region "$REGION" --update-env-vars "PUBLIC_URL=$URL"
echo "Agent card: $URL/.well-known/agent-card.json"
echo "Grant the defect-fix agent's service account roles/run.invoker on $SVC."
