# ROADMAP — Claude cho AI Engineer (ứng dụng)

Tick `[x]` khi đã học + làm lab. Mỗi giai đoạn nên có ít nhất 1 lab trong `labs/`.

## Nguồn học chính: Anthropic Academy (https://anthropic.skilljar.com/)

Quyết định 2026-09-30: học **khóa chọn lọc** theo thứ tự dưới đây, xen kẽ lab trong repo.
Khóa là "input", lab trong `labs/` là "output" — học xong mỗi khóa phải có ít nhất 1 lab tự làm.

| # | Khóa | Giai đoạn | Cần gì |
|---|---|---|---|
| 1 | [x] Claude Code 101 (xong 2026-10-06) | 1 | Subscription |
| 2 | [ ] Claude Code in Action | 1 | Subscription |
| 3 | [ ] Introduction to agent skills | 1 | Subscription |
| 4 | [ ] Introduction to subagents | 1 | Subscription |
| 5 | [ ] AI Fluency for Builders *(học nhanh, lấy tư duy)* | 2 | — |
| 6 | [ ] Building with the Claude API **(khóa lõi, dài nhất)** | 2–7 | API credits |
| 7 | [ ] Introduction to Model Context Protocol | 8 | API credits |
| 8 | [ ] Model Context Protocol: Advanced Topics | 8 | API credits |

- Tùy chọn: Claude Platform 101 (tổng quan nền tảng), AI Capabilities and Limitations.
- Bỏ qua: Claude 101, Cowork, AI Fluency cho educators/students/nonprofits/small business/K-12/creative,
  Teaching AI Fluency, Enterprise, Bedrock/Google Cloud (chỉ học nếu công ty dùng cloud đó).
- Tự bổ sung (khóa học không phủ đủ): Claude Agent SDK (docs), bài "Building effective agents",
  repo `anthropics/claude-cookbooks`, evals + RAG làm bằng dự án thật, Capstone.

## Giai đoạn 0 — Thiết lập
- [x] Tạo repo học tập + hệ thống memory đồng bộ qua git
- [x] Tạo subagent `ai-mentor` và skill `/hoc-tiep`, `/save-progress`
- [ ] Push lên GitHub, clone ở nhà, kiểm tra `/hoc-tiep` hoạt động
- [x] Chọn ngôn ngữ chính: Python
- [x] Môi trường Python (máy công ty: Python 3.12.10, anthropic 1.9.0): `.venv` + `requirements.txt` (`anthropic`, `python-dotenv`)
- [ ] Lấy API key tại console.anthropic.com, lưu vào `.env` (không commit)

## Giai đoạn 1 — Dùng Claude Code thành thạo (công cụ hằng ngày)
- [x] CLAUDE.md: project vs user (`~/.claude/CLAUDE.md`), cách viết hiệu quả
- [ ] Permission modes, `/config`, `/model`, `/clear`, `/compact`, Plan mode
- [x] Slash commands & **Skills** (`.claude/skills/*/SKILL.md`)
- [ ] **Subagents** (`.claude/agents/*.md`) — khi nào nên tách agent
- [x] **Hooks** (settings.json) — tự động hoá trước/sau tool call
- [ ] **MCP servers** trong Claude Code (`claude mcp add ...`)
- [ ] Workflow thực tế: đọc codebase lạ, refactor, viết test, review PR

## Giai đoạn 2 — Prompt Engineering nền tảng
- [ ] System prompt vs user prompt, vai trò, context
- [ ] Cấu trúc prompt rõ ràng (XML tags, ví dụ few-shot, chỉ dẫn định dạng output)
- [ ] Chain-of-thought / extended thinking — khi nào nên bật
- [ ] Prompt chaining: chia bài toán lớn thành nhiều bước
- [ ] Giảm hallucination: grounding, trích dẫn, cho phép nói "không biết"

## Giai đoạn 3 — Claude API (Messages API) cơ bản
- [ ] SDK Python `anthropic`, gọi Messages API đầu tiên
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
