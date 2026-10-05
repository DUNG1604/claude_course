# PROGRESS — Mình đang ở đâu?

> File này là trạng thái HIỆN TẠI. Claude đọc nó đầu mỗi phiên. Ghi đè khi cập nhật.

**Cập nhật lần cuối:** 2026-10-05 (máy công ty)

## Hồ sơ người học
- Vai trò: Developer, hướng tới **AI Engineer (ứng dụng)**
- Mục tiêu: làm chủ Claude từ cơ bản → nâng cao; xây được app/agent dùng LLM ở mức production
- Ngôn ngữ lập trình chính: **Python** (chuẩn hệ sinh thái AI) — labs dùng SDK `anthropic` cho Python
- Thời gian học: học ở công ty + về nhà học tiếp (đồng bộ qua git)

## Vị trí hiện tại
- **Giai đoạn:** 1 — Claude Code · Khóa 1/8: **Claude Code 101** (bắt đầu 2026-09-30)
- **Đang làm:** [labs/01-claude-code-101/README.md](../labs/01-claude-code-101/README.md) —
  checklist thực hành theo 5 module. Xem các ô đã tick trong file đó để biết đang ở module nào.
- **Bài giảng đã soạn:** [Module 1](../labs/01-claude-code-101/bai-giang-module-1.md),
  [Module 2](../labs/01-claude-code-101/bai-giang-module-2.md) (2026-09-30).
  [Module 3](../labs/01-claude-code-101/bai-giang-module-3.md),
  [Module 4](../labs/01-claude-code-101/bai-giang-module-4.md) (2026-10-01),
  [Module 5 — tổng kết + đề ôn](../labs/01-claude-code-101/bai-giang-module-5.md) (2026-10-05).
  **Lý thuyết khóa 1 đã xong** (2026-10-05). Người học bỏ qua quiz M2–M4 → gom vào đề ôn §5.4.
  **Chưa làm thực hành** (§5.3): check_env.py, skill `/til`, hook SessionStart, quiz Skilljar.
  Repo đã có commit (3 commit tính tới 2026-10-05).
  Tiếp theo: làm thực hành §5.3 rồi mới tick khóa 1 → sang khóa 2 "Claude Code in Action".

## Bước tiếp theo (làm ngay phiên sau)
1. Push repo lên GitHub, clone về máy nhà, chạy `claude` trong thư mục và gõ `/hoc-tiep`.
2. Máy công ty đã có Python 3.12 + `.venv` + thư viện; còn thiếu: dán API key vào `.env`.
   Máy nhà: cài Python 3.12 → `python -m venv .venv` → `pip install -r requirements.txt` → tạo `.env`.
3. Bắt đầu Giai đoạn 1 = khóa **Claude Code 101** trên Anthropic Academy (chỉ cần subscription).
4. Trước khi tới khóa "Building with the Claude API": nạp API credits ở Console + đặt spend limit.

## Quyết định đã chốt
- 2026-09-30: Ngôn ngữ = Python. Nguồn học = khóa chọn lọc của Anthropic Academy (thứ tự trong
  ROADMAP.md) + lab tự làm trong `labs/`.
- Tài khoản: có **subscription Claude**, chưa có API credits.

## Câu hỏi đang mở / điều còn mơ hồ (ôn lại bằng quiz)
- Checkpoint chỉ chụp file sửa qua tool Edit/Write → `rm` qua Bash không khôi phục được. Nhớ *vì sao*.
- Quy tắc bị quên sau compact → cách sửa: đưa vào CLAUDE.md (được nạp lại sau compact) /
  `/compact <trọng tâm>` / hook nếu bắt buộc. Chưa nêu được cách sửa cụ thể.
- Hay nghĩ "chat = chỉ model". Thực ra claude.ai cũng có harness; khác biệt là agent tự lặp trên môi trường của mình.
