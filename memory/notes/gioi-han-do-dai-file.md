# Giới hạn độ dài file (theo tài liệu Anthropic)

Nguồn: [Memory docs](https://code.claude.com/docs/en/memory),
[Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). Tra 2026-09-30.

| File | Giới hạn | Vì sao |
|---|---|---|
| `CLAUDE.md` | **< 200 dòng** mỗi file | Dài hơn thì tốn context và Claude làm theo kém đi. File > 4 MiB bị bỏ qua |
| `MEMORY.md` (auto memory) | **200 dòng hoặc 25KB đầu** được nạp | Phần sau bị cắt, không nạp. Nên chỉ để index, 1 dòng/mục |
| `SKILL.md` | **< 500 dòng** | Vượt thì tách ra file tham chiếu |
| File tham chiếu > **100 dòng** | Phải có **mục lục ở đầu** | Claude có thể chỉ đọc một phần (`head`), mục lục cho nó thấy toàn bộ phạm vi |
| Tham chiếu từ skill | **Sâu 1 cấp** | A → B → C thì Claude dễ đọc thiếu C |

Ý chính:
- **`@import` không tiết kiệm context**: file import vẫn nạp lúc khởi động. Nó chỉ giúp tổ chức.
- Muốn tiết kiệm thật thì dùng **file nạp theo nhu cầu**: skill (chỉ nạp khi dùng), rule có `paths:`
  (chỉ nạp khi đọc file khớp), hoặc file thường để Claude tự Read khi cần.
- Pattern **index + topic files**: file chính chỉ là mục lục ngắn, chi tiết để ở file con. Auto memory
  của Claude Code làm đúng như vậy, và `memory/NOTES.md` của repo này cũng thế.
- `/doctor prompt-audit`: nhờ Claude soát các file chỉ dẫn xem có mâu thuẫn hoặc lỗi thời không.
- Quy tắc áp dụng trong repo: [.claude/rules/memory-files.md](../../.claude/rules/memory-files.md).
