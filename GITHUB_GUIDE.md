# 📚 Hướng Dẫn Đưa Project Lên GitHub - Chi Tiết Từng Bước

## 📋 Mục Lục
1. [Chuẩn Bị](#1-chuẩn-bị)
2. [Tạo Repository Trên GitHub](#2-tạo-repository-trên-github)
3. [Khởi Tạo Git Trong Project](#3-khởi-tạo-git-trong-project)
4. [Push Code Lên GitHub](#4-push-code-lên-github)
5. [Cập Nhật Code Sau Này](#5-cập-nhật-code-sau-này)

---

## 1. Chuẩn Bị

### ✅ Kiểm tra Git đã được cài đặt chưa

Mở PowerShell hoặc CMD và chạy:

```bash
git --version
```

**Nếu chưa cài:**
- Tải Git tại: https://git-scm.com/download/win
- Cài đặt và restart terminal

### ✅ Cấu hình Git lần đầu (nếu chưa làm)

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

**Chú ý:** Email nên trùng với email GitHub của bạn.

### ✅ Đăng nhập GitHub

- Đảm bảo bạn đã có tài khoản GitHub
- Truy cập: https://github.com
- Đăng nhập vào tài khoản

---

## 2. Tạo Repository Trên GitHub

### Bước 1: Tạo Repository Mới

1. Vào GitHub (https://github.com)
2. Click nút **"+"** ở góc trên bên phải
3. Chọn **"New repository"**

### Bước 2: Điền Thông Tin

**Repository name:** `fastapi-todo-app` (hoặc tên bạn thích)

**Description:** (Tùy chọn)
```
A beautiful ToDo application built with FastAPI featuring CRUD operations, filtering, sorting, and pagination
```

**Visibility:**
- ✅ **Public** - Ai cũng có thể xem (khuyên dùng cho học tập)
- ⬜ **Private** - Chỉ bạn và người được mời xem

**Initialize this repository with:**
- ⬜ **KHÔNG TICK** vào "Add a README file"
- ⬜ **KHÔNG TICK** vào "Add .gitignore"
- ⬜ **KHÔNG TICK** vào "Choose a license"

> **Lưu ý:** Chúng ta sẽ push code có sẵn, nên KHÔNG tạo các file này trên GitHub.

### Bước 3: Tạo Repository

- Click nút **"Create repository"**
- GitHub sẽ hiển thị trang với hướng dẫn

**Lưu lại URL repository**, ví dụ:
```
https://github.com/username/fastapi-todo-app.git
```

---

## 3. Khởi Tạo Git Trong Project

### Mở Terminal trong thư mục project

**Cách 1:** Mở PowerShell/CMD và chạy:
```bash
cd "d:\phát triển ứng dụng\Todolist - FastAPI - TH1"
```

**Cách 2:** Trong VS Code:
- Nhấn **Ctrl + `** để mở terminal
- Terminal tự động mở ở thư mục project

### Chạy các lệnh sau (từng lệnh một):

#### 1️⃣ Khởi tạo Git repository
```bash
git init
```
✅ **Kết quả:** `Initialized empty Git repository...`

#### 2️⃣ Thêm tất cả file vào staging
```bash
git add .
```
✅ **Kết quả:** Không có output (im lặng là tốt)

#### 3️⃣ Tạo commit đầu tiên
```bash
git commit -m "Initial commit: FastAPI ToDo App with Web UI"
```
✅ **Kết quả:** Hiển thị số lượng file được commit

#### 4️⃣ Đổi tên branch thành main (nếu cần)
```bash
git branch -M main
```

---

## 4. Push Code Lên GitHub

### Bước 1: Kết nối với GitHub Repository

Thay `YOUR_GITHUB_USERNAME` và `YOUR_REPO_NAME` bằng thông tin của bạn:

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
```

**Ví dụ:**
```bash
git remote add origin https://github.com/phatdev/fastapi-todo-app.git
```

### Bước 2: Push code lên GitHub

```bash
git push -u origin main
```

### ⚠️ Xác Thực GitHub

**Lần đầu push, bạn sẽ cần xác thực:**

#### Cách 1: Sử dụng Personal Access Token (Khuyên dùng)

1. Vào GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. **Note:** `FastAPI Todo App`
4. **Expiration:** Chọn thời gian (ví dụ: 90 days)
5. **Select scopes:** Tick ✅ **repo** (toàn bộ)
6. Click **"Generate token"**
7. **Copy token** (chỉ hiện 1 lần!)

**Khi terminal hỏi password:**
- Username: `your_github_username`
- Password: **Dán token vừa copy** (không phải password GitHub)

#### Cách 2: Sử dụng GitHub CLI (Nâng cao)

```bash
gh auth login
```
Làm theo hướng dẫn trên màn hình.

### ✅ Kiểm tra trên GitHub

1. Mở trình duyệt
2. Vào repository của bạn: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
3. Bạn sẽ thấy toàn bộ code đã được push!

---

## 5. Cập Nhật Code Sau Này

### Khi bạn sửa code và muốn cập nhật lên GitHub:

#### 1️⃣ Kiểm tra file đã thay đổi
```bash
git status
```

#### 2️⃣ Thêm file đã thay đổi
```bash
git add .
```

Hoặc thêm file cụ thể:
```bash
git add app/main.py
git add static/style.css
```

#### 3️⃣ Commit với message mô tả
```bash
git commit -m "Add new feature: dark mode toggle"
```

**Mẹo:** Message nên mô tả rõ ràng những gì bạn thay đổi:
- ✅ `"Fix: resolve validation error in todo creation"`
- ✅ `"Add: implement search debouncing"`
- ❌ `"update"` (quá chung chung)

#### 4️⃣ Push lên GitHub
```bash
git push
```

---

## 📌 Các Lệnh Git Thường Dùng

### Xem trạng thái hiện tại
```bash
git status
```

### Xem lịch sử commit
```bash
git log
```

Hoặc gọn hơn:
```bash
git log --oneline
```

### Xem thay đổi chưa commit
```bash
git diff
```

### Xem remote repository
```bash
git remote -v
```

### Pull code mới nhất từ GitHub về
```bash
git pull
```

### Tạo branch mới
```bash
git branch feature-name
git checkout feature-name
```

Hoặc tạo và chuyển luôn:
```bash
git checkout -b feature-name
```

### Chuyển branch
```bash
git checkout main
```

### Merge branch
```bash
git checkout main
git merge feature-name
```

---

## 🎯 Quy Trình Làm Việc Chuẩn

### Làm việc hàng ngày:

1. **Pull code mới nhất:**
   ```bash
   git pull
   ```

2. **Làm việc và sửa code...**

3. **Xem thay đổi:**
   ```bash
   git status
   ```

4. **Add và commit:**
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```

5. **Push lên GitHub:**
   ```bash
   git push
   ```

---

## ⚠️ Xử Lý Lỗi Thường Gặp

### Lỗi: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Lỗi: "failed to push some refs"
```bash
git pull --rebase origin main
git push
```

### Lỗi: "Permission denied"
- Kiểm tra lại Personal Access Token
- Kiểm tra username/email đã đúng chưa

### Muốn bỏ qua một file trong commit
Sửa file `.gitignore` và thêm tên file:
```
test_file.py
```

### Huỷ commit chưa push
```bash
git reset --soft HEAD~1
```

---

## 🎨 Tùy Chỉnh README cho GitHub

File `README.md` hiện tại đã khá đầy đủ, nhưng bạn có thể thêm:

### Badges (huy hiệu đẹp):
```markdown
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

### Screenshots:
1. Chụp ảnh màn hình giao diện
2. Upload vào GitHub (Issues → New Issue → kéo ảnh vào)
3. Copy link ảnh
4. Thêm vào README:
```markdown
## Screenshots

![Web UI](https://github.com/user/repo/issues/1/screenshot.png)
```

---

## 📚 Tài Nguyên Học Git

- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com
- **Interactive Tutorial:** https://learngitbranching.js.org

---

## ✅ Checklist Cuối Cùng

Trước khi push, đảm bảo:

- ✅ File `.gitignore` đã được tạo
- ✅ Đã xóa các file nhạy cảm (passwords, API keys)
- ✅ File `README.md` có hướng dẫn rõ ràng
- ✅ File `requirements.txt` đầy đủ dependencies
- ✅ Code chạy được trên máy local
- ✅ Đã commit với message rõ ràng
- ✅ Repository visibility đúng (Public/Private)

---

## 🎉 Hoàn Thành!

Sau khi push thành công, bạn có thể:

1. **Chia sẻ link repository** với bạn bè, giáo viên
2. **Clone** project về máy khác để làm việc
3. **Cộng tác** với người khác (nếu Public)
4. **Thêm vào portfolio** GitHub của bạn

**Link repository của bạn:**
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

---

## 💡 Mẹo Pro

### 1. Sử dụng Git GUI (nếu không thích command line)
- **GitHub Desktop:** https://desktop.github.com
- **GitKraken:** https://www.gitkraken.com
- **VS Code Git Extension:** Tích hợp sẵn trong VS Code

### 2. Tạo .gitignore tự động
Vào: https://www.toptal.com/developers/gitignore
Chọn: Python, FastAPI, VisualStudioCode

### 3. Pre-commit Hooks
Tự động format code trước khi commit:
```bash
pip install pre-commit
pre-commit install
```

---

**Chúc bạn thành công! 🚀**

Nếu gặp vấn đề, hãy check lại từng bước hoặc Google error message cụ thể!
