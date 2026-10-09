# Bài giảng — Claude Code in Action · Module 4: Verify and Share

> Nguồn: [Best practices — verify / adversarial review](https://code.claude.com/docs/en/best-practices),
> [Hooks — Stop](https://code.claude.com/docs/en/hooks), [Sessions](https://code.claude.com/docs/en/sessions),
> [Settings](https://code.claude.com/docs/en/settings), [Plugins](https://code.claude.com/docs/en/plugins),
> [Create a plugin](https://code.claude.com/docs/en/plugins/create), [Marketplace](https://code.claude.com/docs/en/plugin-marketplaces),
> [Plugin security](https://code.claude.com/docs/en/plugins/security). Soạn 2026-10-09.
> Skilljar module 4 gồm: *"Trust It: Verifying Unsupervised Runs"*, *"Plugins"*, *Quiz*, *Course Quiz*. Nội dung bài
> cần đăng nhập; file này soạn theo docs chính thức cùng chủ đề.

**Mục lục**
- 4.1 Chuyện thật: "Claude báo xong rồi mà"
- 4.2 Kiểm chứng tỉ lệ với mức bạn *không* nhìn
- 4.3 Đọc bằng chứng của phiên không giám sát
- 4.4 Stop hook: chỉ cho dừng khi test xanh thật
- 4.5 Ý kiến thứ hai: reviewer không phải người viết
- 4.6 Chia sẻ cấu hình: cái gì commit, cái gì giữ riêng
- 4.7 Plugin: đóng gói setup bạn tin được
- 4.8 Marketplace: cả team cài bằng một lệnh

Trước đó: [Module 3](bai-giang-module-3.md) · Thực hành: [README lab, phần Module 4](README.md)

---

### 4.1 Chuyện thật: "Claude báo xong rồi mà"

**Tối thứ Sáu**, bạn chạy `claude -p "sửa hết lỗi test trong playground"` rồi đi ngủ. **Sáng thứ Bảy** output ghi:
*"Done. All tests pass ✅"*. Bạn merge. **Thứ Hai** CI đỏ. Đọc lại mới thấy: Claude không có quyền chạy `python`
(mode Manual của `-p`), nên nó *đoán* là pass. Có test nó còn "sửa" bằng cách xóa `assert`.

**Cùng tuần**, đồng nghiệp mới vào repo. Họ cần skill `kiem-tra-memory`, deny rule force push, hook SessionStart
của bạn. Bạn gửi zip, họ chép tay, sửa một chỗ. Hai tuần sau hai máy chạy hai bản khác nhau.

| | Không có Module 4 | Có Module 4 |
|---|---|---|
| Biết phiên chạy đêm có đúng không | Tin câu "Done ✅" | Đọc **bằng chứng**: lệnh đã chạy, exit code |
| Chặn "xong giả" | Hy vọng | **Stop hook** chạy test thật, đỏ thì không cho dừng |
| Phát hiện lỗi người viết không thấy | Tự review lúc mệt | **Reviewer** ở context mới |
| Đưa setup cho người khác | Zip + chép tay | **Plugin**, cài 1 lệnh, cập nhật từ 1 nguồn |

Câu tóm tắt của khóa: *kiểm chứng tỉ lệ với mức bạn không nhìn, chốt turn bằng kết quả test thật qua hooks,
đóng gói setup bạn tin được thành plugin cả team cài.*

### 4.2 Kiểm chứng tỉ lệ với mức bạn *không* nhìn

**Học xong làm được gì:** chọn đúng mức kiểm chứng cho từng việc, không thừa không thiếu.

Claude dừng khi việc **trông như** xong. Không có phép thử chạy được thì "trông như xong" là tín hiệu duy nhất,
và **bạn** thành vòng kiểm chứng. Docs chia 4 mức, càng xuống càng tốn công cài nhưng càng ít phải canh:

| Mức | Cách | Ai chấm | Hợp với |
|---|---|---|---|
| 1. Trong prompt | "viết xong chạy `python -m unittest`, sửa tới khi xanh" | Chính Claude | Bạn ngồi xem |
| 2. Cả phiên | `/goal <điều kiện>` (Module 1) | Model nhỏ đọc hội thoại | Phiên dài, bạn ghé xem |
| 3. Cổng tất định | **Stop hook** chạy script (4.4) | Exit code | Chạy đêm, không ai xem |
| 4. Ý kiến thứ hai | Subagent reviewer, `/code-review` (4.5) | Model khác, context mới | Trước khi merge |

Ví dụ đời thực: sửa typo bạn đang nhìn → mức 1. Routine chạy 3h sáng mở PR → mức 3 + 4.
Quy tắc docs: **"If you can't verify it, don't ship it."** Và bắt Claude **đưa bằng chứng** (output test, lệnh đã
chạy và kết quả) thay vì khẳng định "đã pass". Đọc bằng chứng nhanh hơn tự chạy lại.

### 4.3 Đọc bằng chứng của phiên không giám sát

**Học xong làm được gì:** sau một phiên `-p`/routine, tìm ra Claude *thật sự* đã chạy lệnh gì, kết quả gì.

| Muốn | Dùng | Ghi chú |
|---|---|---|
| Kết quả + chi phí + từ chối quyền | `claude -p ... --output-format json` | Đọc `result`, `session_id`, `permission_denials` |
| Hỏi lại chính phiên đó | `claude -p --resume <session_id> "liệt kê lệnh đã chạy và exit code"` | Phiên `-p` **không** hiện trong `/resume` picker, phải dùng ID |
| Mở lại phiên tương tác | `claude --resume <id>` rồi `Ctrl+O` xem transcript | Thấy từng tool call + output |
| Bản đọc được cho người | `/export ten-file.txt` trong phiên | Văn bản thuần |
| File gốc | `%USERPROFILE%\.claude\projects\<project>\<session-id>.jsonl` | Mỗi dòng 1 JSON; định dạng **nội bộ, đổi theo version** |
| Routine (cloud) | Mở run trên `claude.ai/code/routines` | Xanh = không lỗi hạ tầng, **không** phải task đúng |

Đọc transcript theo checklist 3 câu: (1) lệnh kiểm chứng **có được chạy** không, hay bị từ chối quyền?
(2) exit code là gì? (3) Claude có **sửa test/sửa phép thử** để cho qua không (`git diff` file test)?

**Bẫy:** transcript tự xóa sau **30 ngày** (`cleanupPeriodDays`). `--no-session-persistence` thì không có gì để đọc.
Đừng viết script parse `.jsonl` lâu dài; muốn tự động thì dùng JSON của `-p` hoặc `transcript_path` mà hook nhận.
Cấp tổ chức còn có OpenTelemetry (`CLAUDE_CODE_ENABLE_TELEMETRY=1`) đếm usage/tool, chưa cần ở giai đoạn này.

### 4.4 Stop hook: chỉ cho dừng khi test xanh thật

**Học xong làm được gì:** viết hook chạy test mỗi khi Claude định dừng; đỏ thì Claude phải làm tiếp.

Nhắc lại khóa 1: `Stop` chạy khi Claude **sắp kết thúc turn**. Hook trả **exit 2** (hoặc JSON
`{"decision": "block", "reason": "..."}`) → Claude **không được dừng**, đọc lý do và làm tiếp.
Khác `/goal`: không có model nào "phán", chỉ có exit code của test.

```python
# .claude/hooks/chot_test.py — Stop hook (Python, không cần jq trên Windows)
import json, subprocess, sys

data = json.load(sys.stdin)              # Claude Code gửi JSON vào stdin: session_id, transcript_path, ...
if data.get("stop_hook_active"):         # True = turn này đã bị hook chặn rồi, Claude đang làm tiếp
    sys.exit(0)                          # → cho dừng, tránh vòng lặp vô hạn (pattern trong docs)
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "labs/02-claude-code-in-action/playground"],
                   capture_output=True, text=True)
if r.returncode != 0:                    # test đỏ
    print("Test đang đỏ, sửa code (không sửa test):\n" + r.stderr[-1500:], file=sys.stderr)
    sys.exit(2)                          # exit 2 = chặn dừng; stderr thành feedback cho Claude
```

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command",
  "command": ".venv/Scripts/python .claude/hooks/chot_test.py" } ] } ] } }
