FROM python:latest

WORKDIR /app

COPY requirements.txt /app
COPY src /app 

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py", "2>&1", "|", "tee", "-a", "/logs/output-docker.log"]
