FROM python:3.10-slim

# Prevent tzdata from blocking installs
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install OS packages required by Playwright browsers
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxi6 \
    libxrender1 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "server:app"]
