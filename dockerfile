FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest ruff

COPY . .

RUN chmod -x Application/*.py tests/*.py

ENV PYTHONPATH=/app

CMD ["pytest", "-v"]
