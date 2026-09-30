# Bài giảng — Claude Code 101 · Module 1: Claude Code là gì? Hoạt động thế nào?

> Nguồn: tài liệu chính thức [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works),
> [Quickstart](https://code.claude.com/docs/en/quickstart), [Best practices](https://code.claude.com/docs/en/best-practices).
> Soạn 2026-09-30. Máy công ty đang có Claude Code **2.1.285** và Git for Windows 2.51.

**Mục lục**
- 1.1 Định nghĩa trong một câu
- 1.2 Agentic loop — trái tim của mọi AI agent
- 1.3 Model + Tools = Agent · Claude Code là "harness"
- 1.4 Claude Code thấy được những gì?
- 1.5 Context window — tài nguyên quan trọng nhất
- 1.6 Sessions (phiên làm việc)
- 1.7 An toàn: Checkpoints và Permissions
- 1.8 Chạy ở đâu

Tiếp theo: [Module 2 — Cài đặt & Prompt đầu tiên](bai-giang-module-2.md)

---

### 1.1 Định nghĩa trong một câu

**Claude Code là một _agent_ chạy trong terminal.** Nó không chỉ trả lời, mà còn **tự hành động**:
đọc file, sửa code, chạy lệnh, chạy test, dùng git, tra web. Sau đó nó tự kiểm tra kết quả và làm tiếp.

So sánh 3 kiểu AI hỗ trợ code:

| | Chat (claude.ai) | Autocomplete (gợi ý inline) | **Claude Code (agent)** |
|---|---|---|---|
| Thấy gì | Thứ bạn copy vào | File đang mở | **Cả project** + terminal + git |
| Làm được gì | Trả lời bằng text | Gợi ý vài dòng | **Đọc, sửa nhiều file, chạy lệnh, tự verify** |
| Ai là "vòng lặp" | **Bạn** (copy → chạy → copy lỗi lại) | Bạn | **Claude tự lặp**, bạn giám sát |

Ý quan trọng nhất là dòng cuối. Với chat, *bạn* phải copy lỗi qua lại. Với agent, Claude tự chạy,
tự đọc lỗi, tự sửa.

### 1.2 Agentic loop — trái tim của mọi AI agent

Mỗi khi bạn giao việc, Claude đi qua 3 pha, lặp đến khi xong:

```
   Prompt của bạn
        │
        ▼
  ┌─► 1. GATHER CONTEXT  (đọc file, tìm kiếm, chạy git log...)
  │         │
  │         ▼
  │   2. TAKE ACTION     (sửa file, chạy lệnh...)
  │         │
  │         ▼
  └── 3. VERIFY RESULTS  (chạy test, đọc output) ── xong? ──► Trả kết quả
```

Ví dụ bạn nói *"fix the failing tests"*, Claude có thể:
1. Chạy test suite để xem test nào fail
2. Đọc output lỗi
3. Tìm các file source liên quan
4. Đọc các file đó để hiểu code
5. Sửa file
6. Chạy lại test để kiểm tra

Mỗi bước trả về thông tin mới, và Claude dựa vào đó để quyết định bước sau. Việc đơn giản như hỏi về
code thì có khi chỉ cần pha 1. Sửa bug thì phải lặp cả 3 pha nhiều lần.

**Bạn cũng nằm trong vòng lặp**, có thể chen vào bất cứ lúc nào:
- `Esc`: dừng ngay. Tool đang chạy bị hủy, context vẫn giữ nguyên.
- Gõ tin nhắn rồi `Enter` trong lúc Claude đang chạy: tin được *xếp hàng*. Claude đọc nó ngay sau khi
  xong tool hiện tại, rồi đổi hướng.

### 1.3 Model + Tools = Agent · Claude Code là "harness"

Agentic loop có 2 thành phần:
- **Model** (Claude Opus / Sonnet / Haiku): *suy nghĩ*, quyết định bước tiếp theo. Đổi bằng `/model`.
- **Tools**: *hành động*. Không có tool thì model chỉ trả lời được bằng text.

**Claude Code chính là lớp vỏ (harness)** bao quanh model: cung cấp tools và quản lý những gì model
nhìn thấy (context).

5 nhóm tool có sẵn:

| Nhóm | Làm gì |
|---|---|
| File operations | Đọc, sửa, tạo, đổi tên file |
| Search | Tìm file theo pattern, tìm nội dung bằng regex |
| Execution | Chạy lệnh shell, server, test, git |
| Web | Tìm kiếm web, đọc tài liệu, tra thông báo lỗi |
| Code intelligence | Xem lỗi type sau khi sửa, nhảy tới định nghĩa (cần plugin) |

Ngoài ra còn tool để tạo subagent, hỏi bạn câu hỏi, v.v. Có thể mở rộng thêm bằng **skills, MCP,
hooks, subagents** (Module 4).

> 💡 **Góc AI Engineer: đây là thứ bạn sẽ tự xây ở Giai đoạn 4 và 8.**
> Bên dưới, Claude Code chỉ là một vòng lặp gọi API như sau (pseudo-Python):
>
> ```python
> messages = [{"role": "user", "content": "fix the failing tests"}]
> while True:
>     resp = client.messages.create(model=..., tools=TOOLS, messages=messages)
>     messages.append({"role": "assistant", "content": resp.content})
>     if resp.stop_reason != "tool_use":      # model không gọi tool nữa → xong
>         break
>     results = [
>         {"type": "tool_result", "tool_use_id": b.id, "content": run_tool(b.name, b.input)}
>         for b in resp.content if b.type == "tool_use"
>     ]
>     messages.append({"role": "user", "content": results})   # đưa kết quả tool lại cho model
> ```
>
> Giải thích từng dòng + ví dụ chạy 5 vòng: [memory/notes/agentic-loop.md](../../memory/notes/agentic-loop.md)
>
> Hiểu vòng lặp này là hiểu 80% mọi "AI agent" trên thị trường. Khi dùng Claude Code, bạn hãy để ý
> xem nó gọi tool nào, theo thứ tự nào. Đó là cách học thiết kế agent miễn phí.

> 📌 Giải thích sâu hơn về "harness" và ẩn dụ não, tay, cơ thể: [memory/notes/harness.md](../../memory/notes/harness.md)

### 1.4 Claude Code thấy được những gì?

Khi bạn chạy `claude` trong một thư mục:
- **Project**: file trong thư mục và thư mục con (file bên ngoài thì phải được bạn cho phép)
- **Terminal**: mọi lệnh bạn chạy được thì nó cũng chạy được
- **Git state**: branch hiện tại, thay đổi chưa commit, lịch sử commit
- **CLAUDE.md**: chỉ dẫn riêng của project, **tự nạp mỗi phiên** (repo này dùng nó để dặn đọc `memory/`)
- **Auto memory**: những điều Claude tự ghi nhớ, lưu trong `~/.claude/projects/...`. Chỉ nằm trên
  từng máy, không đi theo git.
- **Extensions** bạn cấu hình: MCP servers, skills, subagents

### 1.5 Context window — tài nguyên quan trọng nhất

Context window là **toàn bộ những gì Claude "nhìn thấy"** tại một thời điểm: lịch sử hội thoại, nội
dung các file đã đọc, output lệnh, CLAUDE.md, skill đã nạp, system instructions.

**Quy luật cốt lõi của khóa học:** context đầy rất nhanh, và **context càng đầy thì model làm càng
kém**. Nó bắt đầu "quên" chỉ dẫn ban đầu và mắc lỗi nhiều hơn.

Khi gần đầy, Claude Code tự **compact**: xóa bớt output tool cũ, rồi tóm tắt hội thoại. Chỉ dẫn chi
tiết từ đầu phiên có thể bị mất. Vì vậy:
- Quy tắc lâu dài → để trong **CLAUDE.md**, đừng chỉ nói trong chat
- `/context` → xem cái gì đang chiếm chỗ
- (Module 3 sẽ học kỹ `/clear`, `/compact`, subagent để giữ context gọn)

### 1.6 Sessions (phiên làm việc)

- Mỗi phiên được lưu thành file JSONL trong `~/.claude/projects/`.
- **Các phiên độc lập với nhau**: phiên mới bắt đầu với context trống. Đây chính là lý do repo này có
  `memory/` + skill `/hoc-tiep`.
- `claude -c` (`--continue`): tiếp tục phiên gần nhất trong thư mục này. `claude -r` (`--resume`):
  chọn phiên từ danh sách.
- `/branch` hoặc `--fork-session`: *fork* phiên, tức là copy lịch sử sang phiên mới, phiên gốc giữ nguyên.

> ⚠️ Phân biệt: `/resume` là **lệnh có sẵn** của Claude Code, mở lại *hội thoại cũ trên máy này*
> (lịch sử JSONL, không đi theo git). `/hoc-tiep` là **skill của repo này**, đọc `memory/` để biết
> *tiến độ học*, dùng được ở mọi máy. Lúc đầu skill tên `resume`, bị trùng với lệnh có sẵn nên đã
> đổi tên. Bài học: đặt tên skill thì tránh trùng lệnh built-in.

### 1.7 An toàn: Checkpoints và Permissions

**Checkpoints (hoàn tác sửa file):**
- Trước khi sửa file, Claude chụp lại nội dung cũ. Nhấn **`Esc` hai lần** hoặc `/rewind` để quay lại.
  Có thể khôi phục hội thoại, code, hoặc cả hai.
- ⚠️ Chỉ ghi lại thay đổi qua *tool sửa file* của Claude. Thay đổi qua **lệnh Bash** (ví dụ `rm`) và
  hành động bên ngoài (database, API, deploy) **không hoàn tác được**. Checkpoint **không thay thế git**.

**Permission modes** (nhấn `Shift+Tab` để chuyển qua lại):

| Mode | Hành vi | Khi nào dùng |
|---|---|---|
| **Auto** | Một model phân loại chạy nền duyệt hành động, chỉ chặn việc rủi ro | Mặc định (bản ≥ 2.1.283) |
| **Manual** | Hỏi trước mỗi lần sửa file hoặc chạy lệnh | Muốn tự kiểm soát từng bước, code nhạy cảm |
| **Accept edits** | Tự sửa file và chạy lệnh file cơ bản, vẫn hỏi với lệnh khác | Tin kế hoạch, muốn đi nhanh |
| **Plan** | Chỉ đọc và đề xuất kế hoạch, **không sửa** | Trước việc lớn hoặc code lạ (Module 3) |

Có thể cho phép sẵn một số lệnh an toàn (như `git status`) trong `.claude/settings.json` hoặc qua `/permissions`.

### 1.8 Chạy ở đâu

Vòng lặp giống hệt nhau ở mọi nơi, chỉ khác giao diện: **Terminal (CLI)**, **VS Code extension**
(bạn đang dùng), JetBrains, Desktop app, web (claude.ai/code), Slack, GitHub Actions. Code chạy ở
máy bạn (local), trên cloud của Anthropic, hoặc Remote Control (điều khiển từ web, code vẫn chạy ở máy bạn).

## Tóm tắt Module 1
1. Claude Code = **model + tools + harness** chạy **agentic loop** (gather → act → verify).
2. Nó thấy **cả project, terminal, git**, và tự nạp **CLAUDE.md** mỗi phiên.
3. **Context window** là tài nguyên số 1. Càng đầy càng kém, quy tắc lâu dài để trong CLAUDE.md.
4. An toàn: **checkpoint** (`Esc Esc`) chỉ hoàn tác sửa file, không thay git. **Permission modes** qua `Shift+Tab`.

## Câu hỏi tự kiểm tra (trả lời cho Claude chấm)
1. Vì sao nói Claude Code là "agent" còn chat trên claude.ai thì không?
2. Claude xóa file bằng lệnh `rm` trong Bash. Nhấn `Esc Esc` có lấy lại được không? Vì sao?
3. Bạn dặn Claude một quy tắc trong chat ở đầu phiên. 2 tiếng sau nó không làm theo nữa. Chuyện gì xảy ra, sửa thế nào?
4. Khác nhau giữa `claude -c` và `/branch`?
