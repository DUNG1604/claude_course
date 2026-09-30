# Claude Code — Cấu trúc thư mục `.claude/`

| Thứ | Vị trí | Dùng để |
|---|---|---|
| `CLAUDE.md` | gốc repo (hoặc `~/.claude/CLAUDE.md` cho mọi project) | Chỉ dẫn Claude tự đọc **mỗi phiên** |
| Rules | `.claude/rules/*.md` | Chỉ dẫn tách nhỏ; có `paths:` thì chỉ nạp khi Claude đọc file khớp |
| Subagent | `.claude/agents/<tên>.md` | Một "Claude con" có system prompt + tools riêng, chạy trong context riêng |
| Skill | `.claude/skills/<tên>/SKILL.md` | Bộ hướng dẫn tái sử dụng, gọi bằng `/<tên>` hoặc Claude tự dùng khi hợp |
| Settings/Hooks | `.claude/settings.json` | Permissions, hooks, env |

- **Gotcha:** memory mặc định của Claude Code nằm trong `~/.claude/projects/...` trên từng máy →
  **không** đi theo git. Muốn đồng bộ giữa các máy thì để memory trong repo (như repo này) và
  dặn trong `CLAUDE.md` là phải đọc nó.
- **Gotcha:** đặt tên skill đừng trùng lệnh built-in. Skill `resume` trùng `/resume` (lệnh mở lại
  hội thoại cũ) → đã đổi thành `/hoc-tiep`.
- **Gotcha:** subagent/skill mới tạo có thể cần mở lại phiên `claude` mới nhận.
- Subagent vs Skill: subagent = *tách context* (việc dài, không muốn làm bẩn hội thoại chính);
  skill = *quy trình/chỉ dẫn* chạy ngay trong hội thoại chính.
