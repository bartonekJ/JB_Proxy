FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

RUN echo "force_render_rebuild_001"

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "server:app"]
