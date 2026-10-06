# Lab 01 — Claude Code 101 (thực hành song song khóa học)

Khóa: https://anthropic.skilljar.com/claude-code-101 · Chỉ cần subscription, không tốn API credits.

**Cách học:** xem xong module nào → làm ngay phần tương ứng dưới đây → tick `[x]`.
Chưa hiểu chỗ nào thì hỏi thẳng Claude trong repo này.

---

## Module 1–2 — Claude Code là gì · Cài đặt · Prompt đầu tiên

- [ ] Ngoài extension VS Code, cài thêm **CLI** theo bài "Installing Claude Code", mở terminal
      trong repo và chạy `claude`. Gõ `/help` xem có những lệnh gì.
- [ ] Prompt đầu tiên: *"Repo này dùng để làm gì? Mình đang học tới đâu?"*
      → Quan sát: Claude có tự đọc `CLAUDE.md` và `memory/` không? Nó dùng những tool nào?
- [ ] Tự trả lời (ghi vào phần "Rút ra" cuối file): Claude Code khác chat trên claude.ai ở điểm nào?
      "Agentic loop" (vòng lặp agent) nghĩa là gì?

## Module 3 — Daily workflows

**Explore → Plan → Code → Commit.** Nhờ Claude làm script `check_env.py` trong thư mục này. Script
kiểm tra `.env` có `ANTHROPIC_API_KEY` chưa và key có đúng dạng `sk-ant-` không, **nhưng không bao
giờ in key ra màn hình**.
- [ ] **Explore:** yêu cầu Claude đọc `.env.example` và `requirements.txt` trước, *chưa được code*.
- [ ] **Plan:** bật Plan mode (`Shift+Tab` trong CLI), duyệt kế hoạch, sửa ít nhất 1 điểm rồi mới cho code.
- [ ] **Code:** chạy thử `.\.venv\Scripts\python.exe labs\01-claude-code-101\check_env.py`.
- [ ] **Commit:** nhờ Claude viết commit message rồi commit.

**Context management**
- [ ] Gõ `/context` xem context window đang chứa những gì.
- [ ] Thử `/compact` và `/clear`. Tự ghi lại: khi nào dùng lệnh nào? Dùng `/clear` xong mất gì?

**Code review**
- [ ] Nhờ Claude review `check_env.py` (hoặc `/code-review`). Có lỗi nào bạn không tự thấy không?

## Module 4 — Tùy biến Claude Code (repo này có sẵn ví dụ để mổ xẻ)

- [x] **CLAUDE.md:** đọc [CLAUDE.md](../../CLAUDE.md), tự thêm 1 quy tắc của riêng bạn. Mở phiên mới
      và kiểm tra Claude có làm theo không.
- [ ] **Subagents:** đọc [ai-mentor.md](../../.claude/agents/ai-mentor.md). Gõ `/agents` xem danh sách
      agent. Nhờ *"ai-mentor giảng lại cho mình về context window"*.
      → Ghi lại: subagent có thấy lịch sử hội thoại chính không? Vì sao điều đó hữu ích?
- [ ] **Skills:** đọc [save-progress](../../.claude/skills/save-progress/SKILL.md). **Tự tạo** skill
      `/til` ("today I learned"): nhận 1 câu, thêm vào đúng file `memory/notes/<chủ-đề>.md` (cập nhật mục lục NOTES.md nếu tạo file mới).
- [ ] **Rules:** đọc [.claude/rules/memory-files.md](../../.claude/rules/memory-files.md). Rule này có
      `paths:` nên chỉ được nạp khi Claude đọc file khớp. Chạy `/context` trước và sau khi nhờ Claude đọc
      một file trong `memory/` để thấy rule được nạp lúc nào.
- [ ] **MCP:** chạy `claude mcp list`. Tự trả lời: MCP server khác tool có sẵn ở điểm nào?
- [x] **Hooks:** tạo hook `SessionStart` trong `.claude/settings.json` chạy `git status --short`,
      để mỗi lần mở phiên thấy ngay còn thay đổi nào chưa commit hoặc push (hữu ích khi học ở 2 máy).
      Không làm được thì nhờ Claude, nhưng phải hiểu từng dòng.

## Module 5 — Assessment

- [ ] Làm quiz của khóa.
- [ ] Nhờ *"ai-mentor quiz mình về Claude Code 101"*. Câu nào sai sẽ được ghi vào PROGRESS.
- [ ] Gõ `/save-progress` rồi push.

## Tiêu chí hoàn thành
- `check_env.py` chạy được, không lộ key, đã commit.
- Có skill `/til` và hook `SessionStart` do bạn tạo, dùng được.
- Trả lời được bằng lời của mình: CLAUDE.md, subagent, skill, MCP, hook — mỗi thứ dùng khi nào.

---

## Rút ra (tự ghi)
-
