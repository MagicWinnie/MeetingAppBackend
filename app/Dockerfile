FROM python:3.13-slim

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY app/ app/
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# Install dependencies
RUN uv sync --frozen --no-cache

RUN dos2unix app/init.sh
RUN chmod +x app/init.sh

ENTRYPOINT ["sh", "-c", "app/init.sh && /app/.venv/bin/fastapi run app/main.py --port 8000 --host 0.0.0.0"]