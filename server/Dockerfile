FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libgbm1 \
    libxshmfence1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xvfb \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft Edge (Stable)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && \
    apt-get install -y microsoft-edge-stable && \
    rm -rf /var/lib/apt/lists/*

# Download and install matching msedgedriver (136.0.3240.92 for example)
RUN wget -O msedgedriver.zip "https://msedgedriver.azureedge.net/136.0.3240.92/edgedriver_linux64.zip" && \
    unzip msedgedriver.zip && \
    mv msedgedriver /usr/bin/msedgedriver && \
    chmod +x /usr/bin/msedgedriver && \
    rm msedgedriver.zip

# Copy Python files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
