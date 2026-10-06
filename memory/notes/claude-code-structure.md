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
- **Gotcha — khi nào thay đổi có hiệu lực:** skill mới tạo được harness **nhận ngay** trong phiên đang chạy
  (đã thấy 2026-10-06 với `/til`). Hook trong `settings.json` thì **phải mở phiên mới** (hook `SessionStart`
  đã lỡ lúc mở phiên thì không chạy bù). Subagent mới: nếu không thấy thì mở phiên mới.
- **CLAUDE.md nhiều cấp = cộng dồn, không ghi đè:** `~/.claude/CLAUDE.md` (mọi project) + CLAUDE.md từ thư mục
  chạy `claude` đi **ngược lên** (nạp lúc mở phiên) + CLAUDE.md thư mục **con** (chỉ nạp khi Claude đụng file
  trong đó, mất sau compact). Mâu thuẫn thì Claude tự cân nhắc → đừng viết mâu thuẫn. Skill/subagent thì ngược
  lại: trùng tên → 1 bản thắng.
- **Thư mục tự đặt (vd `inventory/`) không bao giờ tự nạp.** Phải có chuỗi link bắt đầu từ thứ *tự nạp*
  (CLAUDE.md / rule / description skill) → index → file chi tiết, sâu 1 cấp. Link markdown chỉ là gợi ý,
  Claude tự Read khi thấy cần; chỉ `@import` mới nạp thật (và nạp toàn bộ). Câu dặn phải có điều kiện "khi nào".
- **Lời dặn vs luật:** CLAUDE.md/skill = lời dặn (Claude có thể quên/bỏ qua). Hook = luật, harness luôn
  chạy. Bắt buộc 100% (vd cấm sửa `.env`) → hook `PreToolUse` exit 2. Chi tiết: [Module 4](../../labs/01-claude-code-101/bai-giang-module-4.md).
- Hook `SessionStart` + matcher `compact`: stdout được bơm lại vào context sau compact → cách chữa quy tắc bị quên.
- MCP = thêm tool để chạm hệ thống ngoài; đầu phiên chỉ nạp tên tool. Skill = dạy cách dùng tool đó.
- Subagent vs Skill: subagent = *tách context* (việc dài, không muốn làm bẩn hội thoại chính);
  skill = *quy trình/chỉ dẫn* chạy ngay trong hội thoại chính.
