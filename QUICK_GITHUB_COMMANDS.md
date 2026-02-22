# ⚡ Lệnh Git/GitHub - Cheat Sheet Nhanh

## 🚀 Push Lần Đầu (Copy-Paste Từng Dòng)

```bash
# 1. Khởi tạo Git
git init

# 2. Thêm tất cả file
git add .

# 3. Commit đầu tiên
git commit -m "Initial commit: FastAPI ToDo App"

# 4. Đổi branch thành main
git branch -M main

# 5. Kết nối GitHub (thay YOUR_USERNAME và YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 6. Push lên GitHub
git push -u origin main
```

---

## 🔄 Cập Nhật Code (Hàng Ngày)

```bash
# Xem file đã thay đổi
git status

# Thêm file thay đổi
git add .

# Commit với message
git commit -m "Mô tả thay đổi của bạn"

# Push lên GitHub
git push
```

---

## 📝 Một Lệnh Nhanh (All-in-One)

```bash
git add . && git commit -m "Update: your changes" && git push
```

---

## 🎯 Các Lệnh Thường Dùng

| Lệnh | Mô Tả |
|------|-------|
| `git status` | Xem trạng thái file |
| `git add .` | Thêm tất cả file |
| `git add file.py` | Thêm file cụ thể |
| `git commit -m "message"` | Commit với message |
| `git push` | Đẩy code lên GitHub |
| `git pull` | Kéo code mới về |
| `git log` | Xem lịch sử commit |
| `git diff` | Xem thay đổi |
| `git branch` | Xem danh sách branch |
| `git checkout -b new-branch` | Tạo branch mới |

---

## ⚠️ Fix Lỗi Nhanh

### Remote already exists
```bash
git remote remove origin
git remote add origin https://github.com/USER/REPO.git
```

### Failed to push
```bash
git pull --rebase origin main
git push
```

### Undo commit chưa push
```bash
git reset --soft HEAD~1
```

---

## 💯 Best Practices

✅ **Commit thường xuyên** (mỗi khi hoàn thành 1 tính năng nhỏ)  
✅ **Message rõ ràng** (mô tả điều gì thay đổi)  
✅ **Pull trước khi Push** (tránh conflict)  
✅ **Không commit file nhạy cảm** (.env, passwords)  

---

**Để xem chi tiết đầy đủ, đọc file `GITHUB_GUIDE.md`**
