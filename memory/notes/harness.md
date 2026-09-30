# Harness (agent harness)

- **Harness = toàn bộ code bao quanh model để biến model thành agent.** Model chỉ là hàm
  `text vào → text ra`, không tự đọc file hay chạy lệnh được. Nó chỉ *nói* "tôi muốn gọi tool X với
  input Y", còn harness mới *thực sự làm*.
- Nghĩa gốc: bộ yên cương của ngựa. Ngựa (model) khỏe nhưng không tự kéo xe đúng hướng; yên cương
  (harness) nối sức ngựa vào xe và cho người cầm cương điều khiển.
- Ẩn dụ đã chốt (2026-09-30): **Model = não · Tools = tay chân · Harness = cơ thể + hệ thần kinh**
  (dẫn truyền lệnh/kết quả, chọn thứ não được thấy, phản xạ an toàn).
  ⚠️ Hiểu lầm ban đầu của mình: "harness = tools". Sai, vì tools chỉ là một phần của harness. Bỏ hết
  tools đi thì vòng lặp, context, session, permission vẫn còn, và đó vẫn là harness.
- Harness lo 6 việc: (1) vòng lặp agent, (2) định nghĩa + thực thi tools, (3) quản lý context
  (system prompt, nạp CLAUDE.md, compact), (4) permissions/an toàn, (5) sessions/memory, (6) giao diện.
- Cùng một model đặt trong harness khác nhau (claude.ai, Claude Code, app của mình) sẽ hành xử khác nhau.
- Claude Code = một harness. **Claude Agent SDK** = harness của Claude Code đóng gói thành thư viện.
  Công việc của AI Engineer ứng dụng phần lớn là **thiết kế harness**, không phải train model.
- Từ gần nghĩa: *scaffolding*, *orchestration layer*. Phân biệt với *test harness* (code bao quanh
  để chạy test), cùng ý "khung bao quanh để vận hành một thứ".
