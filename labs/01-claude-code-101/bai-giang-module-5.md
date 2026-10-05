# Claude Code 101 · Module 5: Assessment & tổng kết khóa

> Module 5 không có kiến thức mới: làm quiz của khóa trên Skilljar + tự ôn. Soạn 2026-10-05.

**Mục lục**
- 5.1 Cả khóa trên 1 trang
- 5.2 Bảng chọn công cụ (thuộc lòng)
- 5.3 Tự đánh giá: đã làm được chưa?
- 5.4 Đề ôn tổng hợp (gom các câu đã bỏ qua)

Trước đó: [Module 4](bai-giang-module-4.md) · Thực hành: [README lab](README.md)

---

### 5.1 Cả khóa trên 1 trang

| Module | Ý cốt lõi | Chi tiết |
|---|---|---|
| 1. Claude Code là gì | Agent = model (não) + tools (tay) + harness (cơ thể). Agentic loop: model xin `tool_use` → harness chạy → gửi `tool_result` về, lặp tới `end_turn`. API stateless, mỗi vòng gửi lại cả cuốn sổ `messages` | [Module 1](bai-giang-module-1.md) |
| 2. Cài đặt & prompt đầu | CLI/IDE, đăng nhập bằng subscription. Prompt tốt = cụ thể + có ngữ cảnh + có cách kiểm tra | [Module 2](bai-giang-module-2.md) |
| 3. Daily workflows | 2 ràng buộc: context đầy thì kém, Claude dừng khi việc *trông* xong. Explore → Plan → Code → Commit, luôn có verification, `/clear` khi đổi việc, review bằng context mới | [Module 3](bai-giang-module-3.md) |
| 4. Tùy biến | CLAUDE.md/rules (luôn biết), skill (biết khi cần), subagent (cách ly), MCP (chạm bên ngoài), hook (bắt buộc xảy ra), plugin (đóng gói) | [Module 4](bai-giang-module-4.md) |

**3 câu đáng nhớ nhất cả khóa:**
1. *Context là tài nguyên khan hiếm.* Gần như mọi tính năng (subagent, skill 3 tầng, rule `paths:`, MCP
   tool search) đều sinh ra để tiết kiệm nó.
2. *Cho Claude cách tự kiểm tra.* Không có test/build/ảnh thì bạn thành người kiểm tra.
3. *Lời dặn ≠ luật.* CLAUDE.md/skill có thể bị quên; thứ bắt buộc thì làm thành hook.

### 5.2 Bảng chọn công cụ

| Tình huống | Dùng |
|---|---|
| Claude làm sai một quy ước 2 lần | Thêm 1 dòng CLAUDE.md |
| Quy tắc chỉ cần khi đụng một nhóm file | Rule có `paths:` |
| Gõ lại cùng prompt / dán lại cùng quy trình | Skill (action) |
| Tài liệu tra cứu chỉ thỉnh thoảng cần | Skill (reference) |
| Việc đọc nhiều file, chỉ cần kết luận | Subagent |
| Review code vừa viết | Subagent / `/code-review` (context mới) |
| Cần dữ liệu từ Jira, DB, trình duyệt | MCP server |
| Việc phải luôn xảy ra / phải chặn chắc chắn | Hook |
| Đổi sang việc không liên quan | `/clear` |
| Đang giữa việc dài, context gần đầy | `/compact <trọng tâm>` |
| Sửa sai 2 lần vẫn không được | `/clear` + prompt mới tốt hơn |
| Thay đổi mô tả được trong 1 câu | Làm luôn, khỏi plan mode |

### 5.3 Tự đánh giá: đã làm được chưa?

Đọc hiểu ≠ làm được. Tick khi **đã tự làm**, không phải khi đã đọc:

- [ ] Có ít nhất 1 commit làm theo đủ Explore → Plan → Code → Commit (`check_env.py`)
- [ ] Đã dùng `/context` và thấy rule `paths:` được nạp lúc nào
- [ ] Đã tự viết 1 skill (`/til`) và nó **tự kích hoạt** được nhờ description
- [ ] Đã tạo 1 hook (`SessionStart` → `git status --short`) và thấy output trong phiên
- [ ] Đã gọi subagent `ai-mentor` và giải thích được vì sao nó không thấy hội thoại chính
- [ ] Đã làm quiz của khóa trên Skilljar

### 5.4 Đề ôn tổng hợp

Gom các câu đã bỏ qua ở Module 1–4. Tự trả lời trong đầu; câu nào phải ngập ngừng → đọc lại mục chỉ dẫn.

1. Checkpoint (`Esc Esc`) có khôi phục được file bị xóa bằng `rm` không? Vì sao? *(M1)*
2. Viết lại prompt *"thêm chức năng đăng ký user"* sao cho có phép kiểm tra rõ ràng. *(M2, M3 §3.3)*
3. Khi nào nên bỏ qua plan mode? *(M3 §3.2)*
4. Sau compact, cái gì được nạp lại, cái gì mất? Nêu 3 cách chữa quy tắc bị quên. *(M3 §3.5, M4 §4.6)*
5. Muốn Claude **không bao giờ** `git push --force`: CLAUDE.md hay hook? Sự kiện nào, exit code mấy? *(M4 §4.6)*
6. Skill reference và skill action khác nhau thế nào? `/til` thuộc loại nào? *(M4 §4.3)*
7. Thư mục tự đặt như `inventory/` được Claude đọc khi nào? Thiết kế sao cho 40 file vẫn tìm đúng? *(M4)*
