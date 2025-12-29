FROM python:3.11-slim
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir pandas prophet scikit-learn sqlalchemy psycopg2-binary
CMD ["python", "-m", "analytics.runner"]
