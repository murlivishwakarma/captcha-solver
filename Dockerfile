FROM python:3.10-slim

# Install Tesseract OCR and necessary libraries
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the local files into the container's working directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 4000 for local testing (this will be overridden by Azure's environment variables)
EXPOSE 4000

# Start the Flask app using Gunicorn, listen on the port Azure assigns (usually 80)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:$PORT", "app:app"]
