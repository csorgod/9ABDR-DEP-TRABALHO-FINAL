FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        git \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PYSPARK_PYTHON=python3

RUN pip install --no-cache-dir pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

RUN mkdir -p logs output

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
