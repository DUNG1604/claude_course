---
paths:
  - "memory/**"
  - "labs/**"
  - ".claude/**"
  - "CLAUDE.md"
---

# Quy tắc độ dài & tách file

Ⓐ = giới hạn Anthropic khuyến nghị · Ⓡ = quy ước riêng của repo này (chặt hơn để dễ đọc lại).

| File | Giới hạn | Vượt thì làm gì |
|---|---|---|
| `CLAUDE.md` | Ⓐ < 200 · Ⓡ < 100 dòng | Chuyển phần chỉ liên quan một nhóm file sang `.claude/rules/<chủ-đề>.md` có `paths:`; quy trình nhiều bước → skill |
| `.claude/skills/*/SKILL.md` | Ⓐ < 500 dòng | Tách chi tiết ra file cạnh SKILL.md, link trực tiếp (sâu 1 cấp) |
| `.claude/agents/*.md`, `.claude/rules/*.md` | Ⓡ < 150 dòng | Tách theo chủ đề |
| `memory/PROGRESS.md` | Ⓡ < 60 dòng | Chỉ giữ trạng thái hiện tại; lịch sử → `sessions/` |
| `memory/NOTES.md` (index) | Ⓐ < 200 dòng (như MEMORY.md) | 1 dòng / chủ đề; gom chủ đề thành nhóm lớn hơn |
| `memory/notes/<chủ-đề>.md` | Ⓡ < 150 dòng | Tách thành chủ đề con, ví dụ `notes/tool-use-basics.md` + `notes/tool-use-advanced.md` |
| `memory/ROADMAP.md` | Ⓡ < 200 dòng | Tách mỗi giai đoạn thành `memory/roadmap/giai-doan-N.md`, ROADMAP.md giữ bảng tổng |
| `memory/sessions/YYYY-MM-DD.md` | Ⓡ < 150 dòng | Viết gọn lại; chi tiết kiến thức chuyển sang `notes/` |
| Bài giảng `labs/**/bai-giang-*.md` | Ⓡ 1 module/file, < 250 dòng | Tách theo module hoặc bài |

Quy tắc chung:
- Ⓐ File nào > 100 dòng (trừ CLAUDE.md) phải có **mục lục** ở đầu.
- Ⓐ Link giữa các file chỉ **sâu 1 cấp** tính từ file index (index → file con, không đi tiếp).
- Tên file mô tả nội dung, kebab-case (`tool-use-basics.md`, không phải `notes2.md`).
- Tách file xong phải cập nhật **mọi link** trỏ tới nội dung cũ (dùng Grep để tìm).
- Kiểm tra nhanh: skill `/kiem-tra-memory` (script so với bảng trên). Đổi giới hạn ở đây → sửa luôn
  `LIMITS` trong `.claude/skills/kiem-tra-memory/check_lengths.py`.
