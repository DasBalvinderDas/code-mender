FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY codemender_agent ./codemender_agent
RUN useradd -m app && chown -R app /app
USER app
ENV PORT=8080
CMD ["sh", "-c", "uvicorn codemender_agent.a2a_app:a2a_app --host 0.0.0.0 --port ${PORT}"]
