FROM mcr.microsoft.com/playwright/python:v1.49.0-focal

# Výchozí playwright image už obsahuje:
# - chromium, webkit, firefox
# - správné knihovny
# - správnou cache strukturu

WORKDIR /app

# Prevent tzdata from blocking installs
ENV DEBIAN_FRONTEND=noninteractive

# Zkopíruj Python požadavky
COPY requirements.txt .

# Nainstaluj Python knihovny (Flask, etc)
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj projekt
COPY . .

EXPOSE 8000

# Render vyžaduje, aby server běžel na 0.0.0.0
CMD ["gunicorn", "-b", "0.0.0.0:8000", "server:app"]
