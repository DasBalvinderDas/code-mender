# Build from the repo root:  gcloud run deploy ... --source . --dockerfile runner/Dockerfile   (see deploy/deploy_runner.sh)
# Before building, download the cm binary into runner/ (needs your CodeMender access):
#   gcloud artifacts generic download --project=cmoc-prod --location=us --repository=codemender-cli-production \
#     --package=cm --version=stable --name=cm-linux-amd64.zip --destination=runner/
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates unzip \
    && rm -rf /var/lib/apt/lists/*
COPY runner/cm-linux-amd64.zip /tmp/cm.zip
RUN unzip /tmp/cm.zip -d /tmp/cmbin && install -m 0755 /tmp/cmbin/cm /usr/local/bin/cm && rm -rf /tmp/cm.zip /tmp/cmbin
WORKDIR /srv
COPY runner/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY runner ./runner
RUN useradd -m cmuser
USER cmuser
ENV PORT=8080
CMD ["sh", "-c", "uvicorn runner.app:app --host 0.0.0.0 --port ${PORT}"]