```
`Stop` không cần `matcher`. `[-1500:]` chỉ gửi đuôi lỗi để khỏi tràn context.

**Bẫy:**
- Hook chạy **mỗi turn**, kể cả turn Claude chỉ trả lời câu hỏi → test phải **nhanh**; test chậm thì đừng dùng Stop hook.
- Pattern `stop_hook_active` ở trên chỉ cho **1 lần làm lại**. Bỏ nó thì Claude Code vẫn tự gỡ sau **8 lần chặn liên tiếp**
  không có tool call xen giữa, rồi dừng kèm cảnh báo. Đừng tưởng hook "bắt buộc tuyệt đối".
- Hook trong `.claude/settings.json` chạy cho **mọi người** clone repo. Đang thử thì để ở file riêng (lab dùng `--settings`).
- Muốn chặn cả kiểu "xóa assert cho qua": thêm điều kiện vào `reason`, hoặc để reviewer (4.5) bắt.

### 4.5 Ý kiến thứ hai: reviewer không phải người viết

**Học xong làm được gì:** nhờ một Claude *khác* tìm lỗi trong việc Claude vừa làm.

Người viết có thiên kiến với code của chính mình. Subagent reviewer chạy ở **context mới**, chỉ thấy diff + tiêu chí.

| Cách | Gõ gì | Khi nào |
|---|---|---|
| Review tính đúng | `/code-review` (Module 3 §3.6) | Mặc định trước khi merge |
| Review theo kế hoạch | *"Use a subagent to review the diff against PLAN.md. Report gaps, not style preferences."* | Có spec/plan |
| Writer / Reviewer | Phiên A viết, phiên B review, dán kết quả về A | Việc lớn |

**Bẫy (đã gặp ở Module 2):** reviewer được bảo "tìm lỗi" sẽ **luôn** tìm ra gì đó. Dặn: *chỉ báo lỗi ảnh hưởng tính đúng
hoặc yêu cầu*; còn lại là tùy chọn, không thì over-engineering.

### 4.6 Chia sẻ cấu hình: cái gì commit, cái gì giữ riêng

**Học xong làm được gì:** biết đặt một setting ở file nào để đúng người nhận được.

| Scope | File | Ai bị ảnh hưởng | Ví dụ trong repo này |
|---|---|---|---|
| Managed | `managed-settings.json` / console | Cả tổ chức, không ai đè được | (không có) |
| Local | `.claude/settings.local.json` (gitignore) | Bạn, repo này | Thử hook, quyền cá nhân |
| **Project** | `.claude/settings.json` (commit) | Mọi người clone repo | Deny force push, hook SessionStart |
| User | `%USERPROFILE%\.claude\settings.json` | Bạn, mọi project | Theme, model mặc định |

Thứ tự ưu tiên cao → thấp: Managed > `--settings` > Local > Project > User. Riêng **list** (vd `permissions.allow`)
được **gộp** từ mọi file chứ không đè. Ngoài settings, commit luôn `CLAUDE.md`, `.claude/skills/`, `.claude/agents/`,
`.claude/rules/`, `.mcp.json` → người clone có ngay. **Giới hạn:** chỉ dùng được trong *repo đó*. Muốn mang sang
repo khác hay phát phiên bản → plugin.

### 4.7 Plugin: đóng gói setup bạn tin được

**Học xong làm được gì:** gom skills + hooks + agents + MCP thành 1 thư mục cài được ở bất kỳ project nào.

Ví von: `.claude/` của repo = đồ đạc **gắn chết trong nhà**. Plugin = **vali** xách sang nhà khác, có số phiên bản.

```text
hoc-tap/                         ← plugin root (thư mục bạn đưa cho --plugin-dir)
├── .claude-plugin/plugin.json   ← CHỈ manifest nằm trong đây
├── skills/kiem-tra-memory/SKILL.md  → gọi bằng /hoc-tap:kiem-tra-memory
├── agents/reviewer.md           ← subagent hoc-tap:reviewer
├── hooks/hooks.json             ← cùng dạng "hooks" trong settings.json
└── .mcp.json                    ← MCP server (nếu có)
```
```json
{ "name": "hoc-tap", "description": "Skill học tập của repo learn-claude", "version": "0.1.0",
  "author": { "name": "dungnq" } }
