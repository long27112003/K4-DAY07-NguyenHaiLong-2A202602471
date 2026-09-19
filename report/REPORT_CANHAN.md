# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao (tiến gần về 1.0) nghĩa là góc giữa hai vector embedding của hai đoạn văn bản rất nhỏ. Điều này biểu thị hai đoạn văn có mức độ tương đồng rất lớn về mặt ý nghĩa/ngữ nghĩa trong không gian vector biểu diễn, bất kể từ ngữ bề mặt hoặc độ dài câu có thể khác biệt.

**Ví dụ có độ tương tự CAO:**
- Câu A: Sinh viên bắt buộc phải tích lũy tối thiểu 14 tín chỉ trong mỗi học kỳ chính theo quy chế đào tạo.
- Câu B: Mỗi kỳ học tiêu chuẩn, người học hệ đại học chính quy không được đăng ký dưới 14 tín chỉ.
- Tại sao tương đồng: Hai câu sử dụng các từ ngữ khác nhau ("sinh viên" vs "người học", "tích lũy tối thiểu" vs "không được đăng ký dưới", "học kỳ chính" vs "kỳ học tiêu chuẩn") nhưng truyền tải cùng một quy tắc học vụ và cùng một bản chất ngữ nghĩa.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Sinh viên hoàn thành đủ 130 tín chỉ và đạt chuẩn đầu ra ngoại ngữ sẽ được xét công nhận tốt nghiệp.
- Câu B: Trận thi đấu bóng đá giao hữu giữa hai viện đào tạo chiều nay bị hoãn lại do thời tiết mưa lớn.
- Tại sao khác: Hai câu nói về hai chủ đề hoàn toàn tách biệt, không có chung bất kỳ trường nghĩa, từ vựng hay ngữ cảnh nào.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Khoảng cách Euclid bị phụ thuộc trực tiếp vào độ dài (magnitude) của vector, khiến hai văn bản có cùng ý nghĩa nhưng khác biệt về độ dài (ví dụ một câu ngắn và một đoạn văn dài diễn giải câu đó) bị đẩy ra xa nhau. Ngược lại, Cosine similarity chỉ đo góc định hướng giữa hai vector, giúp đo lường chính xác độ tương đồng ngữ nghĩa mà không bị ảnh hưởng bởi độ dài của văn bản.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* Áp dụng công thức: `số lượng chunk = ceil((độ_dài_tài_liệu - độ_chồng_chéo) / (kích_thước_chunk - độ_chồng_chéo))`
> `= ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = ceil(22.11) = 23`
> *Đáp án:* **23 chunks**

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi overlap tăng lên 100: `ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = 25 chunks` (số chunk tăng từ 23 lên 25). Người ta muốn tăng độ chồng chéo để duy trì tính liên tục và bảo toàn ngữ cảnh giữa các chunk liền kề, ngăn chặn nguy cơ một câu văn, con số hay thực thể quan trọng bị cắt đôi ngay ranh giới phân mảnh, giúp bộ truy xuất (retriever) tìm kiếm thông tin trọn vẹn hơn.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Dùng regex lookbehind `r"(?<=[.!?])(?:\s+|\n+)"` để tách văn bản tại ranh giới câu mà vẫn giữ nguyên được dấu câu gốc ở cuối câu. Sau đó gom từng nhóm câu theo `max_sentences_per_chunk`, loại bỏ khoảng trắng thừa và xử lý an toàn trường hợp chuỗi rỗng. Edge case còn tồn tại: các từ viết tắt có dấu chấm (như `TS.`, `v.v.`) hoặc số thập phân (`3.5`) có thể bị chia nhầm thành ranh giới câu.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Triển khai thuật toán đệ quy theo danh sách phân cách ưu tiên từ cấu trúc lớn đến nhỏ `["\n\n", "\n", ". ", " ", ""]`. Nếu mảnh văn bản lớn hơn `chunk_size`, thuật toán gọi đệ quy với separator cấp kế tiếp; sau đó tiến hành gom các mảnh nhỏ liền kề lại cho tới sát ngưỡng `chunk_size` để không sinh ra chunk vụn. Base case dừng đệ quy khi chuỗi rỗng, chuỗi `<= chunk_size`, hoặc khi danh sách separator rỗng thì cắt lát theo ký tự.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?*

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?*

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?*

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
# Dán kết quả (output) của: pytest tests/ -v
```

**Số lượng bài test vượt qua (pass):** __ / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | cao / thấp | | |
| 2 | | | cao / thấp | | |
| 3 | | | cao / thấp | | |
| 4 | | | cao / thấp | | |
| 5 | | | cao / thấp | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:*

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** __ / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | / 5 |
| Hướng tiếp cận của tôi (My Approach) | / 10 |
| Hoàn thiện code (Core Implementation — tests) | / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | / 5 |
| Kết quả truy xuất của tôi (Competition Results) | / 10 |
| **Tổng phần cá nhân** | **/ 60** |
