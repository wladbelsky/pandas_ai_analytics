FROM python:3.13

LABEL authors="wladbelsky"

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "main.py"]
