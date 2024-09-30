FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY power_model.pkl .
COPY cpu_load_model.pkl .
COPY power_scaler.pkl .
COPY cpu_scaler.pkl .

CMD ["python", "app.py"] 