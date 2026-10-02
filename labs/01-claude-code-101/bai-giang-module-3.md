# Bài giảng — Claude Code 101 · Module 3: Daily Workflows

> Nguồn: [Best practices](https://code.claude.com/docs/en/best-practices),
> [Common workflows](https://code.claude.com/docs/en/common-workflows),
> [Explore the context window](https://code.claude.com/docs/en/context-window). Soạn 2026-10-01.

**Mục lục**
- 3.1 Hai ràng buộc quyết định mọi workflow
- 3.2 Explore → Plan → Code → Commit
- 3.3 Cho Claude cách tự kiểm tra (verification)
- 3.4 Quản lý context
- 3.5 Cái gì còn, cái gì mất sau compact
- 3.6 Code review
- 3.7 Git hằng ngày
- 3.8 Năm lỗi thường gặp

Trước đó: [Module 2](bai-giang-module-2.md) · Tiếp theo: [Module 4](bai-giang-module-4.md) · Thực hành: [README lab, phần Module 3](README.md)

---

### 3.1 Hai ràng buộc quyết định mọi workflow

Mọi lời khuyên trong module này đều xuất phát từ 2 ràng buộc:

1. **Context đầy nhanh, và càng đầy thì Claude làm càng kém.** (Nhớ lại [agentic loop](../../memory/notes/agentic-loop.md):
   mỗi tool call làm cuốn sổ `messages` dài thêm và bị gửi lại toàn bộ.)
2. **Claude dừng khi việc *trông có vẻ* xong.** Không có cách nào để kiểm tra thì "trông có vẻ xong"
   là tín hiệu duy nhất Claude có, và **bạn** lại thành người phải kiểm tra.

→ Workflow tốt = **giữ context gọn** + **cho Claude một phép kiểm tra để tự chạy**.

### 3.2 Explore → Plan → Code → Commit

Để Claude lao vào code ngay thì dễ giải **sai bài toán**. Nên tách thành 4 pha:

| Pha | Mode | Bạn nói gì (ví dụ) | Mục đích |
|---|---|---|---|
| **1. Explore** | Plan mode | *"đọc src/auth, hiểu cách xử lý session và login, cách quản lý biến môi trường cho secret"* | Claude chỉ đọc, chưa sửa |
| **2. Plan** | Plan mode | *"mình muốn thêm Google OAuth. Cần sửa file nào? Luồng session thế nào? Lập kế hoạch."* | Ra kế hoạch để bạn duyệt |
| **3. Code** | Thoát plan mode | *"làm theo kế hoạch. Viết test cho callback, chạy test suite và sửa lỗi."* | Code + tự kiểm tra theo kế hoạch |
| **4. Commit** | — | *"commit với message mô tả rõ, rồi mở PR"* | Chốt lại |

**Plan mode, cách bật:**
- `Shift+Tab` cho tới khi thanh trạng thái hiện `⏸ plan mode on`
- Hoặc khởi động bằng `claude --permission-mode plan`
- `Ctrl+G`: mở kế hoạch trong editor để **tự sửa** trước khi duyệt
- Duyệt kế hoạch (hoặc `Shift+Tab`) để thoát plan mode và bắt đầu code

**Khi nào BỎ QUA plan:** việc nhỏ, phạm vi rõ (sửa typo, thêm 1 dòng log, đổi tên biến).
Quy tắc ngón tay cái: ***nếu mô tả được thay đổi trong 1 câu thì không cần plan.***
Nên plan khi: chưa chắc cách làm, sửa nhiều file, hoặc code mình chưa quen.

> 💡 Mẹo cho tính năng lớn: bảo Claude **phỏng vấn bạn** trước. *"Mình muốn làm X. Hỏi mình chi tiết
> (kỹ thuật, edge case, đánh đổi), đừng hỏi điều hiển nhiên. Hỏi xong thì viết spec vào SPEC.md."*
> Sau đó mở **phiên mới** (context sạch) để code theo SPEC.md.

### 3.3 Cho Claude cách tự kiểm tra (verification)

Đây là lời khuyên **giá trị nhất** của cả tài liệu best practices.

| ❌ Không có cách kiểm tra | ✅ Có cách kiểm tra |
|---|---|
| *"viết hàm validate email"* | *"viết validate_email. Test: user@example.com → True, invalid → False, user@.com → False. Code xong chạy test."* |
| *"làm dashboard đẹp hơn"* | *"[dán ảnh] làm theo thiết kế này. Chụp màn hình kết quả, so với ảnh gốc, liệt kê chỗ khác và sửa."* |
| *"build đang lỗi"* | *"build lỗi như sau: [dán lỗi]. Sửa và kiểm tra build pass. Sửa gốc rễ, đừng tắt lỗi đi."* |

Phép kiểm tra có thể là: test suite, exit code của build, linter, script so sánh output, ảnh chụp màn hình.

**4 mức kiểm tra, từ dễ tới chắc chắn:**
1. **Trong prompt:** *"...chạy test và sửa tới khi pass"*. Dùng được ngay hôm nay.
2. **Cả phiên:** đặt điều kiện bằng `/goal`. Một bộ đánh giá riêng kiểm tra lại sau mỗi lượt.
3. **Cổng cứng:** **Stop hook** chạy script kiểm tra và không cho Claude kết thúc khi chưa pass (Module 4).
4. **Ý kiến thứ hai:** một **subagent** với context mới review kết quả, để người làm không phải là người chấm.

**Đòi bằng chứng, đừng tin lời khẳng định:** bảo Claude dán output test, lệnh đã chạy, ảnh chụp.
Xem bằng chứng nhanh hơn tự chạy lại.

> 💡 **Góc AI Engineer:** "làm → kiểm tra → sửa → lặp" chính là pattern **evaluator-optimizer** bạn
> sẽ tự code ở Giai đoạn 8. Mức 4 (subagent chấm) cũng là ý tưởng **LLM-as-judge** của Giai đoạn 7 (Evals).

### 3.4 Quản lý context

**Context có gì ngay từ đầu?** (số liệu ví dụ của Anthropic, đơn vị token)

| Thứ | ~Token | Ghi chú |
|---|---|---|
| System prompt | 4.200 | Luôn có, bạn không thấy |
| Project CLAUDE.md | 1.800 | Tùy độ dài, đây là lý do giữ < 200 dòng |
| Auto memory, skill descriptions, env, MCP tool names | ~1.500 | Chỉ *mô tả* skill, nội dung skill nạp khi dùng |
| **Mỗi lần đọc 1 file code** | **1.000–2.500** | Thứ làm đầy context nhanh nhất |

**Bộ lệnh quản lý context:**

| Lệnh | Làm gì | Khi nào dùng |
|---|---|---|
| `/context` | Xem cái gì đang chiếm chỗ | Khi thấy Claude bắt đầu "quên", hoặc tò mò |
| `/clear` | **Xóa sạch** hội thoại (CLAUDE.md vẫn được nạp lại) | **Chuyển sang việc không liên quan.** Dùng nhiều nhất |
| `/compact <trọng tâm>` | Tóm tắt hội thoại, giữ thứ bạn chỉ định | Đang giữa việc dài, muốn giải phóng chỗ. Ví dụ `/compact giữ lại các thay đổi API` |
| `/rewind` (hoặc `Esc Esc`) → **Summarize from here / up to here** | Tóm tắt **một phần** hội thoại | Muốn giữ nguyên phần gần đây, nén phần cũ |
| `/btw <câu hỏi>` | Hỏi nhanh, câu trả lời **không vào lịch sử** | Tra một chi tiết mà không làm đầy context |
| *"dùng subagent điều tra X"* | Subagent đọc file trong context **riêng**, chỉ trả về tóm tắt | Khám phá codebase lớn, nghiên cứu |

Tự động: gần đầy thì Claude Code tự compact (xóa output tool cũ trước, rồi mới tóm tắt).

**`/clear` khác `/compact` thế nào?** `/clear` = bắt đầu lại từ đầu, mất hết hội thoại. `/compact` =
nén lại, vẫn nhớ đại ý. Đổi việc thì `/clear`, đang giữa việc thì `/compact`.

### 3.5 Cái gì còn, cái gì mất sau compact

Phần này trả lời câu 3 của quiz Module 1 *("quy tắc nói trong chat bị quên")*:

| Thứ | Sau compact |
|---|---|
| CLAUDE.md ở gốc project, rule **không** có `paths:` | ✅ **Nạp lại từ đĩa** |
| Kế hoạch viết trong plan mode | ✅ Nạp lại từ đĩa |
| Auto memory, git status | ✅ Nạp lại / đọc mới |
| File đã đọc/sửa | 🟡 Đọc lại **tối đa 5 file** sửa gần nhất (file > 5.000 token chỉ còn đường dẫn) |
| Skill đã gọi | 🟡 Nạp lại, nhưng bị cắt bớt (5.000 token/skill). **Để chỉ dẫn quan trọng ở đầu SKILL.md** |
| Rule **có** `paths:`, CLAUDE.md ở thư mục con | 🟡 Bị tóm tắt mất, chỉ nạp lại khi Claude đọc file khớp |
| **Chỉ dẫn chỉ nói trong chat** | ❌ **Chỉ còn trong bản tóm tắt**, có thể mất |

→ **Quy tắc vàng:** thứ gì phải nhớ suốt phiên thì ghi vào **CLAUDE.md**, đừng chỉ nói trong chat.

> ⚠️ Liên hệ repo này: [.claude/rules/memory-files.md](../../.claude/rules/memory-files.md) có `paths:`.
> Sau compact nó sẽ mất cho tới khi Claude đọc lại một file trong `memory/`. Ổn, vì `/save-progress`
> luôn đọc `memory/` trước. Đó cũng là lý do CLAUDE.md có 1 dòng nhắc rule này: dòng nhắc thì không bị mất.

### 3.6 Code review

**Vì sao không bảo chính phiên vừa code tự review?** Vì nó **thiên vị code nó vừa viết**: nó nhớ
"lý do" của từng dòng nên khó thấy lỗi. Reviewer nên có **context mới**, chỉ thấy diff và tiêu chí.

3 cách, từ nhanh tới kỹ:
1. **`/code-review`**: skill có sẵn, review diff hiện tại tìm bug trong một **subagent mới**, trả kết quả về phiên.
2. **Review theo kế hoạch** (tự viết prompt):
   > *"Dùng subagent review diff so với PLAN.md. Kiểm tra mọi yêu cầu đã làm, edge case đã có test,
   > không sửa gì ngoài phạm vi. Chỉ báo lỗ hổng, không báo sở thích style."*
3. **Writer/Reviewer**: 2 phiên song song. Phiên A code, phiên B review file đó, rồi dán feedback của B về A.

> ⚠️ **Cẩn thận over-engineering:** reviewer được bảo "tìm lỗi" thì *luôn* tìm ra gì đó, kể cả khi code
> ổn. Sửa hết mọi góp ý → code phình to, phòng thủ thừa. Bảo reviewer **chỉ báo lỗi ảnh hưởng tính đúng
> hoặc yêu cầu**, phần còn lại là tùy chọn.

### 3.7 Git hằng ngày

Git qua hội thoại: *"mình đã sửa những file nào?"*, *"commit với message mô tả rõ"*,
*"tạo branch feature/x"*, *"xem 5 commit gần nhất"*, *"giúp resolve conflict"*.
- Có `gh` CLI thì Claude tạo được PR, đọc comment, xem issue.
- **Worktrees** (`claude --worktree <tên>`): chạy nhiều phiên song song trên các branch tách biệt, không
  đè file của nhau. ⚠️ Repo phải có **ít nhất 1 commit**. Repo `learn-claude` **chưa commit lần nào**.

### 3.8 Năm lỗi thường gặp

| Lỗi | Triệu chứng | Sửa |
|---|---|---|
| **Phiên "nồi lẩu"** | Việc A → hỏi chuyện B → quay lại A | `/clear` giữa các việc không liên quan |
| **Sửa đi sửa lại** | Chỉnh lần 2, lần 3 vẫn sai | **Sau 2 lần sửa thất bại → `/clear`**, viết prompt mới tốt hơn kèm điều đã học |
| **CLAUDE.md quá dài** | Claude bỏ qua quy tắc | Cắt mạnh. Claude đã làm đúng mà không cần dặn → xóa dòng đó, hoặc chuyển thành hook |
| **Tin rồi mới kiểm** | Code trông ổn nhưng sai edge case | Luôn có phép kiểm tra. Không kiểm được thì đừng ship |
| **Khám phá vô tận** | "Điều tra X" không giới hạn → đọc hàng trăm file | Thu hẹp phạm vi, hoặc giao cho subagent |

---

## Tóm tắt Module 3
1. Hai ràng buộc: **context đầy thì kém** + **Claude dừng khi trông có vẻ xong**.
2. Việc lớn hoặc lạ → **Explore → Plan → Code → Commit** (plan mode). Việc 1 câu → làm luôn.
3. **Luôn cho Claude phép kiểm tra** (test, build, ảnh) và đòi bằng chứng.
4. `/clear` khi đổi việc · `/compact <trọng tâm>` khi giữa việc · subagent cho việc đọc nhiều.
5. Quy tắc lâu dài → CLAUDE.md (còn sau compact). Review bằng context mới (`/code-review`, subagent).

## Câu hỏi tự kiểm tra
1. Khi nào nên bỏ qua plan mode? Cho 1 ví dụ cần plan và 1 ví dụ không cần.
2. Bạn sửa bug, Claude làm sai 2 lần dù bạn đã chỉnh. Nên làm gì tiếp, vì sao?
3. `/clear` và `/compact` khác nhau thế nào? Cho tình huống dùng mỗi lệnh.
4. Vì sao nên review bằng subagent thay vì bảo chính phiên vừa code tự review?
5. Viết lại prompt *"thêm chức năng đăng ký user"* để có phép kiểm tra rõ ràng.
