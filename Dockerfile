FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        git \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PYSPARK_PYTHON=python3

RUN pip install --no-cache-dir pipenv

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY --chown=appuser:appuser . .

RUN mkdir -p logs output && chown appuser:appuser logs output

USER appuser

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
