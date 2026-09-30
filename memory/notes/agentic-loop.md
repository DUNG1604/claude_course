# Agentic loop — vòng lặp gọi API bên dưới mọi agent

```python
messages = [{"role": "user", "content": "fix the failing tests"}]
while True:
    resp = client.messages.create(model=..., tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":
        break
    results = [
        {"type": "tool_result", "tool_use_id": b.id, "content": run_tool(b.name, b.input)}
        for b in resp.content if b.type == "tool_use"
    ]
    messages.append({"role": "user", "content": results})
```

## Ý chính
- **API không có trí nhớ (stateless).** Mỗi lần gọi phải gửi lại toàn bộ `messages`. `messages`
  chính là "cuốn sổ" harness giữ hộ model.
- `while True`: số vòng không biết trước, **model tự quyết khi nào dừng** (khác script thường).
- `tools=TOOLS`: "menu" tool gồm tên, mô tả, JSON schema tham số. Model chỉ *yêu cầu* gọi tool.
- `stop_reason`: `"tool_use"` → chạy tool rồi lặp tiếp · `"end_turn"` → xong · `"max_tokens"` → bị cắt,
  code thật phải xử lý.
- `run_tool` là **hàm mình tự viết**, chỗ harness làm việc thật (đọc file, chạy lệnh...). Model có thể
  yêu cầu nhiều tool trong 1 lượt → list kết quả.
- Kết quả tool gửi lại với `role: "user"` (API chỉ có 2 vai) và phải kèm `tool_use_id` để khớp với
  yêu cầu tương ứng.

## Ví dụ liền mạch ("fix the failing tests")

Mắt xích nối các vòng = **cuốn sổ `messages`**. Model không nhớ vòng trước; nó biết bước tiếp theo
chỉ vì harness **ghi kết quả tool vào sổ rồi gửi lại cả sổ**.

```
Bạn gõ → sổ [1 mục] → API lần 1 → Model: tool_use bash("pytest")
→ Harness chạy pytest → "FAILED ... calc.py:2 ... got 5" → ghi tool_result vào sổ [3 mục]
→ API lần 2 → Model thấy "calc.py:2" → tool_use read_file("calc.py")            (gather)
→ Harness đọc file → "return a+b+1" → ghi sổ [5 mục]
→ API lần 3 → Model: "+1 thừa" → tool_use edit_file(...)                        (act)
→ Harness sửa file → ghi sổ [7 mục]
→ API lần 4 → Model: "phải kiểm tra lại" → tool_use bash("pytest")              (verify)
→ Harness chạy → "1 passed" → ghi sổ [9 mục]
→ API lần 5 → Model: text "Đã sửa..." + end_turn → ghi sổ [10 mục] → break
```

Luồng duy nhất: `Model → Harness → Tool → Harness → ghi sổ → gửi cả sổ → Model`.
⚠️ Lúc đầu mình nhìn bảng tóm tắt tưởng các vòng rời nhau. Thiếu bước "harness ghi tool_result vào sổ".

## Hệ quả
- Context đầy nhanh vì `messages` chỉ dài ra, và **lần nào cũng gửi lại hết**. Đó là lý do cần
  `/clear` và `/compact`.
- Harness = vòng lặp này + tools thật + hỏi quyền trước `run_tool` + tóm tắt `messages` + lưu session.
- Mỗi tool call hiện trong Claude Code = 1 vòng của đoạn code trên → quan sát để học thiết kế agent.
- Sẽ tự code bản chạy thật ở Giai đoạn 4 (tool use). Liên quan: [harness.md](harness.md).
