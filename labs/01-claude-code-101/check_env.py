"""Kiểm tra .env có ANTHROPIC_API_KEY hợp lệ — KHÔNG BAO GIỜ in key ra màn hình.

Chạy: .\\.venv\\Scripts\\python.exe labs\\01-claude-code-101\\check_env.py
Exit code: 0 = ổn, 1 = có lỗi.
"""

import os
import sys
from pathlib import Path

from dotenv import dotenv_values

KEY_NAME = "ANTHROPIC_API_KEY"
KEY_PREFIX = "sk-ant-"
PLACEHOLDER = "sk-ant-..."  # giá trị mẫu trong .env.example

# .env nằm ở gốc repo: labs/01-claude-code-101/check_env.py -> lên 2 cấp
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def check() -> list[str]:
    """Trả về danh sách lỗi (rỗng = ổn). Không bao giờ đưa giá trị key vào thông báo."""
    if not ENV_PATH.exists():
        return [f"Không tìm thấy {ENV_PATH}. Copy .env.example thành .env rồi điền key."]

    key = dotenv_values(ENV_PATH).get(KEY_NAME)
    if key is None:
        return [f"{ENV_PATH.name} chưa có dòng {KEY_NAME}=..."]
    if not key.strip():
        return [f"{KEY_NAME} đang để trống."]
    if key.strip() == PLACEHOLDER:
        return [f"{KEY_NAME} vẫn là giá trị mẫu, chưa dán key thật."]
    if not key.startswith(KEY_PREFIX):
        return [f"{KEY_NAME} sai định dạng: phải bắt đầu bằng '{KEY_PREFIX}'."]
    return []


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, không in được tiếng Việt

    errors = check()
    for err in errors:
        print(f"[LỖI] {err}")
    if not errors:
        print(f"[OK] {KEY_NAME} có trong .env và đúng định dạng.")

    if os.environ.get(KEY_NAME):
        print(
            f"[CẢNH BÁO] Máy đang có biến môi trường hệ thống {KEY_NAME}. "
            "Claude Code có thể tính tiền vào API thay vì subscription — "
            "chỉ nên để key trong .env."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
