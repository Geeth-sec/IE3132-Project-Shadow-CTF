FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY evidence/ /evidence/

RUN useradd --create-home --shell /usr/sbin/nologin ctfuser \
    && chown -R ctfuser:ctfuser /app /evidence

USER ctfuser

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]