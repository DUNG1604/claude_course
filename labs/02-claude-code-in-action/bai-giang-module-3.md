# Bài giảng — Claude Code in Action · Module 3: Automate Repeat Work

> Nguồn: [Headless / `claude -p`](https://code.claude.com/docs/en/headless),
> [Routines](https://code.claude.com/docs/en/routines), [`/loop` & scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks),
> [GitHub Actions](https://code.claude.com/docs/en/github-actions), [Code Review](https://code.claude.com/docs/en/code-review),
> [Authentication](https://code.claude.com/docs/en/authentication). Soạn 2026-10-06.
> Skilljar module 3 gồm 2 bài: *"Routines and Headless"* và *"GitHub Actions and Code Review"* — nội dung bài
> trên Skilljar cần đăng nhập, file này soạn theo docs chính thức cùng chủ đề.

**Mục lục**
- 3.1 Module này để làm gì
- 3.2 Headless `claude -p`: Claude như một lệnh CLI
- 3.3 Quyền trong headless: không ai ngồi bấm "Allow"
- 3.4 Lên lịch: `/loop`, Desktop task, Routines (`/schedule`)
- 3.5 GitHub Actions: `claude-code-action` và `@claude`
- 3.6 Code review tự động: `/code-review`, review trong CI, Code Review managed
- 3.7 Tiền nào của nấy: cái gì cần API credits
- 3.8 Bảng chọn: việc lặp lại này nên chạy ở đâu

Trước đó: [Module 2](bai-giang-module-2.md) · Thực hành: [README lab, phần Module 3](README.md)

---

### 3.1 Module này để làm gì

Module 1–2: bạn **ngồi trong phiên** (lái, cấu hình). Module 3: **không có phiên nào để ngồi** — Claude chạy theo
lệnh của script, theo giờ, hoặc theo sự kiện GitHub.

| Kích hoạt bởi | Công cụ | Chạy ở đâu |
|---|---|---|
| Script / terminal của bạn | `claude -p` (headless) | Máy bạn |
| Đồng hồ, trong phiên đang mở | `/loop` | Máy bạn |
| Đồng hồ / API / sự kiện GitHub, không cần máy | **Routine** (`/schedule`) | Cloud Anthropic |
| Sự kiện GitHub (comment, PR, cron) | GitHub Actions + `claude-code-action` | Runner GitHub |
| Diff trước khi merge | `/code-review` | Máy bạn (hoặc cloud) |

Nguyên tắc xuyên suốt: chạy không giám sát thì **prompt phải tự đủ nghĩa** và **kết quả phải kiểm được**
(exit code, JSON, PR để review) — đúng tinh thần verification ở Module 2.

### 3.2 Headless `claude -p`: Claude như một lệnh CLI

`-p` (`--print`) = chạy 1 lần, in kết quả, thoát. Đọc **stdin**, nên ghép pipe được như `grep`:

```bash
# Git Bash
git log --oneline -20 | claude -p "Tóm tắt 20 commit này thành 3 gạch đầu dòng tiếng Việt"
```

**Exit code:** 0 = thành công, khác 0 = lỗi → script rẽ nhánh được. Lỗi *trong* lượt chạy (vd chưa đăng nhập)
được in ra stdout như kết quả, không phải stderr.

**`--output-format`:**

| Giá trị | Ra gì | Dùng khi |
|---|---|---|
| `text` (mặc định) | Chữ thuần | Đọc bằng mắt, ghi file |
| `json` | 1 object: `result`, `session_id`, `total_cost_usd`, usage... | Script cần parse |
| `stream-json` | Mỗi dòng 1 event JSON (cần thêm `--verbose`) | UI realtime, theo dõi tool call |

Thêm `--json-schema '<schema>'` (đi với `--output-format json`) → kết quả đúng schema nằm ở field
**`structured_output`** (không phải `result`). Schema sai → `claude` báo lỗi và thoát.

```powershell
# PowerShell: không cần jq, ConvertFrom-Json có sẵn
$r = git log --oneline -20 | claude -p "Tóm tắt các commit" --output-format json | ConvertFrom-Json
$r.result; $r.session_id; $r.total_cost_usd
```

Trong Python (đúng ngôn ngữ chính của repo) thì gọi qua `subprocess.run([...], input=..., capture_output=True)`
rồi `json.loads(stdout)` — truyền list đối số, tránh hẳn chuyện escape dấu nháy của PowerShell.

**Cờ hay dùng với `-p`:**

| Cờ | Tác dụng |
|---|---|
| `--max-turns N` | Giới hạn số turn agentic; chạm trần → thoát **có lỗi** |
| `--allowedTools "Read,Bash(git log *)"` | Cho phép tool không cần hỏi (cú pháp giống permission rule) |
| `--permission-mode <mode>` | Mode nền cho cả lượt chạy (3.3) |
| `--append-system-prompt "..."` | Thêm chỉ dẫn, giữ nguyên hành vi mặc định |
| `--continue` / `--resume <session_id>` | Hỏi tiếp cuộc hội thoại trước |
| `--bare` | Bỏ qua CLAUDE.md, hooks, skills, MCP... → kết quả giống nhau mọi máy. **Chỉ dùng API key** |
| `--max-budget-usd` | Trần chi phí (ước tính phía client) |

Skill của bạn gọi được trong `-p`: `claude -p "/kiem-tra-memory"`. Lệnh chỉ có trong giao diện (vd `/login`) thì không.

**Bẫy:**
- **`--bare` không đọc đăng nhập subscription** (cũng không đọc `CLAUDE_CODE_OAUTH_TOKEN`) → bạn chưa có credits
  thì **đừng dùng `--bare`**. Không có `--bare`, `-p` dùng login subscription như phiên thường.
- **`ANTHROPIC_API_KEY` trong biến môi trường thắng subscription**, và ở `-p` được dùng luôn không hỏi.
  Key mẫu trong `.env` chỉ được `python-dotenv` nạp vào process Python — nhưng nếu bạn `export`/`$env:` nó ra
  shell, `claude -p` sẽ dùng key đó và lỗi. Kiểm bằng `/status`.
- Không có `--bare`, `-p` **chạy hooks và nạp settings của thư mục** kể cả thư mục chưa trust, không hỏi.
  Chạy `claude -p` trong repo lạ = chạy hook của người khác.
- `total_cost_usd` là **ước tính**; dùng subscription thì không bị trừ tiền theo số đó, mà trừ vào hạn mức gói.

### 3.3 Quyền trong headless: không ai ngồi bấm "Allow"

Mode khởi đầu của `claude -p` mặc định là **`default` (Manual)**, khác phiên terminal (auto). Không có ai trả lời
→ mọi hành động **cần hỏi đều bị từ chối**, Claude chạy tiếp và thường báo "không có quyền". Muốn nó làm được:

| Cách | Ví dụ | Khi nào |
|---|---|---|
| Chỉ cho đúng tool cần | `--allowedTools "Bash(git diff *),Bash(git commit *)"` | **Mặc định nên dùng** |
| Khóa chặt | `--permission-mode dontAsk` + `allowedTools` | CI: ngoài danh sách là từ chối |
| Cho sửa file | `--permission-mode acceptEdits` | Lint fix, format |
| Classifier canh | `--permission-mode auto --permission-prompts none` | Việc dài, nhiều lệnh khó liệt kê |

- `Bash(git diff *)` — **dấu cách trước `*`** quan trọng; `Bash(git diff*)` khớp cả `git diff-index`.
- **`deny` rule trong `.claude/settings.json` vẫn áp dụng** cho `-p` (khi không `--bare`) → rule chặn force push
  của bạn bảo vệ cả script headless.
- Với `--output-format json`, các lần bị từ chối nằm trong `permission_denials` → script tự phát hiện "thiếu quyền".
- **Đừng** `--dangerously-skip-permissions` ngoài container cô lập (Module 2 §2.4).

### 3.4 Lên lịch: `/loop`, Desktop task, Routines (`/schedule`)

| | `/loop` | Desktop scheduled task | **Routine** (cloud) |
|---|---|---|---|
| Chạy trên | Máy bạn | Máy bạn | Cloud Anthropic |
| Cần máy bật / phiên mở | Có / **có** | Có / không | Không / không |
| Đọc file local | Có | Có | Không (clone mới từ GitHub) |
| Hỏi quyền | Theo phiên | Cấu hình được | **Không** — chạy tự động hoàn toàn |
| Khoảng tối thiểu | 1 phút | 1 phút | **1 giờ** |
| Tuổi thọ | Recurring hết hạn sau **7 ngày** | Lâu dài | Lâu dài |

**`/loop`** — polling trong phiên: `/loop 10m kiểm tra CI của PR và báo kết quả`. Bỏ interval → Claude tự chọn
nhịp (1 phút–1 giờ); bỏ cả prompt → chạy prompt bảo trì mặc định (hoặc `.claude/loop.md`). `Esc` dừng loop tự
nhịp. Đóng terminal → hết chạy. Nhắc 1 lần: *"in 45 minutes, check whether the tests passed"*.

**Routine** = prompt + repo + environment + connectors, lưu ở tài khoản claude.ai, chạy trên cloud kể cả khi tắt máy.
- Gói **Pro, Max, Team, Enterprise**; trạng thái **research preview**. Tạo ở `claude.ai/code/routines` hoặc CLI:
  `/schedule daily PR review at 9am`, `/schedule tomorrow at 9am, summarize yesterday's merged PRs`.
  Quản lý: `/schedule list`, `/schedule update`, `/schedule run` (alias `/routines`).
- **Trigger:** Schedule (CLI tạo được) · GitHub event (PR/release; cần cài Claude GitHub App) ·
  API (`POST .../fire` với bearer token — chỉ thêm được trên web).
- **Tính tiền:** trừ vào **hạn mức subscription** như phiên thường + trần riêng (100 scheduled run/giờ/tài khoản).
  Không cần API credits.
- `/schedule` **cần login claude.ai** — nếu đang dùng `ANTHROPIC_API_KEY` thì báo `Unknown command`.
  Org Team/Enterprise có thể bị Owner tắt Routines.

**Bẫy:**
- Routine **không có permission mode**: được chạy shell, dùng mọi tool của connector được tick (kể cả ghi) mà
  không hỏi → bỏ connector thừa; Claude chỉ push lên nhánh `claude/...`, bảo vệ `main` bằng branch protection.
- Commit/PR/tin nhắn do routine tạo **mang danh tính của bạn**.
- Trạng thái **xanh chỉ nghĩa là phiên không lỗi hạ tầng**, không phải task thành công → mở transcript mà đọc.
- Đặt giờ lệch phút tròn (9:07 thay vì 9:00) để chạy đúng giờ hơn.

### 3.5 GitHub Actions: `claude-code-action` và `@claude`

`anthropics/claude-code-action@v1` chạy Claude Code **trên runner GitHub**. Hai chế độ, tự nhận theo cấu hình:
- **Interactive** (không có input `prompt`): chờ `@claude` trong comment issue/PR → trả lời bằng comment, có thể push commit.
- **Automation** (có `prompt`): chạy theo bất kỳ event nào (`pull_request`, `schedule`...), kết quả ở log workflow.

**Cài:** trong `claude` gõ `/install-github-app` (cần quyền admin repo, `gh` đã `gh auth login`, chỉ github.com).
Lệnh cài Claude GitHub App, lưu secret, đẩy nhánh có workflow và mở PR để bạn merge.

**Xác thực — điểm quan trọng nhất với bạn:**

| Secret | Lấy ở đâu | Tính tiền | Input trong YAML |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Claude Console | **API credits** | `anthropic_api_key` |
| `CLAUDE_CODE_OAUTH_TOKEN` | `claude setup-token` (token 1 năm, gói Pro/Max/Team/Ent) | **Hạn mức subscription** | `claude_code_oauth_token` |

→ Bạn **dùng được GitHub Actions không cần credits** bằng OAuth token. Mọi ví dụ trong docs dùng API key; đổi
đúng 1 dòng sang `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`. Ngoài ra tốn **phút GitHub
Actions** (repo public miễn phí; private có hạn mức free).

```yaml
# .github/workflows/claude.yml — trả lời @claude (rút gọn từ docs)
on:
  issue_comment: { types: [created] }
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write, issues: write, id-token: write }
    steps:
      - uses: actions/checkout@v6
      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          claude_args: "--max-turns 5"
```

- `claude_args` nhận mọi cờ CLI: `--max-turns`, `--model`, `--allowedTools`... Ở automation mode, prompt thường
  **không có quyền shell** cho tới khi bạn cấp qua `--allowedTools`.
- Chỉ người có **write access** mới kích hoạt được; bot bị chặn (chống vòng lặp).
- **Không bao giờ** dán token/key vào YAML — luôn `secrets.*`. Token OAuth gắn với tài khoản *bạn*, không chia cho org.
- **Không phải việc gì cũng cần Claude trong CI.** Kiểm tra tất định (test, `check_lengths.py`) chạy bằng
  `run: python ...` — miễn phí, nhanh, không bao giờ "phán đoán sai". Dùng Claude cho phần cần đọc hiểu.

### 3.6 Code review tự động

| Cách | Ở đâu | Gói / tiền | Ghi chú |
|---|---|---|---|
| **`/code-review`** (alias `/review`) | Phiên local | Subscription | Review nhánh + thay đổi chưa commit; chạy nền bằng subagent |
| `/code-review ultra` | Cloud, nhiều agent | Cần login claude.ai | Sâu hơn, chậm hơn |
| Workflow `code-review` plugin | GitHub Actions | API key **hoặc** OAuth token | `/install-github-app` có tùy chọn workflow này |
| **Code Review (managed)** | Anthropic, tự chạy mọi PR | **Team/Enterprise + usage credits**, ~$15–25/review | Ngoài tầm bài lab |

`/code-review`: thêm target (`main...my-branch`, số PR, file), cờ `--fix` (áp sửa — **không** hoàn tác bằng
`/rewind` khi chạy nền, dùng git), `--comment` (đăng lên PR), mức effort (`low` ít báo nhầm, `high`/`max` rộng hơn).
Trong `-p` nó chạy foreground và trả findings dạng text → **dùng được trong script/CI**.

Review tuân theo CLAUDE.md; bản managed còn đọc `REVIEW.md` (luật riêng cho review: severity, giới hạn nit, bỏ qua
file nào). Nhớ bẫy reviewer ở Module 2: dặn chỉ báo lỗi ảnh hưởng tính đúng.

### 3.7 Tiền nào của nấy: cái gì cần API credits

| Tính năng | Subscription (bạn có) | Cần API credits |
|---|---|---|
| `claude -p` (không `--bare`) | Có | — |
| `claude -p --bare` | **Không** | Có |
| `/loop`, Desktop task | Có | — |
| Routines / `/schedule` | Có (Pro trở lên) | — |
| GitHub Action với `CLAUDE_CODE_OAUTH_TOKEN` | Có | — |
| GitHub Action với `ANTHROPIC_API_KEY` | — | Có |
| `/code-review` local | Có | — |
| Code Review managed | — | Team/Ent + usage credits |
| Agent SDK Python với API key | — | Có (khóa API sau này) |

### 3.8 Bảng chọn: việc lặp lại này nên chạy ở đâu

| Muốn | Dùng |
|---|---|
| Gọi Claude từ script, lấy JSON | `claude -p --output-format json` (+ `--json-schema`) |
| Canh 1 việc trong lúc đang làm | `/loop` |
| Chạy theo giờ, cần file trên máy | Desktop scheduled task |
| Chạy theo giờ / sự kiện, máy tắt cũng chạy | Routine (`/schedule`) |
| Gắn vào luồng PR/issue của team | GitHub Actions (`@claude`, `prompt`) |
| Kiểm tra pass/fail tất định | Script thường trong CI (không cần Claude) |
| Ý kiến thứ hai trước khi merge | `/code-review` (local) → workflow review (CI) |

---

## Câu hỏi tự kiểm tra
1. Script chạy `claude -p "sửa lỗi lint"` trả về "không có quyền sửa file". Vì sao, và 2 cách sửa?
2. Bạn thêm `--bare` để kết quả ổn định hơn thì lệnh lỗi xác thực. Vì sao? Phương án cho người chưa có credits?
3. Muốn mỗi sáng 9h tóm tắt commit hôm qua khi laptop đã tắt: `/loop`, Desktop task hay Routine? Vì sao?
4. Workflow docs dùng `anthropic_api_key`. Bạn sửa gì để chạy bằng subscription, và token lấy ở đâu?
5. `check_lengths.py` nên chạy trong CI bằng `claude-code-action` hay `run: python ...`? Lý do.
