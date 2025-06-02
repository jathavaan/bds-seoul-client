FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libgbm1 \
    libxshmfence1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 && \
    ln -sf /usr/lib/chromium/chromedriver /usr/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

CMD ["python", "main.py"]

