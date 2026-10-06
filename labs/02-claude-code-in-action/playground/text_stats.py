"""Thống kê văn bản đơn giản: đếm từ, đếm câu, tìm từ dài nhất."""

import re

# Từ = chuỗi chữ/số liền nhau (hỗ trợ tiếng Việt có dấu), cho phép dấu nháy/gạch nối ở giữa: "don't", "e-mail"
WORD_RE = re.compile(r"[^\W_]+(?:['\-][^\W_]+)*")
# Câu kết thúc bằng . ! ? (một hoặc nhiều dấu, ví dụ "..." hay "?!")
SENTENCE_END_RE = re.compile(r"[.!?]+")


def words(text: str) -> list[str]:
    """Tách văn bản thành danh sách từ."""
    return WORD_RE.findall(text)


def count_words(text: str) -> int:
    """Đếm số từ trong văn bản."""
    return len(words(text))


def count_sentences(text: str) -> int:
    """Đếm số câu. Đoạn cuối không có dấu kết câu vẫn tính là 1 câu nếu có chữ."""
    parts = SENTENCE_END_RE.split(text)
    return sum(1 for part in parts if words(part))


def longest_word(text: str) -> str | None:
    """Trả về từ dài nhất (từ xuất hiện trước thắng khi bằng độ dài); None nếu không có từ."""
    ws = words(text)
    return max(ws, key=len) if ws else None
