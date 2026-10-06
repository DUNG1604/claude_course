# Lab 02 — Claude Code in Action (thực hành song song khóa học)

Khóa: https://anthropic.skilljar.com/claude-code-in-action · Chỉ cần subscription.
Mục tiêu khóa: chạy Claude **lâu hơn, ít giám sát hơn** mà vẫn **tin được kết quả**.

**Cách học:** đọc bài giảng module → làm phần tương ứng dưới đây → tick `[x]`.

| Module | Bài giảng | Nội dung |
|---|---|---|
| 1. Steer the Work | [bai-giang-module-1.md](bai-giang-module-1.md) | Lái phiên dài: queue, Esc, rewind, /goal |
| 2. Configure Claude | [bai-giang-module-2.md](bai-giang-module-2.md) | CLAUDE.md hiệu quả, verification skills, permission modes, hooks |
| 3. Automate Repeat Work | (sắp soạn) | Routines, headless `claude -p`, GitHub Actions, code review |
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
      thừa, mâu thuẫn, hay nên chuyển thành hook?"*. Chọn ít nhất 1 đề xuất để sửa, rồi kiểm chứng hành vi.
- [ ] **Auto mode + ranh giới:** ở auto mode, nói *"phiên này đừng commit gì nhé"*, nhờ sửa 1 file trong
      `playground/`, rồi bảo *"commit đi"*. Quan sát classifier xử lý ra sao. Sau đó gỡ ranh giới.
- [ ] **Permission rule:** thêm `deny` cho `Bash(git push --force *)` vào `.claude/settings.json`.
      Kiểm chứng bằng `/permissions` (đừng thử push thật).
- [ ] **Verification skill:** tạo skill `kiem-tra-memory` chạy lệnh đếm dòng và so với
      [rule độ dài](../../.claude/rules/memory-files.md), báo file nào vượt. Dùng trước mỗi lần commit memory.
- [ ] Tự ghi (phần Rút ra): CLAUDE.md, `/goal`, Stop hook, `deny` rule — mỗi cái chắc chắn tới mức nào?

## Module 3–4
(Thêm checklist khi soạn bài giảng từng module.)

## Module 5 — Assessment
- [ ] Quiz khóa trên Skilljar.
- [ ] `/save-progress` rồi push.

---

## Rút ra (tự ghi)
-
