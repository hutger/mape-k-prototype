FROM python:3.10.6-alpine

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD ["python3", "-u", "/app/mape-k.py"]