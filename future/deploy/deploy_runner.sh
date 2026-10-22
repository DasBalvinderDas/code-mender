#!/usr/bin/env bash
# Deploys the CodeMender runner (the sandbox that runs the real `cm` CLI) to Cloud Run.
# Prerequisite: runner/cm-linux-amd64.zip exists (see the download command in runner/Dockerfile).
# Usage: PROJECT=my-proj REGION=us-central1 AGENT_SA=<agent engine runtime service account email> ./deploy/deploy_runner.sh
set -euo pipefail
: "${PROJECT:?set PROJECT}"; : "${AGENT_SA:?set AGENT_SA (the CodeMender agent's runtime service account)}"
REGION="${REGION:-us-central1}"; SVC="${SVC:-codemender-runner}"; REPO="${REPO:-codemender}"
RUNNER_SA="${RUNNER_SA:-codemender-runner@${PROJECT}.iam.gserviceaccount.com}"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}/${SVC}:latest"
[ -f runner/cm-linux-amd64.zip ] || { echo "runner/cm-linux-amd64.zip is missing; download it first (see runner/Dockerfile)"; exit 1; }

gcloud artifacts repositories describe "$REPO" --project "$PROJECT" --location "$REGION" >/dev/null 2>&1 || \
  gcloud artifacts repositories create "$REPO" --project "$PROJECT" --location "$REGION" --repository-format docker
# The runner identity runs exploit scripts, so give it the minimum: Vertex AI only (needed by cm).
gcloud iam service-accounts describe "$RUNNER_SA" --project "$PROJECT" >/dev/null 2>&1 || \
  gcloud iam service-accounts create "${RUNNER_SA%%@*}" --project "$PROJECT" --display-name "CodeMender runner"
gcloud projects add-iam-policy-binding "$PROJECT" --member "serviceAccount:$RUNNER_SA" --role roles/aiplatform.user --condition=None >/dev/null

gcloud builds submit --project "$PROJECT" --config deploy/cloudbuild-runner.yaml --substitutions "_IMAGE=$IMAGE" .
# One instance, always on: job state is in memory and jobs run in the background for many minutes.
gcloud run deploy "$SVC" --project "$PROJECT" --region "$REGION" --image "$IMAGE" --service-account "$RUNNER_SA" \
  --no-allow-unauthenticated --cpu 2 --memory 4Gi --timeout 3600 --concurrency 8 \
  --min-instances 1 --max-instances 1 --no-cpu-throttling \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_CLOUD_LOCATION=$REGION"
gcloud run services add-iam-policy-binding "$SVC" --project "$PROJECT" --region "$REGION" \
  --member "serviceAccount:$AGENT_SA" --role roles/run.invoker >/dev/null
echo "Runner URL: $(gcloud run services describe "$SVC" --project "$PROJECT" --region "$REGION" --format='value(status.url)')"
echo "Pass it to the agent deploy: --runner-url <that URL>"
