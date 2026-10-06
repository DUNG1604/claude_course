# PROGRESS — Mình đang ở đâu?

> File này là trạng thái HIỆN TẠI. Claude đọc nó đầu mỗi phiên. Ghi đè khi cập nhật.

**Cập nhật lần cuối:** 2026-10-05 (máy công ty)

## Hồ sơ người học
- Vai trò: Developer, hướng tới **AI Engineer (ứng dụng)**
- Mục tiêu: làm chủ Claude từ cơ bản → nâng cao; xây được app/agent dùng LLM ở mức production
- Ngôn ngữ lập trình chính: **Python** (chuẩn hệ sinh thái AI) — labs dùng SDK `anthropic` cho Python
- Thời gian học: học ở công ty + về nhà học tiếp (đồng bộ qua git)

## Vị trí hiện tại
- **Giai đoạn:** 1 — Claude Code.
- **Khóa 1/8 Claude Code 101: ✅ HOÀN THÀNH 2026-10-06** (quiz 5/5). Bài giảng + lab:
  [labs/01-claude-code-101/](../labs/01-claude-code-101/README.md). Đã làm: hook SessionStart, skill `/til`,
  `check_env.py`. Quiz tự luận M2–M4 bỏ qua → đề ôn ở bai-giang-module-5.md §5.4.
- **Khóa 2/8: Claude Code in Action** (bắt đầu 2026-10-06) — lab [labs/02-claude-code-in-action/](../labs/02-claude-code-in-action/README.md).
  5 module: Steer the Work · Configure Claude · Automate Repeat Work · Verify and Share · Quiz.
  Đã soạn: [Module 1](../labs/02-claude-code-in-action/bai-giang-module-1.md) (queue, Esc, rewind, /goal).
  Tiếp theo: đọc Module 1 → làm checklist Module 1 trong lab (sân tập `playground/`) → Module 2.
  `.env` vẫn là key mẫu (check_env.py báo) — cần trước khóa API, chưa gấp.

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
- 2026-10-06: Người học thích **Claude viết file cấu hình/skill**, mình tập trung hiểu + kiểm chứng.
  → Mentor: viết hộ phần cấu hình được, nhưng luôn giải thích từng dòng và để người học tự kiểm chứng.

## Câu hỏi đang mở / điều còn mơ hồ (ôn lại bằng quiz)
- Checkpoint chỉ chụp file sửa qua tool Edit/Write → `rm` qua Bash không khôi phục được. Nhớ *vì sao*.
- Quy tắc bị quên sau compact → cách sửa: đưa vào CLAUDE.md (được nạp lại sau compact) /
  `/compact <trọng tâm>` / hook nếu bắt buộc. Chưa nêu được cách sửa cụ thể.
- Hay nghĩ "chat = chỉ model". Thực ra claude.ai cũng có harness; khác biệt là agent tự lặp trên môi trường của mình.
