# Plugin Claude Code — đóng gói skill mang sang repo khác

Lab: `labs/02-claude-code-in-action/` Module 4 §4.7 (làm 2026-10-22). Plugin: `plugins/hoc-tap/`.

## Cấu trúc & vòng phát triển
```
plugins/hoc-tap/
├── .claude-plugin/plugin.json   ← CHỈ manifest trong đây (skills/ để trong này = không load skill nào)
└── skills/<tên>/SKILL.md        ← gọi bằng /hoc-tap:<tên> (name trong manifest = tiền tố)
```
`claude plugin validate ./plugins/hoc-tap` → `claude --plugin-dir ./plugins/hoc-tap` (chỉ 1 phiên)
→ sửa → `/reload-plugins` → `/plugin` tab Errors. Cảnh báo thiếu icon/LICENSE chỉ quan trọng khi publish.

## 3 lỗi đường dẫn khi chép skill từ `.claude/skills/` sang plugin
| Lỗi | Triệu chứng | Sửa |
|---|---|---|
| SKILL.md ghi cứng `.claude/skills/.../check_lengths.py` | Plugin **mượn** script bản gốc; kết quả đúng nên tưởng ổn. Chỉ thấy qua `Ctrl+O` | `"${CLAUDE_SKILL_DIR}/check_lengths.py"` |
| Link tương đối `../../rules/...` | Trỏ ra ngoài plugin, file không tồn tại | Ghi rõ "`.claude/rules/...` của repo đang mở" |
| Script `ROOT = parents[3]` | Ở vị trí mới = `plugins/` → đếm **0 file mà vẫn exit 0** | `CLAUDE_PROJECT_DIR` hoặc `Path.cwd()` + chặn "0 file" → exit 1 |

Quy tắc: file **đi theo plugin** (script) → `${CLAUDE_SKILL_DIR}` / `${CLAUDE_PLUGIN_ROOT}`;
file **thuộc repo đang mở** (memory, rules) → đường dẫn từ gốc repo, không `../`.

## Marketplace (§4.8, làm 2026-10-26)
`.claude-plugin/marketplace.json` ở **gốc repo** = danh mục: `name` (sau `@`), `plugins[].name` (trước `@`,
trùng plugin.json), `source: "./plugins/hoc-tap"` (từ gốc marketplace, cấm `..`). 1 marketplace chứa nhiều plugin.
```
claude plugin marketplace add ./                         # chỉ đăng ký danh mục, KHÔNG cài gì (ghi vào user settings)
claude plugin install hoc-tap@dung-tools --scope local   # ghi enabledPlugins vào .claude/settings.local.json
claude plugin marketplace remove dung-tools              # gỡ luôn plugin cài từ nó
```
- Cài/add **lần 2** → bỏ qua, báo "already installed" / "already on disk".
- Source local path → plugin đọc **tại chỗ**, sửa file chỉ cần `/reload-plugins`.
- `validate` chỉ kiểm cấu trúc, không kiểm logic (bài 3 pass validate mà script vẫn đếm 0 file).

## Bài học Module 4
- Lời tóm tắt "exit 0, đạt" là *tuyên bố*; transcript (`Ctrl+O`) là *bằng chứng*. Lỗi 1 chỉ lộ khi xem lệnh thật.
- Kiểm tra "không tìm thấy gì" mà báo pass = pass giả. Verification script phải fail khi input rỗng.
- Bản gốc `.claude/` vẫn load song song với plugin: skill không đụng nhờ tiền tố, nhưng hook sẽ chạy 2 lần.
