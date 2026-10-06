"""Kiểm tra độ dài file .md theo .claude/rules/memory-files.md.

Chạy: python .claude/skills/kiem-tra-memory/check_lengths.py
Exit code: 0 = mọi file trong giới hạn, 1 = có file vượt (dùng được cho hook/CI).
"""
import sys
from pathlib import Path

# Giữ đồng bộ với bảng trong .claude/rules/memory-files.md (lấy giới hạn chặt hơn: Ⓡ nếu có).
LIMITS = [
    ("CLAUDE.md", 100),
    (".claude/skills/*/SKILL.md", 500),
    (".claude/agents/*.md", 150),
    (".claude/rules/*.md", 150),
    ("memory/PROGRESS.md", 60),
    ("memory/NOTES.md", 200),
    ("memory/notes/*.md", 150),
    ("memory/ROADMAP.md", 200),
    ("memory/sessions/*.md", 150),
    ("labs/**/bai-giang-*.md", 250),
]
WARN_RATIO = 0.9  # >= 90% giới hạn thì cảnh báo "sắp vượt"
TOC_THRESHOLD = 100  # file > 100 dòng (trừ CLAUDE.md) phải có mục lục
TOC_SCAN_LINES = 25  # tìm chữ "mục lục" trong 25 dòng đầu

ROOT = Path(__file__).resolve().parents[3]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được emoji
    over, near, no_toc, ok = [], [], [], 0

    for pattern, limit in LIMITS:
        for path in sorted(ROOT.glob(pattern)):
            lines = read_lines(path)
            n = len(lines)
            rel = path.relative_to(ROOT).as_posix()
            if n >= limit:
                over.append(f"❌ {rel}: {n}/{limit} dòng")
            elif n >= limit * WARN_RATIO:
                near.append(f"⚠️  {rel}: {n}/{limit} dòng (≥{WARN_RATIO:.0%})")
            else:
                ok += 1
            head = "\n".join(lines[:TOC_SCAN_LINES]).lower()
            if rel != "CLAUDE.md" and n > TOC_THRESHOLD and "mục lục" not in head:
                no_toc.append(f"📑 {rel}: {n} dòng nhưng không có 'Mục lục' ở đầu")

    for line in over + near + no_toc:
        print(line)
    print(f"\nTổng: {ok} OK · {len(near)} sắp vượt · {len(over)} vượt · {len(no_toc)} thiếu mục lục")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
