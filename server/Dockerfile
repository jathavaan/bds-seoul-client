FROM --platform=$BUILDPLATFORM python:3.11-slim

ARG TARGETARCH

WORKDIR /app

# Install Firefox ESR and all of its headless dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      firefox-esr \
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

# Fetch the right Geckodriver for this ARCH
RUN set -eux; \
    GECKO_VER=0.33.0; \
    case "$TARGETARCH" in \
      amd64)  SUFFIX=linux64   ;; \
      arm64)  SUFFIX=linux-aarch64 ;; \
      *) echo "Unsupported arch: $TARGETARCH" >&2; exit 1 ;; \
    esac; \
    curl -fsSL "https://github.com/mozilla/geckodriver/releases/download/v${GECKO_VER}/geckodriver-v${GECKO_VER}-${SUFFIX}.tar.gz" \
      | tar -xz -C /usr/local/bin

# Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Optionally wait a second for geckodriver to be ready
CMD sh -c "\
    geckodriver --port 4444 & \
    sleep 2 && \
    uvicorn main:app --host 0.0.0.0 --port 5000"
