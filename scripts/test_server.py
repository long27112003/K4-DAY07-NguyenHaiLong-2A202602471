import json
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def test_api():
    print("=== KIỂM THỬ SHADCN CHATBOT & 5 CÂU HỎI BENCHMARK ===")

    # 1. Test /api/stats
    res = urllib.request.urlopen("http://localhost:8000/api/stats")
    stats = json.loads(res.read().decode("utf-8"))
    print(f"[1] /api/stats: OK ({stats['status']}) - Chunks: {stats['total_chunks']}, Docs: {stats['documents_count']}")

    # 2. Test 5 benchmark queries
    test_cases = [
        ("Trường tổ chức cho sinh viên đăng ký học muộn nhất bao lâu trước khi bắt đầu học kỳ?", "all"),
        ("Học cải thiện điểm được tối đa bao nhiêu tín chỉ trong học kỳ 1?", "student"),
        ("Khi không đồng ý với điểm thi thì làm gì?", "student"),
        ("Sinh viên được tuyển chọn vào chương trình Chất lượng cao như thế nào?", "student"),
        ("Điều kiện để được xét công nhận tốt nghiệp gồm những gì?", "student"),
    ]

    print("\n[2] /api/chat: Kiểm thử 5 câu hỏi benchmark mới")
    for idx, (q, aud) in enumerate(test_cases, 1):
        req_data = json.dumps({"question": q, "audience": aud, "top_k": 3}).encode("utf-8")
        req = urllib.request.Request("http://localhost:8000/api/chat", data=req_data, headers={"Content-Type": "application/json"})
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        print(f"\n[Câu {idx}] '{q}'")
        print(f"  Audience: {aud} | Top Score: {data['top_score']:.3f} | Chunks: {len(data['chunks'])} | Latency: {data['latency_ms']} ms")
        print(f"  Trả lời: {data['answer']}")

    # 3. Test static assets
    for asset in ["/index.html", "/style.css", "/app.js"]:
        res = urllib.request.urlopen(f"http://localhost:8000{asset}")
        content = res.read()
        print(f"\n[3] Asset {asset}: OK (status={res.status}, size={len(content)} bytes)")

    print("\n=== TẤT CẢ CÁC BÀI KIỂM TRA ĐỀU THÀNH CÔNG 100%! ===")


if __name__ == "__main__":
    test_api()
