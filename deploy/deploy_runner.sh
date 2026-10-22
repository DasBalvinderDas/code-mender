#!/usr/bin/env bash
# Deploys the CodeMender runner (the sandbox that runs the real `cm` CLI) to Cloud Run, then saves its URL in .env.
# Settings come from the repository-root .env: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, AGENT_SERVICE_ACCOUNT.
# The runner runs as AGENT_SERVICE_ACCOUNT (the account that has CodeMender access) unless RUNNER_SA is set.
# Usage: ./deploy/deploy_runner.sh
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || { echo "Missing .env: copy .env.example to .env and edit it."; exit 1; }
env_get() { grep -E "^$1=" .env | head -1 | cut -d= -f2- || true; }

PROJECT="${PROJECT:-$(env_get GOOGLE_CLOUD_PROJECT)}"
REGION="${REGION:-$(env_get GOOGLE_CLOUD_LOCATION)}"; REGION="${REGION:-us-central1}"
AGENT_SA="${AGENT_SA:-$(env_get AGENT_SERVICE_ACCOUNT)}"
RUNNER_SA="${RUNNER_SA:-$AGENT_SA}"
SVC="${SVC:-codemender-runner}"; REPO="${REPO:-codemender}"
[ -n "$PROJECT" ] || { echo "Set GOOGLE_CLOUD_PROJECT in .env"; exit 1; }
[ -n "$RUNNER_SA" ] || { echo "Set AGENT_SERVICE_ACCOUNT in .env (the service account that has CodeMender access)"; exit 1; }
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}/${SVC}:latest"

echo "Project: $PROJECT  Region: $REGION"
echo "Runner runs as: $RUNNER_SA"
echo "Agent (allowed to call the runner): ${AGENT_SA:-<none set>}"

gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --project "$PROJECT"

# 1. the cm binary (needs your CodeMender access); skipped if already downloaded
if [ ! -f runner/cm-linux-amd64.zip ]; then
  echo "Downloading the cm CLI ..."
  gcloud artifacts generic download --project=cmoc-prod --location=us --repository=codemender-cli-production \
    --package=cm --version=stable --name=cm-linux-amd64.zip --destination=runner/
fi
[ -f runner/cm-linux-amd64.zip ] || { echo "runner/cm-linux-amd64.zip is missing; the download above failed (check your CodeMender access)."; exit 1; }

# 2. image
gcloud artifacts repositories describe "$REPO" --project "$PROJECT" --location "$REGION" >/dev/null 2>&1 || \
  gcloud artifacts repositories create "$REPO" --project "$PROJECT" --location "$REGION" --repository-format docker
gcloud builds submit --project "$PROJECT" --config deploy/cloudbuild-runner.yaml --substitutions "_IMAGE=$IMAGE" .

# 3. service: one always-on instance, because job state is kept in memory and jobs run in the background for minutes.
# Verify and fix (which run exploit code) are NOT enabled: RUNNER_ALLOW_VERIFY_FIX is deliberately not set.
gcloud run deploy "$SVC" --project "$PROJECT" --region "$REGION" --image "$IMAGE" --service-account "$RUNNER_SA" \
  --no-allow-unauthenticated --cpu 2 --memory 4Gi --timeout 3600 --concurrency 8 \
  --min-instances 1 --max-instances 1 --no-cpu-throttling \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_CLOUD_LOCATION=$REGION"

# 4. who may call it
if [ -n "$AGENT_SA" ]; then
  gcloud run services add-iam-policy-binding "$SVC" --project "$PROJECT" --region "$REGION" \
    --member "serviceAccount:$AGENT_SA" --role roles/run.invoker >/dev/null
fi
# the person testing from the shell
ME="$(gcloud config get-value account 2>/dev/null || true)"
[ -n "$ME" ] && gcloud run services add-iam-policy-binding "$SVC" --project "$PROJECT" --region "$REGION" \
    --member "user:$ME" --role roles/run.invoker >/dev/null 2>&1 || true

URL="$(gcloud run services describe "$SVC" --project "$PROJECT" --region "$REGION" --format='value(status.url)')"
if grep -qE "^CODEMENDER_RUNNER_URL=" .env; then sed -i "s#^CODEMENDER_RUNNER_URL=.*#CODEMENDER_RUNNER_URL=$URL#" .env; else echo "CODEMENDER_RUNNER_URL=$URL" >> .env; fi
echo
echo "Runner URL: $URL   (saved in .env as CODEMENDER_RUNNER_URL)"
echo "Next: check it with  python deploy/check_runner.py   then redeploy the agent:  python deploy/deploy_agent_engine.py"
