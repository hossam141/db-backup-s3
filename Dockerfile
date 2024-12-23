FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-mysql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backup_script.py .

CMD ["python", "backup_script.py"]