# Bài giảng — Claude Code in Action · Module 1: Steer the Work

> Nguồn: [Interactive mode](https://code.claude.com/docs/en/interactive-mode),
> [Checkpointing](https://code.claude.com/docs/en/checkpointing), [/goal](https://code.claude.com/docs/en/goal).
> Soạn 2026-10-06. Nối tiếp khóa 1 (Module 3: Explore → Plan → Code → Commit).

**Mục lục**
- 1.1 Vì sao phiên dài khó lái
- 1.2 Trước khi chạy: chốt plan và điều kiện "xong"
- 1.3 Trong khi chạy: queue, /btw, Esc
- 1.4 Khi lệch hướng: rewind, branch, làm lại
- 1.5 /goal: để Claude tự chạy tới khi đạt điều kiện
- 1.6 Bảng chọn nhanh

Tiếp theo: [Module 2](bai-giang-module-2.md) · Thực hành: [README lab, phần Module 1](README.md)

---

### 1.1 Vì sao phiên dài khó lái

Khóa 1 dạy làm **một task ngắn**: bạn prompt → Claude làm → bạn xem. Khóa 2 hướng tới **task dài**:
Claude chạy 20–50 tool call, có khi hàng giờ. Khi đó có 3 vấn đề:

1. **Lệch hướng (drift):** hiểu sai từ bước 3 → 40 bước sau đều sai theo.
2. **Context đầy:** càng dài càng quên chỉ dẫn đầu phiên (ràng buộc 1 của khóa 1).
3. **Dừng sớm hoặc dừng sai:** Claude tự cho là xong (ràng buộc 2).

→ Module này là bộ "vô lăng" cho 3 thời điểm: **trước**, **trong**, và **sau khi lệch**.

### 1.2 Trước khi chạy: chốt plan và điều kiện "xong"

Rẻ nhất là sửa trước khi chạy:
- **Plan mode** (`Shift+Tab`): Claude đọc + lập plan, chưa sửa gì. Duyệt plan là chỗ bắt lỗi hiểu sai.
- **Sửa plan trực tiếp:** `Ctrl+G` mở prompt/plan trong text editor, sửa nhiều dòng thoải mái hơn gõ chat.
- **Nói rõ "xong" nghĩa là gì**, có lệnh kiểm chứng: *"xong khi `python -m unittest` exit 0 và không sửa test
  cũ"*. Không có điều này thì mọi công cụ ở 1.5 cũng vô dụng.

### 1.3 Trong khi chạy: queue, /btw, Esc

Bạn **không phải đợi** Claude làm xong mới được nói:

| Muốn | Làm | Điều gì xảy ra |
|---|---|---|
| Bổ sung yêu cầu, **không dừng** Claude | Gõ tin nhắn + `Enter` khi Claude đang chạy (**queue**) | Tin nhắn vào hàng đợi. Claude nhận nó **ngay sau loạt tool call hiện tại, trong cùng turn** |
| Gửi ngay không chờ | `Ctrl+Enter` | Đẩy hàng đợi đi luôn |
| Rút lại tin đã queue | `Up` ở dòng đầu ô nhập | Tin quay về ô nhập để sửa/xóa |
| Hỏi bên lề, không làm bẩn lịch sử | `/btw <câu hỏi>` | Trả lời riêng, **không có tool**, không gián đoạn turn, không vào lịch sử |
| **Dừng ngay** vì đang sai | `Esc` (hoặc `Ctrl+C`) | Turn bị ngắt; tin đã queue được gửi luôn |
| Xem Claude đang làm gì | `Ctrl+T` (danh sách task), `Ctrl+O` (transcript chi tiết) | Chỉ xem |
| Lệnh chạy lâu chặn đường | `Ctrl+B` | Đẩy Bash/agent xuống chạy nền |

**Nguyên tắc chọn:** Claude đi đúng hướng nhưng thiếu chi tiết → **queue**. Claude đi sai hướng → **Esc** ngay,
đừng để nó chạy thêm 10 bước sai rồi mới sửa.

Liên hệ khóa 1: queue hoạt động được vì [agentic loop](../../memory/notes/agentic-loop.md) — sau mỗi lượt
`tool_result`, harness chèn thêm tin nhắn của bạn vào cuốn sổ `messages` trước khi gửi lại cho model.

### 1.4 Khi lệch hướng: rewind, branch, làm lại

**`/rewind`** (hoặc `Esc Esc` khi ô nhập trống) — mỗi prompt bạn gửi tạo một checkpoint. Menu cho phép:

| Lựa chọn | Code | Hội thoại | Dùng khi |
|---|---|---|---|
| Restore code and conversation | Quay lại | Quay lại | Làm lại từ đầu bước đó với prompt tốt hơn |
| Restore conversation | Giữ nguyên | Quay lại | Code ổn, muốn hỏi theo hướng khác |
| Restore code | Quay lại | Giữ nguyên | Code hỏng nhưng muốn Claude nhớ "cách này sai" |
| Summarize from here / up to here | Giữ nguyên | **Nén** một phần | Giải phóng context (như `/compact` có chọn lọc) |

⚠️ **Rewind không cứu được:**
- File sửa bằng **Bash** (`rm`, `mv`, `cp`, script) — chỉ Edit/Write được theo dõi.
- Sửa của **subagent** (thường) và sửa bạn tự làm ngoài Claude Code.
- Tin nhắn **queue giữa turn** không có checkpoint riêng → phải rewind cả turn.
→ Checkpoint là "Ctrl+Z trong phiên", **không thay git**. Việc dài → commit thường xuyên.

**Thử hướng khác mà giữ bản gốc:** `/branch` (rẽ nhánh hội thoại).

> **VS Code extension:** không có `/branch`, `Esc Esc`. Thay vào đó **hover lên một tin nhắn → nút rewind**:
> *Fork conversation from here* (≈ /branch) · *Rewind code to here* (≈ Restore code) ·
> *Fork conversation and rewind code*. Extension chỉ có **một phần** lệnh `/` — cần đủ thì chạy `claude` (CLI). **Sai 2 lần** → `/clear` + prompt tốt hơn
(khóa 1, Module 3).

### 1.5 /goal: để Claude tự chạy tới khi đạt điều kiện

Bình thường Claude dừng khi **nó** thấy xong. `/goal <điều kiện>` thêm một **người chấm riêng**:

```
/goal python -m unittest exits 0, có ít nhất 8 test, không sửa test cũ — hoặc dừng sau 10 turn
```

Cơ chế: sau mỗi turn, một model nhỏ, nhanh (evaluator) đọc điều kiện + hội thoại và trả verdict:
- **Not yet met** → Claude tự làm turn tiếp, dùng lý do làm gợi ý.
- **Met** → goal tự xóa, ghi "achieved".
- **Impossible** → goal tự xóa, ghi lý do.

Thực chất `/goal` là một **Stop hook dạng prompt** gắn vào phiên — đúng thứ bạn học ở khóa 1, Module 4.

**Viết điều kiện tốt** — evaluator **không chạy lệnh, không đọc file**, chỉ đọc những gì Claude đã in ra:
- **Một trạng thái đo được:** test pass, exit code, số file, hàng đợi rỗng.
- **Cách chứng minh:** "`python -m unittest` exits 0" → Claude chạy, kết quả hiện trong transcript.
- **Ràng buộc:** "không sửa test cũ" — chặn kiểu "xóa test cho pass".
- **Giới hạn:** "hoặc dừng sau 10 turn" — tránh chạy vô tận, tốn quota.

Lệnh đi kèm: `/goal` (xem trạng thái), `/goal clear` (hủy). `/goal` không đổi permission mode — muốn chạy
không cần bấm duyệt thì kết hợp **auto mode** (Module 2).

So sánh: `/goal` chạy tiếp khi turn xong · `/loop` chạy theo **khoảng thời gian** · Stop hook tự viết thì
áp dụng mọi phiên.

### 1.6 Bảng chọn nhanh

| Tình huống | Dùng |
|---|---|
| Task lớn, sợ hiểu sai | Plan mode + `Ctrl+G` sửa plan |
| Claude đúng hướng, chợt nhớ thêm yêu cầu | Queue (gõ + Enter khi đang chạy) |
| Muốn hỏi nhanh, không làm phiền | `/btw` |
| Claude đi sai hướng | `Esc` ngay, rồi nói lại |
| Code bị sửa hỏng | `Esc Esc` → Restore code (nếu sửa bằng Edit/Write) |
| Muốn thử cách khác, giữ bản gốc | `/branch` |
| Task dài có điều kiện kiểm chứng rõ | `/goal` |
| Sai 2 lần | `/clear` + prompt mới |

---

## Câu hỏi tự kiểm tra
1. Queue và Esc khác nhau thế nào? Khi nào dùng cái nào?
2. Claude chạy `rm -rf build/` nhầm. Rewind có cứu được không? Phòng bằng cách nào? (gợi ý: khóa 1 Module 4)
3. Điều kiện `/goal code chạy tốt` có vấn đề gì? Viết lại cho tốt.
4. Vì sao `/goal` dùng một model **khác** để chấm thay vì để chính Claude tự quyết là xong?
