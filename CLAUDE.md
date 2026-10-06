# learn-claude — Hành trình làm chủ Claude → AI Engineer (ứng dụng)

Repo này là "sổ học tập" của mình. Mình là developer, đang học Claude từ cơ bản đến nâng cao
theo hướng **AI Engineer ứng dụng** (xây sản phẩm dùng LLM, không phải nghiên cứu model).
Giao tiếp bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh.

## BẮT BUỘC khi bắt đầu mỗi phiên

1. Đọc [memory/PROGRESS.md](memory/PROGRESS.md) — mình đang ở đâu, đang làm gì, bước tiếp theo.
2. Đọc file mới nhất trong [memory/sessions/](memory/sessions/) — phiên gần nhất đã trao đổi gì.
3. Tham chiếu [memory/ROADMAP.md](memory/ROADMAP.md) khi cần biết lộ trình tổng thể.
4. Chào ngắn gọn: "Lần trước bạn dừng ở ..., hôm nay mình tiếp tục ... nhé?" — rồi mới làm việc.
   Nếu đầu phiên có output `git status` (từ hook SessionStart) báo file chưa commit → câu chào phải
   nhắc người học commit + push trước, liệt kê tên file. Áp dụng kể cả khi câu hỏi đầu không liên quan.

## Trong phiên

- Khi mình học xong một khái niệm, giải xong một bài tập, hoặc có một insight/"aha" → ghi nhớ để
  lưu vào memory lúc cuối phiên (hoặc lưu ngay nếu quan trọng).
- Kiến thức có giá trị lâu dài (giải thích khái niệm, pattern, gotcha) → ghi vào
  `memory/notes/<chủ-đề>.md` (ngắn gọn, có ví dụ code nếu cần) và thêm 1 dòng vào mục lục
  [memory/NOTES.md](memory/NOTES.md). Chỉ đọc file chủ đề khi cần, đừng đọc hết.
- Ngôn ngữ chính: **Python** (SDK `anthropic`). Mọi ví dụ và lab viết bằng Python, dùng `.venv`,
  dependencies ghi vào `requirements.txt`, đọc key qua `python-dotenv`.
- Code thực hành đặt trong `labs/<số>-<tên>/` (ví dụ `labs/01-messages-api/`), mỗi lab có README ngắn.
- Dạy theo kiểu mentor: giải thích "tại sao", cho ví dụ chạy được, rồi giao bài tập nhỏ.
  Đừng làm hộ hết — để mình tự code, chỉ gợi ý khi mình bí.
- Khi cần kiến thức chính xác về Claude API / Claude Code / Agent SDK, tra tài liệu chính thức
  thay vì đoán (model ID, giá, tham số thay đổi theo thời gian).

## Khi kết thúc phiên (hoặc khi mình gõ `/save-progress`)

Cập nhật memory theo skill `save-progress`:
- Tạo/cập nhật `memory/sessions/YYYY-MM-DD.md`
- Cập nhật `memory/PROGRESS.md` (trạng thái hiện tại + bước tiếp theo)
- Tick các mục đã xong trong `memory/ROADMAP.md`
- Nhắc mình `git add . && git commit && git push`

## Quy tắc memory

- Viết ngắn, cụ thể, đọc lại sau 1 tuần vẫn hiểu. Ngày tháng luôn ghi tuyệt đối (YYYY-MM-DD).
- Không lưu secret/API key vào bất kỳ file nào trong repo (dùng `.env`, đã gitignore).
- `PROGRESS.md` là trạng thái *hiện tại* — ghi đè, không phình ra. Lịch sử nằm ở `sessions/`.
- **Giới hạn độ dài:** CLAUDE.md < 100 dòng, file nào vượt giới hạn thì tách nhỏ. Bảng giới hạn chi tiết
  và cách tách ở [.claude/rules/memory-files.md](.claude/rules/memory-files.md), đọc trước khi tạo
  hoặc sửa file trong `memory/`, `labs/`, `.claude/`.