```
`name` bắt buộc, thành **tiền tố** của mọi skill/agent (`/hoc-tap:til`) để 2 plugin cùng có `til` không đụng nhau.
`version` có đặt thì người dùng **đứng yên** ở bản đó tới khi bạn đổi số.

Vòng phát triển: `claude plugin validate ./hoc-tap` → `claude --plugin-dir ./hoc-tap` (chỉ phiên này, không cài) →
sửa file → `/reload-plugins` → `/plugin` tab **Errors** nếu thiếu gì.

**Bẫy:**
- Để `skills/` **trong** `.claude-plugin/` → plugin load nhưng không có skill nào.
- Bản gốc trong `.claude/` vẫn load song song: skill không đụng nhau nhờ tiền tố, nhưng **hook chạy 2 lần**.
- Link/đường dẫn tương đối hỏng khi rời chỗ cũ. Trong SKILL.md dùng `${CLAUDE_SKILL_DIR}` (thư mục skill),
  `${CLAUDE_PLUGIN_ROOT}` (gốc plugin), `${CLAUDE_PROJECT_DIR}` (repo đang mở). Script đoán gốc repo theo vị trí file
  (như `parents[3]` trong `check_lengths.py`) sẽ sai.
- Plugin bật là có mặt **mọi phiên**: tên + mô tả từng skill tốn context mỗi turn. Không dùng thì disable.
- Plugin **chạy với quyền của bạn**; hook và MCP server chạy **ngoài** permission rules/sandbox. Cài plugin lạ: đọc
  `hooks/hooks.json`, `.mcp.json`, `bin/` trước (`claude plugin details <tên>` liệt kê thành phần).

**Khi KHÔNG cần plugin:** chỉ mình bạn, chỉ một repo → để trong `.claude/` là đủ (4.6).

### 4.8 Marketplace: cả team cài bằng một lệnh

**Học xong làm được gì:** biến repo GitHub thành "cửa hàng" để đồng nghiệp cài plugin theo tên.

Marketplace = thư mục/repo có `.claude-plugin/marketplace.json` liệt kê plugin. Là **danh mục**, không phải store host.

```json
{ "name": "dung-tools", "owner": { "name": "dungnq" },
  "plugins": [ { "name": "hoc-tap", "source": "./plugins/hoc-tap", "description": "Skill học tập" } ] }
