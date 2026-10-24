
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY constraints.txt .

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu "torch==2.6.0+cpu"
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -c constraints.txt -r requirements.txt

COPY app ./app
COPY data ./data
COPY tests ./tests

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
