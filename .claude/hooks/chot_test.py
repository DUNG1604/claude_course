# .claude/hooks/chot_test.py — Stop hook: chỉ cho Claude dừng khi test playground xanh.
# Dùng cho lab 02 Module 4 (§4.4). Bật bằng: claude --settings labs/02-claude-code-in-action/stop-hook.json
import json, os, subprocess, sys

sys.stderr.reconfigure(encoding="utf-8")   # Windows mặc định cp1252 → in tiếng Việt sẽ lỗi

data = json.load(sys.stdin)                # Claude Code gửi JSON vào stdin: session_id, transcript_path, cwd, stop_hook_active...
if data.get("stop_hook_active"):           # True = turn này đã bị hook chặn 1 lần, Claude đang làm tiếp
    sys.exit(0)                            # → cho dừng, tránh vòng lặp vô hạn

repo = os.environ.get("CLAUDE_PROJECT_DIR", ".")   # Claude Code đặt biến này = gốc project
r = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "labs/02-claude-code-in-action/playground"],
    cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace",
    env={**os.environ, "PYTHONIOENCODING": "utf-8"},   # process con cũng ghi utf-8, nếu không tiếng Việt bị vỡ
)
if r.returncode != 0:                      # test đỏ
    print("Test đang đỏ, sửa code (KHÔNG sửa/xóa test cho pass):\n" + r.stderr[-1500:], file=sys.stderr)
    sys.exit(2)                            # exit 2 = chặn dừng; stderr thành feedback cho Claude
sys.exit(0)                                # test xanh → cho dừng