```
`source` tính từ **gốc marketplace** (thư mục chứa `.claude-plugin/`), cấm `..`. Tên entry phải **trùng** `name` trong plugin.json.

| Bước | Lệnh |
|---|---|
| Kiểm tra | `claude plugin validate ./` |
| Thêm marketplace | `claude plugin marketplace add ./` (local) hoặc `... add DUNG1604/claude_course` (GitHub) |
| Cài | `claude plugin install hoc-tap@dung-tools --scope user` (trong phiên: `/plugin`) |
| Xem | `claude plugin list`, `claude plugin details hoc-tap` |
| Gỡ sạch | `claude plugin marketplace remove dung-tools` |

**Scope khi cài:** *user* (bạn, mọi project) · *project* (ghi `enabledPlugins` vào `.claude/settings.json` đã commit, đồng
nghiệp vẫn phải tự cài trên máy họ) · *local* (bạn, repo này). Team muốn tự nhắc cài: commit `extraKnownMarketplaces`
+ `enabledPlugins` vào `.claude/settings.json`; người clone phải **trust** thư mục mới load.

| Muốn chia sẻ | Cách |
|---|---|
| 1 repo, cả team | Commit `.claude/` |
| Vài người, thử nhanh | Gửi thư mục plugin → `--plugin-dir` |
| Nhiều repo, có phiên bản, cập nhật | Marketplace riêng trên GitHub |
| Ai cũng dùng được | Nộp vào directory của Anthropic (ngoài phạm vi) |

---

## Câu hỏi tự kiểm tra
1. Phiên `-p` chạy đêm báo "All tests pass". Bạn kiểm 3 điều gì trong transcript trước khi tin, và lấy transcript bằng cách nào?
2. Stop hook trả exit 2 nhưng Claude vẫn dừng sau vài vòng. Hai nguyên nhân có thể là gì?
3. `/goal` và Stop hook chạy test khác nhau ở chỗ nào? Khi nào chọn cái nào?
4. Deny rule force push nên ở `.claude/settings.json` hay `settings.local.json`? Còn hook bạn đang thử nghiệm?
5. Bạn chép `kiem-tra-memory` vào plugin `hoc-tap`, gọi `/hoc-tap:kiem-tra-memory` thì script báo sai đường dẫn. Vì sao, sửa thế nào?
