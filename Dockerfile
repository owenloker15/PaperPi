FROM python:3.12-slim-bullseye

WORKDIR /app

# Install system dependencies required for Raspberry Pi and Pimoroni Inky
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff5 \
    libgpiod2 \
    python3-dev \
    fonts-dejavu \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Create temp directory if needed
RUN mkdir -p /app/temp

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "./src/paperpi.py"]