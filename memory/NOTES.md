# NOTES — Mục lục kiến thức

> Chỉ là **index**: 1 dòng cho 1 chủ đề. Chi tiết nằm trong `memory/notes/<chủ-đề>.md`.
> Thêm kiến thức: sửa file chủ đề có sẵn, hoặc tạo file mới rồi thêm 1 dòng vào đây.

## Khái niệm AI Engineering
- [Harness](notes/harness.md): model = não, tools = tay, harness = cơ thể + hệ thần kinh
- [Agentic loop](notes/agentic-loop.md): vòng `while` gọi API, `stop_reason`, `tool_result`, API stateless

## Claude Code
- [Cấu trúc `.claude/`](notes/claude-code-structure.md): CLAUDE.md, rules, agents, skills, MCP, hooks; lời dặn vs luật; kèm gotcha
- [Quản lý context](notes/context-management.md): /clear vs /compact, cái gì còn hoặc mất sau compact
- [Giới hạn độ dài file](notes/gioi-han-do-dai-file.md): CLAUDE.md < 200, SKILL.md < 500, mục lục khi > 100 dòng

## Tài khoản & môi trường
- [Subscription vs API](notes/subscription-vs-api.md): hai hệ thống tính tiền riêng, gotcha `ANTHROPIC_API_KEY`
- [Python trên Windows](notes/python-env-windows.md): cài bằng winget, venv, execution policy
