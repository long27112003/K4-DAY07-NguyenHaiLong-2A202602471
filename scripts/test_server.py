import json
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def test_api():
    print("=== KIỂM THỬ STRATIFY AI BACKEND SERVER ===")

    # 1. Test /api/stats
    res = urllib.request.urlopen("http://localhost:8000/api/stats")
    stats = json.loads(res.read().decode("utf-8"))
    print(f"[1] /api/stats: OK ({stats['status']}) - Chunks: {stats['total_chunks']}, Docs: {stats['documents_count']}")

    # 2. Test /api/documents
    res = urllib.request.urlopen("http://localhost:8000/api/documents")
    docs = json.loads(res.read().decode("utf-8"))
    print(f"[2] /api/documents: OK - Tổng cộng {docs['total_documents']} tài liệu")
    for d in docs["documents"]:
        print(f"    - {d['id']}: audience={d['audience']}, chunks={d['chunks_count']}")

    # 3. Test /api/chat with 5 benchmark questions
    test_cases = [
        ("Tín chỉ tối đa và tối thiểu trong học kỳ chính?", "student"),
        ("Điều kiện sinh viên bị buộc thôi học?", "student"),
        ("Quy định về rút học phần và điểm W?", "student"),
        ("Sinh viên tốt nghiệp loại Giỏi/Xuất sắc bị hạ bậc khi nào?", "student"),
        ("Thẩm quyền của Cố vấn học tập phê duyệt đăng ký vượt 25 tín chỉ?", "faculty"),
    ]

    print("\n[3] /api/chat: Kiểm thử các câu hỏi trích xuất")
    for q, aud in test_cases:
        req_data = json.dumps({"question": q, "audience": aud, "top_k": 3}).encode("utf-8")
        req = urllib.request.Request("http://localhost:8000/api/chat", data=req_data, headers={"Content-Type": "application/json"})
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        print(f"\n>> Câu hỏi: '{q}' [audience={aud}]")
        print(f"   Độ trễ: {data['latency_ms']} ms | Top Score: {data['top_score']:.3f} | Chunks: {len(data['chunks'])}")
        print(f"   Trả lời: {data['answer'][:110]}...")

    # 4. Test static assets
    for asset in ["/index.html", "/style.css", "/app.js"]:
        res = urllib.request.urlopen(f"http://localhost:8000{asset}")
        content = res.read()
        print(f"[4] Tải asset {asset}: OK (status={res.status}, size={len(content)} bytes)")

    print("\n=== TẤT CẢ CÁC BƯỚC KIỂM THỬ THÀNH CÔNG 100%! ===")


if __name__ == "__main__":
    test_api()
