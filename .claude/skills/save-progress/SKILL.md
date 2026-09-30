---
name: save-progress
description: Lưu tiến độ học của phiên hiện tại vào memory/ để đồng bộ qua git. Dùng khi người học gõ /save-progress, nói "lưu lại", "hôm nay tới đây", "mình về nhé", hoặc khi kết thúc một buổi học.
---

# Lưu tiến độ học

Mục tiêu: sau khi push, ở máy khác Claude đọc memory/ là biết chính xác người học đang ở đâu.

## Các bước

1. **Rà lại hội thoại phiên này**: đã học khái niệm gì, làm lab nào, gặp lỗi/insight gì,
   câu hỏi nào còn bỏ ngỏ, người học tự nói gì về bản thân (ngôn ngữ, sở thích, điểm yếu).

2. **Nhật ký phiên** — `memory/sessions/YYYY-MM-DD.md` (ngày hôm nay).
   Nếu file đã tồn tại (học nhiều lần trong ngày / ở hai máy) → **thêm** một mục mới
   `## Phiên 2 (máy ...)`, không ghi đè. Cấu trúc:
   - `## Đã làm` — gạch đầu dòng cụ thể, có đường dẫn file lab
   - `## Học được` — ý chính, ngắn; chi tiết đưa sang `memory/notes/`
   - `## Vướng mắc` (nếu có)
   - `## Bước tiếp theo`

3. **Kiến thức** — thêm vào đúng file `memory/notes/<chủ-đề>.md` (chưa có thì tạo file mới và thêm
   1 dòng vào mục lục `memory/NOTES.md`). Không lặp lại nội dung đã có.

4. **`memory/PROGRESS.md`** — **ghi đè** trạng thái hiện tại: ngày cập nhật, giai đoạn,
   đang làm gì, 1–3 bước tiếp theo cụ thể, câu hỏi đang mở. Cập nhật "Hồ sơ người học" nếu
   biết thêm điều gì. Giữ file ngắn (< 60 dòng).

5. **`memory/ROADMAP.md`** — tick `[x]` các mục đã thật sự học + thực hành. Có thể thêm mục
   con nếu người học đi sâu vào thứ không có sẵn.

6. **Kiểm tra**:
   - Không có API key/secret nào trong các file vừa sửa.
   - Độ dài file: chạy `find . -name "*.md" -not -path "./.venv/*" | xargs wc -l | sort -n` rồi so với
     bảng giới hạn trong `.claude/rules/memory-files.md`. File nào vượt thì **tách ngay** theo cột
     "Vượt thì làm gì", rồi Grep để sửa các link cũ. Báo lại cho người học biết đã tách những file nào.

7. **Báo lại** ngắn gọn những gì đã lưu, rồi đưa lệnh git để người học tự chạy:
   ```
   git add .
   git commit -m "learn: <tóm tắt phiên>"
   git push
   ```
   Chỉ tự chạy commit/push nếu người học yêu cầu rõ.
