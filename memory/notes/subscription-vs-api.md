# Subscription vs API — 2 hệ thống tính tiền riêng

- **Subscription (Pro/Max)**: dùng claude.ai + **Claude Code**. Không kèm API credits.
- **API (console.anthropic.com)**: trả theo token, nạp credits riêng. Cần cho code Python gọi
  `anthropic` SDK (mọi lab từ Giai đoạn 3).
- Gotcha: nếu `ANTHROPIC_API_KEY` có trong biến môi trường hệ thống, Claude Code có thể dùng key
  đó (tính tiền API) thay vì subscription → chỉ để key trong `.env` của lab.
- Tiết kiệm khi học: dùng model Haiku cho lab, đặt `max_tokens` nhỏ, bật spend limit trong Console.
