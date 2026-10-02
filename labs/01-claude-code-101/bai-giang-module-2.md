# Bài giảng — Claude Code 101 · Module 2: Cài đặt & Prompt đầu tiên

> Nguồn: tài liệu chính thức [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works),
> [Quickstart](https://code.claude.com/docs/en/quickstart), [Best practices](https://code.claude.com/docs/en/best-practices).
> Soạn 2026-09-30. Máy công ty đang có Claude Code **2.1.285** và Git for Windows 2.51.

**Mục lục**
- 2.1 Cài đặt trên Windows
- 2.2 Đăng nhập
- 2.3 Lệnh cần thuộc
- 2.4 Viết prompt đầu tiên tốt
- 2.5 Thử ngay trên repo này

Trước đó: [Module 1 — Claude Code là gì?](bai-giang-module-1.md) · Tiếp theo: [Module 3 — Daily workflows](bai-giang-module-3.md)

---

### 2.1 Cài đặt trên Windows

Máy công ty **đã có sẵn** (2.1.285). Máy nhà thì chọn 1 trong các cách:

```powershell
# Cách khuyên dùng — native, tự cập nhật (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Hoặc WinGet — KHÔNG tự cập nhật, nhớ chạy: winget upgrade Anthropic.ClaudeCode
winget install Anthropic.ClaudeCode
```

Rồi **mở terminal mới** và chạy `claude --version`.
- Báo `claude` not recognized → chưa có trong PATH, mở terminal mới hoặc xem trang Troubleshoot.
- Nên cài **Git for Windows** để Claude Code có tool Bash. Không có thì nó dùng PowerShell.

### 2.2 Đăng nhập

```powershell
cd <thư mục project>
claude          # lần đầu sẽ mở trình duyệt để đăng nhập
```

- Bạn dùng **subscription** → chọn đăng nhập bằng tài khoản Claude. Đổi tài khoản thì dùng `/login`.
- ⚠️ Nếu biến môi trường `ANTHROPIC_API_KEY` đã được đặt, Claude Code sẽ **hỏi có dùng key đó không**.
  Chọn key thì bị **tính tiền API** thay vì subscription. Vì vậy key chỉ để trong `.env` của lab,
  đừng đặt thành biến môi trường hệ thống.

### 2.3 Lệnh cần thuộc

**Gõ ở terminal (shell):**

| Lệnh | Tác dụng |
|---|---|
| `claude` | Mở phiên tương tác |
| `claude "task"` | Mở phiên kèm prompt đầu tiên |
| `claude -p "query"` | Chạy 1 lần rồi thoát (dùng trong script/CI; học sau) |
| `claude -c` | Tiếp tục phiên gần nhất |
| `claude -r` | Chọn phiên cũ để tiếp tục |

**Gõ trong phiên:**

| Lệnh / Phím | Tác dụng |
|---|---|
| `/help`, `/` | Xem lệnh và skill hiện có |
| `/clear` | Xóa sạch context (bắt đầu việc mới) |
| `/context` | Xem context đang chứa gì |
| `/model` | Đổi model |
| `/init` | Tự tạo CLAUDE.md khởi đầu cho project |
| `/doctor` | Kiểm tra cài đặt và cấu hình |
| `/exit` hoặc `Ctrl+D` ×2 | Thoát |
| `Esc` / `Esc Esc` | Dừng / mở menu rewind |
| `Shift+Tab` | Đổi permission mode |
| `↑`, `Tab` | Lịch sử lệnh, tự hoàn thành |
| `@tên-file` | Chỉ thẳng file cho Claude đọc |

### 2.4 Viết prompt đầu tiên tốt

**Nguyên tắc 1 — Nói chuyện, không cần prompt hoàn hảo.** Bắt đầu bằng ý chính, rồi chỉnh dần
("chưa đúng, lỗi nằm ở phần session"). Không cần làm lại từ đầu.

**Nguyên tắc 2 — Giao việc như cho đồng nghiệp giỏi.** Đưa bối cảnh và mục tiêu, để Claude tự tìm
file và lệnh:
> *"Luồng checkout bị lỗi với thẻ hết hạn. Code liên quan ở src/payments/. Điều tra và sửa giúp."*

**Nguyên tắc 3 — Cụ thể: phạm vi, triệu chứng, nguồn.**

| ❌ Mơ hồ | ✅ Cụ thể |
|---|---|
| "fix the bug" | "fix lỗi login: user thấy màn hình trắng sau khi nhập sai mật khẩu" |
| "add tests for foo.py" | "viết test cho foo.py, case user đã logout. Không dùng mock." |
| "sao API này lạ vậy?" | "đọc git history của ExecutionFactory, tóm tắt vì sao API thành ra như vậy" |

**Nguyên tắc 4 (quan trọng nhất) — Cho Claude cách tự kiểm tra.** Không có tiêu chí thì Claude dừng
khi thấy *trông có vẻ xong*, và **bạn** lại thành người verify.
> ❌ *"viết hàm validate email"*
> ✅ *"viết hàm validate_email. Test: user@example.com → True, invalid → False, user@.com → False.
> Code xong thì chạy test."*

**Nguyên tắc 5 — Cho Claude khám phá trước khi bắt nó sửa.** Hỏi *"giải thích cấu trúc thư mục"*,
*"entry point ở đâu?"* trước. Hỏi Claude Code về chính nó cũng được: *"làm sao tạo skill?"*

### 2.5 Thử ngay trên repo này

Mở terminal trong `learn-claude` và gõ `claude`, rồi lần lượt thử:
1. `what does this project do?` → xem nó có nhắc tới hành trình học và `memory/` không (dấu hiệu đã đọc CLAUDE.md)
2. `/context` → tìm CLAUDE.md trong danh sách
3. `giải thích cấu trúc thư mục @memory` → thử cú pháp `@`
4. `what files have I changed?` → git dạng hội thoại
5. `Shift+Tab` vài lần → xem thanh trạng thái đổi mode

## Tóm tắt Module 2
- Cài: `irm https://claude.ai/install.ps1 | iex` (tự cập nhật) → **terminal mới** → `claude --version`.
- Đăng nhập bằng subscription. Đừng đặt `ANTHROPIC_API_KEY` thành biến môi trường hệ thống.
- Prompt tốt = **cụ thể + có tiêu chí để tự kiểm tra**. Cho Claude khám phá trước khi sửa.

## Câu hỏi tự kiểm tra (trả lời cho Claude chấm)
5. Viết lại prompt *"làm file check env"* cho tốt theo nguyên tắc 3 và 4.
