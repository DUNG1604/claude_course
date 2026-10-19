# PROGRESS — Mình đang ở đâu?

> File này là trạng thái HIỆN TẠI. Claude đọc nó đầu mỗi phiên. Ghi đè khi cập nhật.

**Cập nhật lần cuối:** 2026-10-19 (máy công ty)

## Hồ sơ người học
- Vai trò: Developer, hướng tới **AI Engineer (ứng dụng)**
- Mục tiêu: làm chủ Claude từ cơ bản → nâng cao; xây được app/agent dùng LLM ở mức production
- Ngôn ngữ lập trình chính: **Python** (chuẩn hệ sinh thái AI) — labs dùng SDK `anthropic` cho Python
- Thời gian học: học ở công ty + về nhà học tiếp (đồng bộ qua git)
- Thích Claude viết file cấu hình/skill, mình hiểu + kiểm chứng. Hay bỏ qua quiz tự luận và phần "tự ghi".
  Hay quên `/save-progress` cuối phiên (10-09 phải ghi bù).

## Vị trí hiện tại
- **Giai đoạn:** 1 — Claude Code. Khóa 1/8 Claude Code 101 ✅ (2026-10-06, quiz 5/5).
- **Khóa 2/8: Claude Code in Action** — lab [labs/02-claude-code-in-action/](../labs/02-claude-code-in-action/README.md).
  Đã soạn đủ bài giảng Module 1–4.
  - M1 ✅ 5/6 bài (thiếu phần tự ghi).
  - M2: xong deny rule force-push + skill `/kiem-tra-memory`; bỏ qua audit CLAUDE.md, auto mode.
  - M3: mới thử `/loop`; bỏ qua headless/CI/routine/`@claude` (2026-10-09).
  - M4: **chưa làm** (Stop hook, đọc transcript `-p`, đóng gói plugin).
  - M5: quiz chưa làm.
- `.env` vẫn là key mẫu — cần trước khóa API, chưa gấp.

## Bước tiếp theo (làm ngay phiên sau)
1. Lab M4 trong CLI: ít nhất **Stop hook chốt test** + **đóng gói plugin local**.
2. Quiz Module 5 trên Skilljar → đóng khóa 2.
3. Trước khóa "Building with the Claude API": nạp API credits ở Console + đặt spend limit, dán key vào `.env`.

## Quyết định đã chốt
- 2026-09-30: Ngôn ngữ = Python. Nguồn học = khóa chọn lọc của Anthropic Academy (thứ tự trong
  ROADMAP.md) + lab tự làm trong `labs/`.
- Tài khoản: có **subscription Claude**, chưa có API credits.
- 2026-10-06: Mentor được viết hộ phần cấu hình, nhưng luôn giải thích từng dòng và để người học tự kiểm chứng.

## Câu hỏi đang mở / điều còn mơ hồ (ôn lại bằng quiz)
- Checkpoint chỉ chụp file sửa qua tool Edit/Write → `rm` qua Bash không khôi phục được. Nhớ *vì sao*.
- Quy tắc bị quên sau compact → cách sửa: đưa vào CLAUDE.md (được nạp lại sau compact) /
  `/compact <trọng tâm>` / hook nếu bắt buộc. Chưa nêu được cách sửa cụ thể.
- Hay nghĩ "chat = chỉ model". Thực ra claude.ai cũng có harness; khác biệt là agent tự lặp trên môi trường của mình.
