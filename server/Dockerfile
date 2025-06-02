FROM python:3.11-slim
WORKDIR /app

# Install dependencies + Firefox + GeckoDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    ca-certificates \
    firefox-esr \
    geckodriver \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables (optional but helps)
ENV FIREFOX_BIN=/usr/bin/firefox
ENV GECKODRIVER_BIN=/usr/bin/geckodriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]
