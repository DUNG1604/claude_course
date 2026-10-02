# Quản lý context trong Claude Code

Chi tiết: [bài giảng Module 3](../../labs/01-claude-code-101/bai-giang-module-3.md) §3.4–3.5.

- Đọc 1 file code tốn ~1.000–2.500 token, là thứ làm đầy context nhanh nhất. System prompt ~4.200.
- `/clear`: đổi sang việc không liên quan (mất hội thoại, CLAUDE.md nạp lại).
  `/compact <trọng tâm>`: đang giữa việc dài. `/btw`: hỏi nhanh, không vào lịch sử.
  `/rewind` → Summarize from/up to here: nén một phần. Subagent: đọc nhiều file ở context riêng.
- **Sau compact:** CLAUDE.md gốc + rule không có `paths:` + plan + auto memory → nạp lại từ đĩa.
  Rule có `paths:`, CLAUDE.md thư mục con → mất tới khi đọc lại file khớp. Chỉ dẫn chỉ nói trong
  chat → chỉ còn trong bản tóm tắt. Skill bị cắt còn 5.000 token → để ý chính ở đầu SKILL.md.
- Sửa sai 2 lần vẫn không được → `/clear` + prompt mới tốt hơn (context đã đầy các cách làm hỏng).
