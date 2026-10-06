# Lab 02 — Claude Code in Action (thực hành song song khóa học)

Khóa: https://anthropic.skilljar.com/claude-code-in-action · Chỉ cần subscription.
Mục tiêu khóa: chạy Claude **lâu hơn, ít giám sát hơn** mà vẫn **tin được kết quả**.

**Cách học:** đọc bài giảng module → làm phần tương ứng dưới đây → tick `[x]`.

| Module | Bài giảng | Nội dung |
|---|---|---|
| 1. Steer the Work | [bai-giang-module-1.md](bai-giang-module-1.md) | Lái phiên dài: queue, Esc, rewind, /goal |
| 2. Configure Claude | [bai-giang-module-2.md](bai-giang-module-2.md) | CLAUDE.md hiệu quả, verification skills, permission modes, hooks |
| 3. Automate Repeat Work | [bai-giang-module-3.md](bai-giang-module-3.md) | Routines, headless `claude -p`, GitHub Actions, code review |
| 4. Verify and Share | (sắp soạn) | Kiểm chứng phiên chạy không giám sát, plugins |
| 5. Assessment | — | Quiz khóa |

---

## Module 1 — Steer the Work

Sân tập: thư mục [playground/](playground/) (Claude sẽ tạo code ở đây, phá thoải mái).

- [x] **Queue:** nhờ Claude *"viết `playground/text_stats.py` gồm hàm đếm từ, đếm câu, từ dài nhất,
      kèm `test_text_stats.py` dùng `unittest`"*. **Trong lúc Claude đang chạy**, gõ thêm
      *"đếm từ phải bỏ qua dấu câu"* rồi Enter. Quan sát: Claude có nhận tin nhắn giữa chừng không?
- [x] **Ctrl+T / Ctrl+O:** trong lúc Claude làm, bật danh sách task và transcript (CLI).
- [x] **/btw:** khi Claude đang chạy, hỏi `/btw hàm nào đang được viết?`. Có làm gián đoạn không?
- [x] **Esc + rewind:** bảo Claude thêm một tính năng bạn *không* muốn giữ, rồi `Esc Esc` →
      **Restore code**. Kiểm tra file đã quay về chưa. Sau đó thử nhờ Claude xóa file bằng
      lệnh `rm` rồi rewind → khôi phục được không? Vì sao?
- [x] **/goal:** `/goal python -m unittest discover -s labs/02-claude-code-in-action/playground exits 0,
      có ít nhất 8 test, không sửa test cũ để cho pass — hoặc dừng sau 10 turn`.
      Quan sát verdict của evaluator (Ctrl+O để xem lý do).
- [ ] Tự ghi (phần Rút ra): khác nhau giữa *queue*, *Esc*, *rewind*, *`/goal`*.

## Module 2 — Configure Claude

- [ ] **Audit CLAUDE.md:** nhờ Claude *"rà CLAUDE.md theo bảng chẩn đoán ở Module 2 §2.2: dòng nào mơ hồ,
      thừa, mâu thuẫn, hay nên chuyển thành hook?"*. Chọn ít nhất 1 đề xuất để sửa, rồi kiểm chứng hành vi. — *bỏ qua 2026-10-06*
- [ ] **Auto mode + ranh giới:** ở auto mode, nói *"phiên này đừng commit gì nhé"*, nhờ sửa 1 file trong
      `playground/`, rồi bảo *"commit đi"*. Quan sát classifier xử lý ra sao. Sau đó gỡ ranh giới. — *bỏ qua 2026-10-06*
- [x] **Permission rule:** thêm `deny` cho `Bash(git push --force *)` vào `.claude/settings.json`.
      Kiểm chứng bằng `/permissions` (đừng thử push thật).
- [x] **Verification skill:** tạo skill `kiem-tra-memory` chạy lệnh đếm dòng và so với
      [rule độ dài](../../.claude/rules/memory-files.md), báo file nào vượt. Dùng trước mỗi lần commit memory.
