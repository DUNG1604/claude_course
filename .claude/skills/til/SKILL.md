---
name: til
description: Ghi ngay 1 điều vừa học vào memory/notes/ đúng chủ đề. Dùng khi người học gõ /til, hoặc nói "hôm nay mình học được...", "à hóa ra...", "giờ mới hiểu...", "ghi lại cái này", "nhớ cái này giúp mình".
---

# TIL — ghi ngay điều vừa học

Mục tiêu: điều người học vừa hiểu ra được lưu đúng chỗ trong `memory/notes/` trong vài giây,
không phải đợi tới `/save-progress` cuối phiên.

Nội dung cần ghi: phần chữ sau `/til`, hoặc ý người học vừa nói. Nếu mơ hồ, hỏi lại 1 câu ngắn.

## Các bước

1. **Đọc [memory/NOTES.md](../../../memory/NOTES.md)** (mục lục) để chọn file chủ đề khớp nhất.
   Không mở hết các file trong `notes/`.
2. **Có file khớp** → mở file đó, kiểm tra ý này **đã có chưa**:
   - Đã có → bổ sung chi tiết mới vào dòng cũ (nếu có), không ghi trùng.
   - Chưa có → thêm 1–3 dòng ngắn, viết sao cho đọc lại sau 1 tuần vẫn hiểu; kèm ví dụ nếu cần.

   **Không có file khớp** → tạo `memory/notes/<chủ-đề>.md` (tên kebab-case, tiêu đề `# ...`)
   và thêm 1 dòng vào đúng nhóm trong `NOTES.md`.
3. **Tự kiểm tra:** đếm số dòng file vừa sửa (`wc -l`). Vượt 150 dòng → tách theo
   [.claude/rules/memory-files.md](../../rules/memory-files.md).
4. **Báo lại đúng 1 dòng:** đã ghi vào file nào (dạng link). Không commit, không ghi PROGRESS.

## Không được
- Ghi secret/API key.
- Ghi những gì người học chưa thực sự nói ra (không tự bịa thêm "bài học").
