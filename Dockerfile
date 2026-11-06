FROM python:3.12-slim

WORKDIR /app

# primero las dependencias para aprovechar la cache de docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# codigo fuente
COPY src/ ./src/

# usuario sin privilegios que pueda ejecutar el codigo
RUN useradd -m appuser && chown -R appuser:appuser /app && chmod -R 755 /app
USER appuser

WORKDIR /app/src

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
