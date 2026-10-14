FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --system --no-create-home analyst

COPY --chown=analyst:analyst app/ ./app/
COPY --chown=analyst:analyst logs/ ./logs/

USER analyst

CMD ["python", "-m", "app.analyzer", "logs/sample.log"]
