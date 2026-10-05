# Bài giảng — Claude Code 101 · Module 4: Tùy biến Claude Code

> Nguồn: [Extend Claude Code](https://code.claude.com/docs/en/features-overview),
> [Hooks guide](https://code.claude.com/docs/en/hooks-guide), [Memory](https://code.claude.com/docs/en/memory),
> [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents),
> [MCP](https://code.claude.com/docs/en/mcp). Soạn 2026-10-01.

**Mục lục**
- 4.1 Bản đồ: 6 thứ cắm vào agentic loop
- 4.2 CLAUDE.md và rules: "luôn luôn biết"
- 4.3 Skills: "biết khi cần" + quy trình gọi bằng `/tên`
- 4.4 Subagents: "làm ở phòng riêng, chỉ mang kết quả về"
- 4.5 MCP: "thêm tay mới" để chạm hệ thống bên ngoài
- 4.6 Hooks: "luôn xảy ra, không cần Claude nhớ"
- 4.7 Chi phí context của từng thứ
- 4.8 Khi nào thêm cái gì, và mổ xẻ repo này

Trước đó: [Module 3](bai-giang-module-3.md) · Tiếp theo: [Module 5](bai-giang-module-5.md) · Thực hành: [README lab, phần Module 4](README.md)

---

### 4.1 Bản đồ: 6 thứ cắm vào agentic loop

Nhớ lại: model = não, tools = tay, harness = cơ thể + hệ thần kinh. Các extension là cách bạn
**độ** cái harness đó:

| Thứ | Một câu | Ví dụ |
|---|---|---|
| **CLAUDE.md** | Ngữ cảnh nạp **mọi phiên** | "Dùng Python + `.venv`, chạy test trước khi commit" |
| **Rules** (`.claude/rules/`) | CLAUDE.md tách nhỏ, có thể chỉ nạp khi đụng file khớp `paths:` | Quy tắc độ dài cho `memory/**` |
| **Skill** | Kiến thức/quy trình nạp **khi cần**, gọi bằng `/tên` hoặc Claude tự chọn | `/save-progress`, `/hoc-tiep` |
| **Subagent** | Một Claude con chạy vòng lặp riêng trong **context riêng**, trả về bản tóm tắt | `ai-mentor`, `Explore` |
| **MCP** | Giao thức nối Claude với **dịch vụ bên ngoài** (thêm tool mới) | Jira, Figma, Google Drive, database |
| **Hook** | Lệnh **chắc chắn chạy** tại một sự kiện trong vòng đời | Chạy formatter sau mỗi lần Edit |

**Plugin** là lớp đóng gói: gom skills + hooks + subagents + MCP thành 1 gói cài được, dùng khi
muốn mang cùng một setup sang repo khác hoặc chia sẻ cho team.

> Câu chốt của tài liệu: CLAUDE.md lo ngữ cảnh luôn bật, skill lo kiến thức theo yêu cầu, MCP lo kết
> nối ngoài, subagent lo cách ly, hook lo tự động hóa.

### 4.2 CLAUDE.md và rules: "luôn luôn biết"

**CLAUDE.md** được nạp toàn bộ lúc đầu phiên và nằm trong **mọi request**, nên mỗi dòng đều tốn tiền.

- **Nên ghi:** lệnh build/test, quy ước code, cấu trúc project, quy tắc "không bao giờ làm X".
- **Không nên ghi:** thứ Claude tự đọc code là biết, tài liệu dài (đưa vào skill), việc chỉ thỉnh
  thoảng mới cần.
- Tự hỏi với **từng dòng**: *"Xóa dòng này thì Claude có làm sai không?"* Không sai thì xóa.
- Có nhiều cấp, **cộng dồn** với nhau: `~/.claude/CLAUDE.md` (mọi project của bạn), `./CLAUDE.md`
  (commit cho team), CLAUDE.md trong thư mục con (nạp khi Claude làm việc ở đó).
- Giữ dưới **200 dòng** (repo này: < 100). Phình ra thì chuyển sang rules hoặc skill. `/doctor` có
  thể gợi ý chỗ cắt.

**Rules** = CLAUDE.md chia nhỏ theo chủ đề trong `.claude/rules/*.md`.
- Không có `paths:` → nạp mọi phiên như CLAUDE.md.
- Có `paths:` → chỉ nạp khi Claude đụng file khớp, nên tiết kiệm context. Đổi lại, nó **mất sau
  compact** cho tới khi file khớp được đọc lại (Module 3, mục 3.5).

⚠️ **CLAUDE.md là lời dặn, không phải luật.** Claude *thường* làm theo, nhưng không có gì bảo đảm.
Thứ gì bắt buộc 100% thì dùng hook (4.6).

### 4.3 Skills: "biết khi cần" + quy trình gọi bằng `/tên`

Skill = một thư mục `.claude/skills/<tên>/SKILL.md` gồm frontmatter + hướng dẫn markdown.

```markdown
---
name: til
description: Ghi 1 điều vừa học vào memory/notes. Dùng khi người học nói "til" hoặc "vừa học được".
---
1. Đọc memory/NOTES.md, chọn file chủ đề phù hợp...
```

Skill được nạp theo **2 tầng**:
1. **Đầu phiên:** chỉ nạp `name` + `description`, rất rẻ. Claude dựa vào description để tự quyết
   lúc nào dùng skill, nên **description phải rõ "làm gì + khi nào dùng"**. Description mơ hồ thì
   skill sẽ không tự kích hoạt, hoặc kích hoạt nhầm.
2. **Khi dùng:** gõ `/til`, hoặc Claude thấy hợp thì tự gọi. Lúc này mới nạp toàn bộ nội dung.

Có 2 loại skill:
- **Reference:** kiến thức dùng suốt phiên, ví dụ style guide API.
- **Action:** việc cụ thể, ví dụ `/deploy`, `/save-progress`.

Vài field frontmatter đáng nhớ:
- `disable-model-invocation: true`: chỉ **bạn** gọi được, Claude không tự gọi. Dùng cho skill có
  tác dụng phụ (deploy, gửi tin nhắn). Description cũng không bị nạp nên tốn 0 context.
- `context: fork`: chạy skill trong context riêng, giống subagent.
- Giữ SKILL.md dưới 500 dòng. Chi tiết tách ra file bên cạnh và link sâu 1 cấp.

Claude Code có sẵn vài skill (bundled skill): `/code-review`, `/debug`, `/batch`...

### 4.4 Subagents: "làm ở phòng riêng, chỉ mang kết quả về"

Subagent = file `.claude/agents/<tên>.md`, gồm frontmatter (`name`, `description`, `tools`, `model`,
`skills`) cộng với **system prompt riêng** ở phần thân.

Subagent tồn tại vì **ràng buộc 1** ở Module 3: context đầy thì Claude làm kém. Subagent có thể đọc
30 file, chạy 50 lệnh, nhưng phiên chính chỉ nhận lại **bản tóm tắt** vài đoạn.

Context của subagent lúc khởi động gồm:
- system prompt **của nó**, không phải system prompt của Claude Code;
- CLAUDE.md và git status (riêng agent built-in `Explore` và `Plan` bỏ qua 2 thứ này);
- skill liệt kê trong `skills:`, nạp sẵn toàn bộ;
- prompt mà phiên chính giao cho nó.

→ Subagent **không thấy lịch sử hội thoại** của bạn với phiên chính. Đây vừa là ưu điểm (sạch,
không thiên vị, nên mới dùng để review được) vừa là bẫy: phiên chính phải viết prompt giao việc
**đủ ý**.

| | Skill | Subagent |
|---|---|---|
| Là gì | Nội dung/quy trình tái sử dụng | Worker cách ly có context riêng |
| Ảnh hưởng context chính | **Cộng vào** context chính | Context riêng, chỉ trả tóm tắt |
| Hợp với | Tài liệu tham khảo, quy trình gọi bằng `/tên` | Việc đọc nhiều file, chạy song song, chuyên gia |

Có thể kết hợp 2 thứ: subagent nạp sẵn skill qua `skills:`, còn skill có `context: fork` thì chạy như subagent.

### 4.5 MCP: "thêm tay mới" để chạm hệ thống bên ngoài

**MCP (Model Context Protocol)** là giao thức chuẩn để một **server** cung cấp tool cho Claude:
đọc ticket Jira, query database, điều khiển trình duyệt... Đây là những thứ tool có sẵn
(Read/Edit/Bash) không làm được, hoặc làm rất vụng.

- Server lo phần kết nối và xác thực (OAuth...). Claude chỉ thấy các tool như `getJiraIssue`.
- Thêm server: `claude mcp add --transport http <tên> <url>`. Xem danh sách: `claude mcp list`, hoặc
  `/mcp` ngay trong phiên.
- Phạm vi cài đặt:
  - `local`: chỉ bạn, chỉ project này (mặc định);
  - `project`: ghi vào `.mcp.json` để commit cho team;
  - `user`: mọi project của bạn.
- **Tốn context ít:** đầu phiên chỉ nạp **tên tool**, schema đầy đủ hoãn tới khi cần (tool search).
  Ngay phiên này bạn thấy điều đó: Jira, Figma, Drive... hiện ra dưới dạng "deferred tools".
- ⚠️ Server MCP bên thứ ba có thể đọc dữ liệu hoặc nhận prompt injection, nên chỉ cài server tin cậy.

**MCP và Skill là 2 thứ khác nhau**, và thường đi cùng nhau. MCP cho **khả năng** (kết nối database).
Skill cho **cách dùng tốt** (schema của team, các mẫu query hay dùng).

### 4.6 Hooks: "luôn xảy ra, không cần Claude nhớ"

Hook là lệnh shell (hoặc HTTP, prompt, subagent) mà **harness** chạy tại một sự kiện. Model không
quyết định có chạy hay không, nên hook mang tính **tất định (deterministic)**.

Các sự kiện hay dùng:

| Sự kiện | Khi nào | Dùng để |
|---|---|---|
| `SessionStart` | Bắt đầu/resume phiên, sau `/clear`, sau compact | Nạp thêm ngữ cảnh (stdout → vào context) |
| `UserPromptSubmit` | Bạn gửi prompt, trước khi Claude xử lý | Thêm ngữ cảnh, chặn prompt |
| `PreToolUse` | Trước khi chạy tool | **Chặn** lệnh nguy hiểm, bảo vệ file `.env` |
| `PostToolUse` | Sau khi tool chạy thành công | Format/lint sau mỗi lần Edit |
| `Stop` | Claude trả lời xong | Ép chạy test, gửi thông báo |

Cấu trúc trong `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          { "type": "command", "command": "echo 'Nhắc: đọc memory/PROGRESS.md, dùng Python + .venv'" }
        ]
      }
    ]
  }
}
```

- `matcher` lọc trường hợp. Với `PreToolUse`/`PostToolUse`, matcher là **tên tool**, ví dụ `"Edit|Write"`.
  Với `SessionStart`, matcher là **nguồn**: `startup`, `resume`, `clear`, `compact`. Để `""` thì khớp tất cả.
- Hook nhận dữ liệu sự kiện dạng JSON qua **stdin**, ví dụ `tool_input.file_path`.
- **Exit code:**
  - `0` = cho qua. Với `SessionStart`/`UserPromptSubmit`, stdout được **thêm vào context**.
  - `2` = **chặn**, lý do ghi ra stderr. Ở `PreToolUse`, Claude nhận lý do này để tự điều chỉnh.
    Riêng `SessionStart` thì không chặn được.
  - Mã khác = lỗi không chặn, việc vẫn tiếp tục.

💡 Ví dụ trên chính là **cách thứ 3** để chữa "quy tắc bị quên sau compact" (câu hỏi đang mở trong
PROGRESS): hook `SessionStart` + matcher `compact` bơm lại quy tắc vào context sau mỗi lần compact.

> **Luật vàng:** "đừng sửa `.env`" ghi trong CLAUDE.md là **lời nhờ**. Một hook `PreToolUse` exit 2
> khi đường dẫn chứa `.env` mới là **cưỡng chế**.

### 4.7 Chi phí context của từng thứ

| Thứ | Nạp lúc nào | Tốn context |
|---|---|---|
| CLAUDE.md | Đầu phiên, toàn bộ | **Mọi request**, nên giữ ngắn |
| Rules có `paths:` | Khi đụng file khớp | Chỉ khi cần |
| Skill | Description đầu phiên, nội dung khi dùng | Thấp |
| MCP | Tên tool đầu phiên, schema khi dùng | Thấp tới khi dùng |
| Subagent | Khi được gọi | Context **riêng**, chỉ tóm tắt quay về |
| Hook | Khi sự kiện xảy ra | **0**, trừ khi in output vào context |

Thêm càng nhiều thứ thì càng **nhiễu**, không chỉ tốn tiền: skill có thể kích hoạt sai, Claude có thể quên
quy ước. `/context` (hoặc `/context all`) cho bạn xem từng thứ đang chiếm bao nhiêu token.

### 4.8 Khi nào thêm cái gì, và mổ xẻ repo này

Đừng cấu hình hết ngay từ đầu. Hãy thêm **khi gặp tín hiệu**:

| Tín hiệu | Thêm |
|---|---|
| Claude làm sai một quy ước **2 lần** | 1 dòng CLAUDE.md |
| Gõ đi gõ lại cùng một prompt mở đầu | Skill gọi bằng `/tên` |
| Dán cùng một quy trình nhiều bước lần thứ 3 | Skill |
| Cứ phải copy dữ liệu từ tab trình duyệt vào | MCP server |
| Việc phụ làm ngập hội thoại bằng output không cần xem lại | Subagent |
| Muốn việc gì đó **luôn** xảy ra mà không phải nhắc | Hook |
| Repo thứ 2 cần cùng setup | Plugin |

Chính repo này dùng gần đủ cả 6 thứ:

| Thứ | Trong repo | Vì sao chọn loại này |
|---|---|---|
| CLAUDE.md | [CLAUDE.md](../../CLAUDE.md) | Mọi phiên đều phải biết: đọc PROGRESS, dạy kiểu mentor |
| Rule có `paths:` | [memory-files.md](../../.claude/rules/memory-files.md) | Chỉ cần khi sửa memory/labs, không cần mọi phiên |
| Skill | [save-progress](../../.claude/skills/save-progress/SKILL.md), [hoc-tiep](../../.claude/skills/hoc-tiep/SKILL.md) | Quy trình nhiều bước, bạn chủ động gọi |
| Subagent | [ai-mentor](../../.claude/agents/ai-mentor.md) | Giảng sâu hoặc quiz mà không làm đầy phiên chính |
| MCP | (connector claude.ai: Jira, Drive...) | Dữ liệu nằm ngoài máy |
| Hook | **chưa có, bạn sẽ tạo** | Hiện `git status` mỗi lần mở phiên, không cần nhờ |

---

## Tóm tắt 1 phút
- **Luôn biết** → CLAUDE.md/rules. **Biết khi cần** → skill. **Cách ly** → subagent.
  **Chạm bên ngoài** → MCP. **Bắt buộc xảy ra** → hook. **Đóng gói** → plugin.
- CLAUDE.md và skill là *lời dặn*. Hook là *luật*.
- Mỗi thứ thêm vào đều tốn context và tạo nhiễu. Chỉ thêm khi gặp tín hiệu.

## Câu hỏi tự kiểm tra
1. Bạn muốn Claude **không bao giờ** chạy `git push --force`. Ghi vào CLAUDE.md hay dùng hook? Hook nào, exit code mấy?
2. Skill `/til` của bạn không tự kích hoạt khi bạn nói "hôm nay mình học được...". Sửa ở đâu?
3. Vì sao subagent review code tốt hơn chính phiên vừa code? Nó thấy gì và không thấy gì?
4. MCP server và skill khác nhau thế nào? Cho 1 ví dụ dùng cả hai.
5. Viết `matcher` và `command` cho hook in `git status --short` mỗi khi mở phiên mới.
