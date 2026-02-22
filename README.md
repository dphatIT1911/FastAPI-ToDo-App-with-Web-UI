# FastAPI ToDo Application

Ứng dụng quản lý công việc (ToDo List) được xây dựng bằng FastAPI với kiến trúc phân tầng rõ ràng.

## Yêu cầu đã hoàn thành

### ✅ Cấp 0 - Hello To-Do
- GET `/health` → trả về `{"status": "ok"}`
- GET `/` → trả về message chào mừng

### ✅ Cấp 1 - CRUD cơ bản
- Model ToDo với `id`, `title`, `is_done`
- POST `/api/v1/todos` - Tạo todo mới
- GET `/api/v1/todos` - Lấy danh sách todos
- GET `/api/v1/todos/{id}` - Lấy chi tiết todo
- PUT `/api/v1/todos/{id}` - Cập nhật todo
- DELETE `/api/v1/todos/{id}` - Xóa todo
- Validation bằng Pydantic
- Trả lỗi 404 khi không tìm thấy

### ✅ Cấp 2 - Validation + Filter/Sort/Pagination
- Validation: title không rỗng, độ dài 3-100 ký tự
- Filter: `is_done=true/false`
- Search: `q=keyword` (tìm theo title)
- Sort: `sort=created_at` hoặc `sort=-created_at`
- Pagination: `limit`, `offset`
- Response structure: `{"items": [...], "total": 123, "limit": 10, "offset": 0}`

### ✅ Cấp 3 - Kiến trúc phân tầng
- Cấu trúc thư mục: `routers/`, `schemas/`, `services/`, `repositories/`, `core/`
- Sử dụng APIRouter với prefix `/api/v1`
- Config bằng `pydantic-settings` (.env)
- Logic DB tách biệt khỏi router
- File `main.py` sạch

## Cài đặt

1. Tạo virtual environment:
```bash
python -m venv venv
```

2. Kích hoạt virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
uvicorn app.main:app --reload
```

Hoặc:
```bash
python app/main.py
```

Ứng dụng sẽ chạy tại: http://localhost:8000

## API Documentation

Truy cập Swagger UI tại: http://localhost:8000/docs

## Cấu trúc dự án

```
Todolist - FastAPI - TH1/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point, FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Pydantic Settings config
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── todo.py             # Pydantic models (validation)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── todo_repository.py  # Data access layer (in-memory)
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py     # Business logic
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── api.py          # API router aggregator
│           └── routers/
│               ├── __init__.py
│               └── todos.py    # ToDo endpoints
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
├── EXPLANATION.md              # Giải thích CRUD, Endpoint, Uvicorn
└── README.md                   # This file
```

## Ví dụ sử dụng

### Tạo ToDo mới
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Học FastAPI"}'
```

### Lấy danh sách ToDo với filter và pagination
```bash
curl "http://localhost:8000/api/v1/todos?is_done=false&limit=10&offset=0"
```

### Tìm kiếm ToDo
```bash
curl "http://localhost:8000/api/v1/todos?q=FastAPI"
```

### Sắp xếp theo thời gian tạo
```bash
curl "http://localhost:8000/api/v1/todos?sort=-created_at"
```

### Cập nhật ToDo
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Học FastAPI nâng cao", "is_done": true}'
```

### Xóa ToDo
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1"
```
