# Bài 05 - Bài tập to-do-list

Dưới đây là tài liệu chi tiết về dự án To-Do List FastAPI được xây dựng và hoàn thiện qua 8 cấp độ từ cơ bản đến nâng cao.

---

## Cấp 0 — Làm quen FastAPI (Hello To-Do)
**Mục tiêu:** tạo API tối thiểu chạy được.
**Yêu cầu:**
- Tạo project FastAPI
- Endpoint:
  - `GET /health` → trả `{ "status": "ok" }`
  - `GET /` → trả message chào
**Tiêu chí đạt:**
- Chạy uvicorn và gọi được 2 endpoint.

---

## Cấp 1 — CRUD cơ bản (dữ liệu trong RAM)
**Mục tiêu:** làm CRUD với list/dict trong bộ nhớ (chưa dùng DB).
**Model ToDo:**
- `id`: int
- `title`: str
- `is_done`: bool = False
**Endpoints gợi ý:**
- `POST /todos` tạo todo
- `GET /todos` lấy danh sách
- `GET /todos/{id}` lấy chi tiết
- `PUT /todos/{id}` cập nhật toàn bộ
- `DELETE /todos/{id}` xóa
**Tiêu chí đạt:**
- Validate dữ liệu bằng Pydantic
- Trả lỗi đúng khi không tìm thấy (404)

---

## Cấp 2 — Validation “xịn” + filter/sort/pagination
**Mục tiêu:** API giống thực tế hơn.
**Yêu cầu:**
- `title` không được rỗng, độ dài 3–100
- `GET /todos` hỗ trợ:
  - filter: `is_done=true/false`
  - search: `q=keyword` (tìm theo title)
  - sort: `sort=created_at` hoặc `sort=-created_at`
  - pagination: `limit`, `offset`
**Tiêu chí đạt:**
- Response có cấu trúc:
  `{ "items": [...], "total": 123, "limit": 10, "offset": 0 }`

---

## Cấp 3 — Tách tầng (router/service/repository) + cấu hình chuẩn
**Mục tiêu:** viết như dự án thật.
**Yêu cầu:**
- Tách thư mục: `routers/`, `schemas/`, `services/`, `repositories/`, `core/`
- Dùng `APIRouter`, prefix `/api/v1`
- Config bằng `pydantic-settings` (env): `APP_NAME`, `DEBUG`, …
**Tiêu chí đạt:**
- Không viết logic DB trong router
- Có file `main.py` sạch

---

## Cấp 4 — Dùng Database (SQLite/PostgreSQL) + ORM
**Mục tiêu:** lưu dữ liệu thật.
**Yêu cầu:**
- Dùng SQLAlchemy (hoặc SQLModel)
- Bảng `todos` có: `id`, `title`, `description`, `is_done`, `created_at`, `updated_at`
- Migration bằng Alembic (nếu dùng SQLAlchemy)
- Endpoints thêm:
  - `PATCH /todos/{id}` cập nhật một phần (vd: chỉ `is_done`)
  - `POST /todos/{id}/complete` đánh dấu hoàn thành (tùy bạn)
**Tiêu chí đạt:**
- `created_at`/`updated_at` tự cập nhật
- Query có pagination thực sự từ DB

---

## Cấp 5 — Authentication + User riêng
**Mục tiêu:** mỗi user có to-do riêng.
**Yêu cầu:**
- Bảng `users`: `id`, `email`, `hashed_password`, `is_active`, `created_at`
- JWT login:
  - `POST /auth/register`
  - `POST /auth/login`
  - `GET /auth/me`
- Todo gắn `owner_id`
**Tiêu chí đạt:**
- User A không xem/xóa todo của User B
- Password hash bằng passlib/bcrypt

---

## Cấp 6 — Nâng cao (tag, deadline, nhắc việc)
**Mục tiêu:** thêm tính năng giống app thật.
**Yêu cầu tính năng:**
- `due_date` (deadline)
- `tags` (nhiều tag)
- `GET /todos/overdue` danh sách quá hạn
- `GET /todos/today` việc cần làm hôm nay

---

## Cấp 7 — Testing + tài liệu + deploy
**Mục tiêu:** hoàn chỉnh quy trình.
**Yêu cầu:**
- Viết test bằng pytest + TestClient
- Test các case:
  - tạo thành công
  - validation fail
  - 404
  - auth fail
- Dockerfile + docker-compose (nếu dùng Postgres)
- Viết README chạy dự án

---

## Hướng dẫn Chạy Dự Án & Deploy (Theo Cấp 7)

### Cài đặt môi trường Lab
Khởi tạo và cài đặt các thư viện cần dùng:
```bash
pip install -r requirements.txt
```

### Khởi tạo Cơ sở dữ liệu (SQLite)
Chạy lệnh migration bằng Alembic để khởi tạo các bảng:
```bash
alembic upgrade head
```

### Chạy Server (Local)
Dự án được khởi động bằng lệnh:
```bash
python -m app.main
# Hoặc: uvicorn app.main:app --reload
```
- Web UI: [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)
- Docs (Swagger API): [http://localhost:8000/docs](http://localhost:8000/docs)

### Deploy bằng Docker
Dự án được cấu hình sẵn Dockerfile với SQLite cực kỳ tinh gọn.
Build image và chạy container:
```bash
docker build -t fastapi-todo .
docker run -d -p 8000:8000 --name my_todo_app fastapi-todo
```

### Chạy Testing (Kiểm thử chức năng)
Chạy tự động kiểm thử để xác minh logic backend bằng Pytest:
```bash
py -m pytest tests/ -v
# Hoặc: python -m pytest tests/ -v
```
Toàn bộ các yêu cầu của Cấp độ 7 đã được bao phủ toàn diện nhất!
