# Stop hook — chỉ cho Claude dừng khi test xanh

Lab: `labs/02-claude-code-in-action/` Module 4 §4.4 (làm 2026-10-22).
File: `.claude/hooks/chot_test.py` + `labs/02-claude-code-in-action/stop-hook.json`.

## Cơ chế
- `Stop` chạy khi Claude **sắp kết thúc turn** (mọi turn, kể cả chỉ trả lời câu hỏi → test phải nhanh).
- Input: JSON qua **stdin** (`session_id`, `transcript_path`, `cwd`, `stop_hook_active`...).
- **exit 2** → chặn dừng, **stderr** thành feedback cho Claude. exit 0 → cho dừng.
- `stop_hook_active == True` = turn này đã bị chặn 1 lần → script `exit 0` để tránh vòng lặp vô hạn.
  Bỏ check này thì Claude Code vẫn tự gỡ sau 8 lần chặn liên tiếp (không tool call xen giữa).
- Claude **không thấy code hook**, chỉ thấy stderr → nó có thể đoán sai về hook.

## Bật hook chỉ 1 phiên
```
claude --settings labs/02-claude-code-in-action/stop-hook.json   # đứng ở gốc repo
```
- Settings chỉ tự nạp từ đường dẫn cố định: `~/.claude/settings.json`, `.claude/settings.json`,
  `.claude/settings.local.json`. File JSON ở chỗ khác = file thường, chỉ nạp khi `--settings`.
- Script trong `.claude/hooks/` **không tự chạy**: phải có settings đang nạp trỏ `command` tới nó.
- `--settings` **cộng thêm** vào các tầng có sẵn (deny rule vẫn còn), thoát phiên là mất.
- Kiểm tra: `/hooks`.

## Kết quả thí nghiệm (test sai, code đúng)
Cố ý sửa test `count_words("Xin chào thế giới") == 5` (đúng là 4). Hook chặn → Claude **không sửa gì**,
giải thích test sai và hỏi người. Lần 2 hook cho dừng nhờ `stop_hook_active`.
→ **Hook chỉ biết exit code, không biết test hay code sai.** Lời dặn "không sửa test" chỉ đúng khi test đúng;
model kém hơn có thể làm hỏng code để test xanh → vẫn cần reviewer (§4.5).

## Gotcha Windows
- In tiếng Việt ra stderr → `sys.stderr.reconfigure(encoding="utf-8")`, không thì `UnicodeEncodeError`.
- Process con (unittest) ghi theo cp1252 → output vỡ `ch�o`. Sửa: `env={**os.environ, "PYTHONIOENCODING": "utf-8"}`.
- Dùng `$CLAUDE_PROJECT_DIR` trong `command` và `cwd` để không phụ thuộc thư mục đang đứng.
