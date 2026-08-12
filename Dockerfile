FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements/backend.txt requirements/backend.txt
RUN pip install --no-cache-dir -r requirements/backend.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=/data/wasify.db

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
