FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ["nelson bambina food web page/requirements.txt", "./requirements.txt"]
RUN pip install --no-cache-dir -r requirements.txt

COPY ["nelson bambina food web page/bft_ai", "./bft_ai"]
COPY ["nelson bambina food web page/BFT Nelson.html", "./BFT Nelson.html"]

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn bft_ai.api:app --host 0.0.0.0 --port \"${PORT:-8000}\""]
