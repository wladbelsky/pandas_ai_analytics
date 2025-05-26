FROM python:3.13-bullseye

LABEL authors="wladbelsky"

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "main.py"]
