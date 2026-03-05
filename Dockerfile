FROM python:3.12-slim

WORKDIR /app

# SQLite được hỗ trợ sẵn, không cần cài thêm gcc cồng kềnh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Chạy migration DB mới nhất và sau đó khởi động server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