- [ ] Tự ghi (phần Rút ra): CLAUDE.md, `/goal`, Stop hook, `deny` rule — mỗi cái chắc chắn tới mức nào? — *bỏ qua 2026-10-06*

## Module 3 — Automate Repeat Work

Bài 1–3 chạy bằng **subscription** (không cần API credits). Trước khi làm: `/status` phải báo login claude.ai,
và shell **không** có biến `ANTHROPIC_API_KEY` (nếu có, `claude -p` dùng key mẫu và lỗi). Không dùng `--bare`.

- [ ] **Headless → JSON:** viết `automation/tom_tat_git_log.py` gọi `claude -p` qua `subprocess`
      (stdin = `git log --oneline -20`, `--output-format json`, `--max-turns 1`). In `result`, `session_id`,
      `total_cost_usd`. Nâng cấp: thêm `--json-schema` (vd `{"tom_tat": str, "chu_de": [str]}`), đọc
      `structured_output`, ghi ra `automation/git-log-summary.json`. Đạt: chạy 2 lần đều ra JSON hợp lệ, exit 0.
- [ ] **Headless + quyền:** chạy `claude -p "/kiem-tra-memory" --output-format json` **không** cấp quyền →
      xem `permission_denials` (mode mặc định của `-p` là Manual). Rồi chạy lại với
      `--allowedTools "Bash(.venv/Scripts/python *)"`. Đạt: giải thích được vì sao lần 1 bị chặn, lần 2 chạy;
      và vì sao deny rule force push vẫn có hiệu lực trong `-p`.
- [ ] **CI tất định (không Claude):** nhờ Claude viết `.github/workflows/kiem-tra-memory.yml` chạy
      `python .claude/skills/kiem-tra-memory/check_lengths.py` khi push/PR (script chỉ dùng stdlib, không cần
      `pip install`). Kiểm chứng: tạo nhánh thử có file `memory/notes/*.md` > 150 dòng, mở PR → check **đỏ**;
      xóa file → **xanh**. Không tốn credits, chỉ tốn phút GitHub Actions.
- [ ] **Lên lịch:** trong phiên, `/loop 5m chạy /kiem-tra-memory và báo 1 dòng` → xem 2 lần chạy rồi hủy
      (*"cancel the loop"*). Rồi `/schedule` một routine **one-off** (vd *"in 1 hour, chạy check_lengths.py trên repo
      và tóm tắt kết quả, không push gì"*). Mở run trên `claude.ai/code/routines`, đọc transcript (đừng tin
      trạng thái xanh). Đạt: so sánh được `/loop` vs routine theo bảng §3.4. Cần GitHub đã kết nối với claude.ai.
- [ ] *(Tùy chọn — tốn hạn mức subscription + phút Actions, cần quyền admin repo + `gh`)* **`@claude` trên GitHub:**
      `/install-github-app` → chọn **token subscription** (`CLAUDE_CODE_OAUTH_TOKEN`), **không** chọn API key.
      Merge PR workflow, thêm `claude_args: "--max-turns 5"`, rồi comment `@claude tóm tắt PR này` trên một PR thử.
      Kết hợp: chạy `/code-review` local trên nhánh đó trước khi push. Bản dùng `ANTHROPIC_API_KEY` = **cần API credits**,
      bỏ qua cho tới khi nạp. Code Review managed = Team/Enterprise, ngoài phạm vi.
- [ ] Tự ghi (phần Rút ra): việc lặp lại nào trong repo này đáng tự động hóa, và chạy ở đâu (theo bảng §3.8)?

## Module 4 — Verify and Share
(Thêm checklist khi soạn bài giảng module 4.)

## Module 5 — Assessment
- [ ] Quiz khóa trên Skilljar.
- [ ] `/save-progress` rồi push.

---

## Rút ra (tự ghi)
-
