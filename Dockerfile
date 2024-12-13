FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY . .
RUN uv sync

EXPOSE 8080

CMD ["uv", "run", "lt_app", "--server.port", "8080"]
