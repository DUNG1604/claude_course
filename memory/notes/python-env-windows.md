# Môi trường Python (Windows)

- Cài: `winget install --id Python.Python.3.12 --scope user` → mở terminal **mới** để nhận PATH.
- Gotcha: `python` báo "not found… Microsoft Store" = mới chỉ có alias của Windows, chưa cài thật.
- Mỗi lần làm: `.\.venv\Scripts\Activate.ps1` (lỗi policy → `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`).
- `.venv` và `.env` không commit; máy khác tự tạo lại từ `requirements.txt` và `.env.example`.
