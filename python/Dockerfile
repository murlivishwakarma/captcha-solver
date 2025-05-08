FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:4000", "app:app"]
