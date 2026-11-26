# TMP Check — hosted pilot preview (A-53). Not for live customer TMPs before G6.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# LibreOffice converts Word uploads to PDF
RUN apt-get update && apt-get install -y --no-install-recommends libreoffice-writer-nogui fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY config ./config
COPY compliance ./compliance
# Persistent disk (fly volume) holds the database and uploaded documents
ENV TMPCHECK_ENV=preview TMPCHECK_HTTPS=1 \
    TMPCHECK_DB_URL=sqlite:////data/portal.db TMPCHECK_STORAGE=/data/docs
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "src.portal.app:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]
