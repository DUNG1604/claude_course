# ROADMAP — Claude cho AI Engineer (ứng dụng)

Tick `[x]` khi đã học + làm lab. Mỗi giai đoạn nên có ít nhất 1 lab trong `labs/`.

## Giai đoạn 0 — Thiết lập
- [x] Tạo repo học tập + hệ thống memory đồng bộ qua git
- [x] Tạo subagent `ai-mentor` và skill `/resume`, `/save-progress`
- [ ] Push lên GitHub, clone ở nhà, kiểm tra `/resume` hoạt động
- [ ] Lấy API key tại console.anthropic.com, lưu vào `.env` (không commit)

## Giai đoạn 1 — Dùng Claude Code thành thạo (công cụ hằng ngày)
- [ ] CLAUDE.md: project vs user (`~/.claude/CLAUDE.md`), cách viết hiệu quả
- [ ] Permission modes, `/config`, `/model`, `/clear`, `/compact`, Plan mode
- [ ] Slash commands & **Skills** (`.claude/skills/*/SKILL.md`)
- [ ] **Subagents** (`.claude/agents/*.md`) — khi nào nên tách agent
- [ ] **Hooks** (settings.json) — tự động hoá trước/sau tool call
- [ ] **MCP servers** trong Claude Code (`claude mcp add ...`)
- [ ] Workflow thực tế: đọc codebase lạ, refactor, viết test, review PR

## Giai đoạn 2 — Prompt Engineering nền tảng
- [ ] System prompt vs user prompt, vai trò, context
- [ ] Cấu trúc prompt rõ ràng (XML tags, ví dụ few-shot, chỉ dẫn định dạng output)
- [ ] Chain-of-thought / extended thinking — khi nào nên bật
- [ ] Prompt chaining: chia bài toán lớn thành nhiều bước
- [ ] Giảm hallucination: grounding, trích dẫn, cho phép nói "không biết"

## Giai đoạn 3 — Claude API (Messages API) cơ bản
- [ ] SDK (Python `anthropic` / TS `@anthropic-ai/sdk`), gọi Messages API đầu tiên
- [ ] Model family & chọn model theo chi phí/tốc độ/chất lượng
- [ ] Tham số: `max_tokens`, `temperature`, `stop_sequences`, `system`
- [ ] Hội thoại nhiều lượt (quản lý `messages` history)
- [ ] Streaming
- [ ] Vision (ảnh) & PDF input
- [ ] Đếm token, ước tính chi phí, xử lý lỗi / rate limit / retry

## Giai đoạn 4 — Tool use (Function calling)
- [ ] Định nghĩa tool bằng JSON Schema
- [ ] Vòng lặp tool-use thủ công (tool_use → tool_result)
- [ ] Tool Runner của SDK
- [ ] Structured output (ép JSON theo schema)
- [ ] Server tools: web search, code execution
- [ ] Lab: chatbot gọi API thật (thời tiết/DB nội bộ...)

## Giai đoạn 5 — Tối ưu production
- [ ] Prompt caching (giảm chi phí & độ trễ)
- [ ] Batch API
- [ ] Context window management: tóm tắt, cắt lịch sử, compaction
- [ ] Observability: log prompt/response, đo latency, cost
- [ ] Guardrails & an toàn: prompt injection, kiểm soát đầu vào/đầu ra

## Giai đoạn 6 — RAG & Knowledge
- [ ] Embeddings & vector DB (khái niệm + 1 công cụ cụ thể)
- [ ] Chunking, retrieval, reranking
- [ ] Contextual retrieval
- [ ] Citations
- [ ] Lab: hỏi đáp trên tài liệu nội bộ

## Giai đoạn 7 — Evals (đánh giá chất lượng)
- [ ] Tạo bộ test case, tiêu chí thành công
- [ ] Code-based grading vs LLM-as-judge
- [ ] So sánh prompt/model bằng số liệu, không bằng cảm tính

## Giai đoạn 8 — Agents
- [ ] Workflow vs Agent — các pattern (routing, parallelization, orchestrator-workers, evaluator-optimizer)
- [ ] **MCP**: tự viết 1 MCP server (tools/resources/prompts)
- [ ] **Claude Agent SDK**: xây agent tùy biến
- [ ] Managed Agents (agent chạy trên hạ tầng Anthropic)
- [ ] Multi-agent, subagents, memory dài hạn cho agent
- [ ] Computer use (tìm hiểu)

## Giai đoạn 9 — Capstone
- [ ] Xây 1 sản phẩm hoàn chỉnh: agent + tools + RAG + evals + deploy
- [ ] Viết blog/README tổng kết để làm portfolio
