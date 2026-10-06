---
name: kiem-tra-memory
description: Kiểm tra độ dài các file memory/, labs/, .claude/, CLAUDE.md theo giới hạn trong .claude/rules/memory-files.md, báo file vượt / sắp vượt / thiếu mục lục. Dùng khi người học gõ /kiem-tra-memory, nói "kiểm tra memory", "check độ dài file", "trước khi commit", hoặc trước bước nhắc commit của /save-progress.
---

# Kiểm tra memory — verification skill

Mục tiêu: trả lời pass/fail **bằng script**, không ước lượng bằng mắt. Bảng giới hạn nằm trong
[check_lengths.py](check_lengths.py), phải khớp với [memory-files.md](../../rules/memory-files.md).

## Các bước

1. **Chạy script** từ thư mục gốc repo:
   `.venv/Scripts/python .claude/skills/kiem-tra-memory/check_lengths.py`
   (máy không có `.venv` thì dùng `python`). Exit 0 = đạt, 1 = có file vượt.
2. **Báo kết quả** bằng cách chép nguyên dòng tổng kết của script. Nếu mọi thứ OK thì chỉ cần 1 dòng.
3. **Có ❌ (vượt)** → với từng file, đề xuất cách tách theo cột "Vượt thì làm gì" của rule.
   **Chỉ đề xuất, chưa sửa** — hỏi người học trước, vì tách file kéo theo sửa link.
4. **Có ⚠️ (sắp vượt) hoặc 📑 (thiếu mục lục)** → nhắc một dòng, không chặn commit.

## Không được
- Tự đếm dòng thay vì chạy script (đếm tay sai được, script thì không).
- Sửa bảng giới hạn trong script để file "pass". Muốn đổi giới hạn → sửa rule trước, rồi đồng bộ script.
