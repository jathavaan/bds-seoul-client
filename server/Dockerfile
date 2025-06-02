FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        wget \
        unzip \
        curl \
        ca-certificates \
        fonts-liberation \
        libnss3 \
        libxss1 \
        libasound2 \
        libx11-xcb1 \
        libgbm1 \
        libxshmfence1 \
        libatk-bridge2.0-0 \
        libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

# Get Chromium version and download matching ChromeDriver
RUN CHROMIUM_VERSION=$(chromium --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') && \
    echo "Detected Chromium version: $CHROMIUM_VERSION" && \
    MAJOR_VERSION=$(echo $CHROMIUM_VERSION | cut -d '.' -f 1) && \
    DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | grep -B 5 "\"version\": \"$CHROMIUM_VERSION\"" | grep -oP 'https://.*?chromedriver-linux64.zip') && \
    echo "Downloading: $DRIVER_VERSION" && \
    wget -O /tmp/chromedriver.zip "$DRIVER_VERSION" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf /tmp/*

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]

