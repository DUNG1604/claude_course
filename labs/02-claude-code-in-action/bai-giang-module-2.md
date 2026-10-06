# Bài giảng — Claude Code in Action · Module 2: Configure Claude

> Nguồn: [Memory / CLAUDE.md](https://code.claude.com/docs/en/memory),
> [Best practices](https://code.claude.com/docs/en/best-practices),
> [Permission modes](https://code.claude.com/docs/en/permission-modes),
> [Skills — Run and verify your app](https://code.claude.com/docs/en/skills). Soạn 2026-10-06.

**Mục lục**
- 2.1 Module này để làm gì
- 2.2 CLAUDE.md mà Claude thật sự làm theo
- 2.3 Verification: 4 mức "chốt chặn" + verification skills
- 2.4 Permission modes: Claude được tự làm đến đâu
- 2.5 Hooks: luật cho phiên chạy dài
- 2.6 Bảng chọn: dặn, kiểm, cho phép, cưỡng chế

Trước đó: [Module 1](bai-giang-module-1.md) · Thực hành: [README lab, phần Module 2](README.md)

---

### 2.1 Module này để làm gì

Module 1 là **lái tay** (bạn ngồi canh, Esc, queue). Module 2 là **cài đặt xe** để bạn bớt phải canh:

| Câu hỏi | Công cụ |
|---|---|
| Claude **biết** quy tắc của project chưa? | CLAUDE.md viết tốt |
| Claude **biết khi nào xong** chưa? | Verification (test, `/goal`, Stop hook, reviewer) |
| Claude **được phép** làm gì mà không hỏi? | Permission modes + rules |
| Thứ gì **bắt buộc** phải xảy ra / bị chặn? | Hooks |

Phần lớn bạn đã biết từ khóa 1. Module này đi sâu vào **cách dùng cho phiên dài, không giám sát**.

### 2.2 CLAUDE.md mà Claude thật sự làm theo

CLAUDE.md là **ngữ cảnh**, không phải cấu hình cưỡng chế → cách viết quyết định Claude có theo hay không.

**1. Cụ thể đến mức kiểm chứng được:**

| ❌ Mơ hồ | ✅ Kiểm chứng được |
|---|---|
| "Format code đúng chuẩn" | "Thụt lề 4 space, format bằng `ruff format`" |
| "Test trước khi commit" | "Chạy `python -m unittest` trước khi commit" |
| "Tổ chức file gọn gàng" | "Lab đặt trong `labs/NN-tên/`, mỗi lab có README" |

Mẹo: nếu **bạn** không kiểm tra được Claude đã làm theo hay chưa, thì Claude cũng không biết thế nào là làm đúng.

**2. Ngắn, có cấu trúc, không mâu thuẫn:**
- **< 200 dòng.** Dài hơn → tốn context **và giảm mức tuân thủ**. Phần chỉ áp dụng một vùng code → rule có `paths:`.
- **Nhóm theo heading + gạch đầu dòng**, đừng viết đoạn văn dày.
- **Hai chỉ dẫn mâu thuẫn** → Claude có thể chọn bừa một cái. Định kỳ rà CLAUDE.md, CLAUDE.md thư mục con và rules.

**3. Nhấn mạnh có chọn lọc:** một dòng hay bị bỏ qua → thêm `IMPORTANT` **cho riêng dòng đó**.
Nhấn mạnh 10 dòng thì không dòng nào nổi bật.

**4. Chẩn đoán khi Claude không làm theo:**

| Triệu chứng | Nguyên nhân thường gặp | Sửa |
|---|---|---|
| Có quy tắc mà Claude vẫn làm sai | File quá dài, quy tắc bị chìm | Cắt bớt mạnh tay |
| Claude hỏi điều CLAUDE.md đã trả lời | Câu chữ mơ hồ | Viết lại cụ thể hơn |
| Claude làm đúng kể cả khi không có quy tắc | Dòng đó thừa | Xóa |
| Quy tắc **bắt buộc** mà thỉnh thoảng vẫn bị quên | Lời dặn không đủ | Chuyển thành **hook** |

**5. Coi CLAUDE.md như code:** review khi có lỗi, dọn định kỳ, **kiểm thử** bằng cách xem hành vi Claude có
thay đổi thật không (bạn đã làm đúng vậy với dòng nhắc commit ở khóa 1). `/doctor` đề xuất chỗ cắt; `/context`
xác nhận file đã được nạp.

**Bonus — dặn cách compact:** thêm vào CLAUDE.md câu kiểu *"Khi compact, luôn giữ danh sách file đã sửa và lệnh
test"* để thông tin quan trọng sống sót qua compact.

### 2.3 Verification: 4 mức "chốt chặn" + verification skills

> *"Cho Claude một phép kiểm tra nó tự chạy được — đó là khác biệt giữa phiên bạn phải ngồi canh và phiên bạn
> có thể bỏ đi."* — Best practices

Phép kiểm tra = **bất cứ thứ gì trả về tín hiệu pass/fail mà Claude đọc được**: test, exit code của build, linter,
script so output với file mẫu, screenshot so với thiết kế.

Có phép kiểm tra rồi, chọn **mức chốt chặn**:

| Mức | Cách | Ai quyết "xong" | Dùng khi |
|---|---|---|---|
| 1. Trong prompt | *"…chạy test và sửa tới khi pass"* | Chính Claude | Mọi task, ngay hôm nay |
| 2. `/goal` | Điều kiện + evaluator sau mỗi turn | Model chấm riêng | Task dài trong 1 phiên |
| 3. **Stop hook** | Script chạy khi Claude định dừng; fail → chặn dừng | **Script** (tất định) | Luật cho mọi phiên |
| 4. Ý kiến thứ hai | Subagent / `/code-review` soi diff ở context mới | Model khác, không thấy quá trình | Trước khi coi là xong |

Càng xuống dưới càng tốn công cài đặt, nhưng càng **không cần bạn**.

**Đòi bằng chứng, không đòi lời hứa:** yêu cầu Claude dán output test, lệnh đã chạy và kết quả, screenshot.
Đọc bằng chứng nhanh hơn tự chạy lại, và dùng được cả khi bạn không ngồi xem.

⚠️ **Bẫy reviewer:** bảo reviewer "tìm lỗ hổng" thì nó **luôn** tìm ra vài cái, kể cả khi code ổn → chạy theo
hết sẽ over-engineering. Dặn reviewer *chỉ báo lỗi ảnh hưởng tính đúng hoặc yêu cầu đã nêu*.

**Verification skills có sẵn:**

| Skill | Làm gì |
|---|---|
| `/run` | Chạy app và thao tác để thấy thay đổi hoạt động |
| `/verify` | Build + chạy app để xác nhận thay đổi đúng — **không** chỉ dựa vào test/type check |
| `/run-skill-generator` | Ghi lại "công thức" chạy project thành skill `.claude/skills/run-<tên>/` để lần sau khỏi mò |

Ý tưởng chung: **công thức kiểm chứng của project nên là một skill** — viết một lần, mọi phiên và mọi agent dùng lại.
Bạn cũng tự viết được: ví dụ skill kiểm tra memory files không vượt giới hạn dòng (lab Module 2).

### 2.4 Permission modes: Claude được tự làm đến đâu

| Mode (tên config) | Tự làm không hỏi | Dùng khi |
|---|---|---|
| **Manual** (`default`) | Chỉ đọc | Việc nhạy cảm, muốn duyệt từng bước |
| `acceptEdits` | Đọc + sửa file + lệnh file thông dụng (`mkdir`, `mv`, `cp`...) | Đang review code Claude viết |
| `plan` | Đọc (+ lệnh được classifier duyệt) | Khám phá trước khi sửa |
| **`auto`** | Mọi thứ, có **classifier** kiểm tra nền | Task dài, đỡ mỏi tay bấm duyệt |
| `dontAsk` | Chỉ tool đã cho phép trước; còn lại **từ chối** | CI, script khóa chặt |
| `bypassPermissions` | Mọi thứ, không kiểm tra | **Chỉ** container/VM cô lập |

- **Đổi mode:** `Shift+Tab` (CLI) — vòng `auto → manual → acceptEdits → plan`; VS Code: ô chọn mode.
  Từ v2.1.283, **auto là mode khởi đầu mặc định** — máy bạn (2.1.289) đang ở Auto, đúng như ảnh chụp extension.
- **Auto mode hoạt động thế nào:** một model thứ hai (**classifier**) xem từng hành động trước khi chạy.
  Mặc định **chặn**: tải và chạy code (`curl | bash`), gửi dữ liệu nhạy cảm ra ngoài, deploy production,
  **force push**, `git reset --hard` / `git clean -fd`, xóa không hoàn tác file có từ trước phiên, commit làm lộ secret...
- **Ranh giới bạn nói được tôn trọng:** bạn nói *"đừng push"* → classifier chặn push cho tới khi bạn gỡ.
  Claude tự cho rằng "điều kiện đã thỏa" **không** gỡ được ranh giới đó.
- **Tự lùi về hỏi:** classifier chặn **3 lần liên tiếp hoặc 20 lần tổng** → auto tạm dừng, quay về hỏi bạn.

**Permission rules** — lớp đặt lên trên mode, trong `settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(python -m unittest *)", "Bash(git status *)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Bash(git push --force *)", "Edit(.env)"]
  }
}
```

- `deny` chặn ở **mọi mode**, kể cả `bypassPermissions`. `allow` giảm số lần bị hỏi trong Manual.
- `/permissions` để xem/sửa; `/sandbox` để chạy lệnh trong môi trường cô lập.

### 2.5 Hooks: luật cho phiên chạy dài

Bạn đã có hook `SessionStart`. Với phiên chạy không giám sát, 3 hook đáng giá nhất:

| Hook | Vai trò | Ví dụ |
|---|---|---|
| `PreToolUse` | **Chặn** trước khi làm | exit 2 nếu lệnh chứa `rm -rf` hoặc sửa `.env` |
| `PostToolUse` (matcher `Edit\|Write`) | **Tự sửa** sau mỗi lần sửa file | Chạy `ruff format` lên file vừa sửa |
| `Stop` | **Không cho dừng** khi chưa đạt | Chạy test; fail → chặn, Claude phải sửa tiếp |

Ngoài `type: "command"`, hook còn có `"prompt"` (model nhỏ đánh giá) và `"agent"` (subagent kiểm tra) cho việc
cần phán đoán. `/goal` chính là một Stop hook dạng prompt.

### 2.6 Bảng chọn: dặn, kiểm, cho phép, cưỡng chế

| Muốn | Dùng | Độ chắc |
|---|---|---|
| Claude **biết** quy ước | CLAUDE.md / rules | Lời dặn |
| Claude **biết khi nào xong** | Test trong prompt → `/goal` → Stop hook | Tăng dần |
| Claude **tự chạy** không hỏi | `auto` mode + `allow` rules | Có classifier canh |
| **Cấm tuyệt đối** một hành động | `deny` rule hoặc `PreToolUse` hook | Cưỡng chế |
| Kết quả được **người khác** kiểm | Subagent / `/code-review` | Ý kiến thứ hai |

---

## Câu hỏi tự kiểm tra
1. CLAUDE.md có dòng "luôn viết code sạch". Có vấn đề gì? Viết lại.
2. Claude hay quên chạy test trước khi báo xong. Liệt kê 3 cách sửa từ nhẹ tới mạnh.
3. Bạn đang ở auto mode và nói "đừng commit gì nhé". 10 phút sau Claude muốn commit. Chuyện gì xảy ra?
4. `deny` rule và hook `PreToolUse` đều chặn được `git push --force`. Khác nhau ở đâu? (gợi ý: cái nào cần viết script)
