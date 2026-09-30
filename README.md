# learn-claude

Sổ học tập hành trình làm chủ Claude → AI Engineer (ứng dụng), có "trí nhớ" đồng bộ qua git.

## Cách dùng

```bash
git pull          # khi vừa chuyển máy
claude            # mở Claude Code trong thư mục này
/hoc-tiep         # Claude đọc memory/ và cho biết bạn đang ở đâu
...học...
/save-progress    # Claude cập nhật memory/
git add . && git commit -m "learn: ..." && git push
```

Nhờ mentor: *"dùng ai-mentor giảng về prompt caching"*, *"ai-mentor tạo lab tool use"*,
*"ai-mentor review labs/01-..."*, *"ai-mentor quiz mình"*.

## Cấu trúc

```
CLAUDE.md                     # Claude tự đọc mỗi phiên — dặn đọc memory/
memory/
  PROGRESS.md                 # đang ở đâu, bước tiếp theo (ghi đè)
  ROADMAP.md                  # lộ trình giai đoạn 0 → 9 (checklist)
  NOTES.md                    # mục lục kiến thức (1 dòng / chủ đề)
  notes/<chủ-đề>.md           # chi tiết từng chủ đề
  sessions/YYYY-MM-DD.md      # nhật ký từng phiên
labs/NN-<chủ-đề>/             # code thực hành
.claude/rules/memory-files.md # giới hạn độ dài file & cách tách
.claude/agents/ai-mentor.md   # subagent mentor
.claude/skills/hoc-tiep/      # /hoc-tiep
.claude/skills/save-progress/ # /save-progress
```
