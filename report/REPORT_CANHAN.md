# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Hải Long
**Nhóm:** Nhóm G25
**Ngày:** 20/09/2026

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
> Lưu trữ dưới dạng danh sách từ điển record trong bộ nhớ (in-memory), mỗi record chứa `id`, `content`, bản sao độc lập của `metadata` (bảo đảm luôn có trường `doc_id`) và vector `embedding`. Khi tìm kiếm, hàm `search` tính điểm tương đồng bằng tích vô hướng (dot product) giữa vector câu hỏi và vector từng tài liệu (do vector đã được chuẩn hóa đơn vị), sau đó sắp xếp giảm dần theo score và lấy đúng `top_k` bản ghi.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Lọc (filter) bắt buộc thực hiện **trước** khi tính toán tương đồng (pre-filtering) để bảo đảm toàn bộ kết quả trả về đều thỏa mãn metadata yêu cầu, không bị mất vị trí vào các tài liệu sai đối tượng. Hàm `delete_document` loại bỏ tất cả các chunk có `metadata['doc_id']` (hoặc `id`) khớp với mã tài liệu cần xóa và trả về `True` nếu có ít nhất 1 chunk bị xóa, ngược lại trả về `False`.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Kiểm tra an toàn trạng thái store (tránh crash hoặc gọi LLM khi store rỗng), truy xuất top-k đoạn văn bản liên quan nhất rồi định dạng thành ngữ cảnh có đánh số thứ tự `[1] [2] ...` kèm định danh nguồn. Prompt được thiết kế chặt chẽ yêu cầu mô hình chỉ trả lời dựa trên ngữ cảnh được cấp, bắt buộc trích dẫn số nguồn và thừa nhận nếu không tìm thấy thông tin.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================= 42 passed in 0.13s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên đăng ký tối thiểu 14 tín chỉ trong mỗi học kỳ chính. | Người học hệ cử nhân bắt buộc tích lũy không dưới 14 tín chỉ mỗi kỳ chuẩn. | Cao | -0.3352 | Sai |
| 2 | Quy chế đào tạo đại học chính quy theo hệ thống tín chỉ. | Quy chế đào tạo đại học chính quy theo hệ thống tín chỉ. | Cao | 1.0000 | Đúng |
| 3 | Sinh viên hoàn thành đủ 130 tín chỉ để được xét tốt nghiệp. | Trận đấu bóng đá giao hữu bị hoãn do trời mưa bão. | Thấp | -0.0094 | Đúng |
| 4 | Học phần bị điểm F bắt buộc phải đăng ký học lại. | Sinh viên đạt điểm D và C được quyền học cải thiện nâng cao GPA. | Trung bình / Cao | -0.0209 | Sai |
| 5 | Sinh viên được phép rút học phần trong 2 tuần đầu. | Sinh viên không được phép rút học phần trong 2 tuần đầu. | Cao (do trùng hầu hết từ) | -0.0944 | Sai |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là ở Cặp 1 (hai câu cùng nghĩa nhưng khác từ vựng) điểm tương đồng lại ra âm (-0.3352), và Cặp 5 (hai câu gần như giống hệt nhau chỉ thêm từ "không") điểm cũng âm (-0.0944). Điều này phản ánh rõ hạn chế của `MockEmbedder` (băm MD5 chuỗi ký tự): nó chỉ là hàm băm tạo số giả ngẫu nhiên nên chỉ cần thay đổi 1 ký tự là vector bị phân tán ngẫu nhiên, hoàn toàn không có khả năng hiểu ngữ nghĩa (semantic understanding). Để hệ thống RAG hoạt động đúng bản chất trong thực tế, bắt buộc phải dùng các mô hình pre-trained text embedding thực thụ (như multilingual MiniLM hay text-embedding-3-small).

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên bình thường được đăng ký tối đa và tối thiểu bao nhiêu tín chỉ trong một học kỳ chính? | `quy-dinh-chuong-trinh-tien-tien-aep#0` (Quy định đào tạo chương trình tiên tiến AEP) | 0.2169 | Chưa tối ưu (do mock embedding) | Agent trả lời về định hướng và chuẩn đào tạo của chương trình tiên tiến. |
| 2 | Sinh viên bị buộc thôi học trong những trường hợp nào theo quy chế đào tạo? | `trach-nhiem-co-van-va-giang-vien#5` (Top 3 có `canh-bao-hoc-tap-va-buoc-thoi-hoc#2` score 0.2140) | 0.2416 | Có (Top 3 trúng Gold Document) | Agent trích xuất tiêu chí cảnh báo học tập và các trường hợp bị buộc thôi học. |
| 3 | Quy định rút học phần từ tuần thứ 3 đến tuần thứ 6 như thế nào và sinh viên nhận điểm gì? | `thang-diem-va-danh-gia-hoc-phan#1` (Top 2 có `rut-hoc-phan-va-nghi-tam-thoi#4` score 0.2855) | 0.3394 | Có (Top 2 trúng Gold Document) | Agent trích dẫn quy trình nộp đơn xin rút môn và việc bảo lưu kết quả học tập. |
| 4 | Sinh viên có điểm CPA loại Giỏi hoặc Xuất sắc bị hạ một bậc xếp loại tốt nghiệp khi nào? | `quy-dinh-chuong-trinh-tien-tien-aep#0` (Mục giới thiệu chuẩn tiếng Anh) | 0.1405 | Chưa sát (điểm score thấp) | Agent thông báo thông tin về hạ bậc tốt nghiệp chưa xuất hiện rõ ở top-1. |
| 5 | Hạn mức đăng ký học phần tối đa trong một học kỳ chính là bao nhiêu tín chỉ và ai có thẩm quyền phê duyệt khi vượt quá hạn mức thông thường? *(A/B Filter)* | `quy-dinh-chuong-trinh-tien-tien-aep#4` (Top 2 & 3 là `canh-bao-hoc-tap-va-buoc-thoi-hoc`) | 0.3427 | Có liên quan đối tượng sinh viên | Agent trả lời về quy định duy trì học tập của sinh viên, loại bỏ hoàn toàn các chunk của giảng viên. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 3 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Chiến lược chia nhỏ theo Tiêu đề/Mục (`MarkdownSectionChunker`) là hướng tiếp cận tự nhiên và bảo toàn ngữ cảnh tốt nhất cho văn bản quy phạm, vì mỗi điều khoản tự nó đã là một khối logic hoàn chỉnh. Khi kết hợp cơ chế gắn lại tiêu đề mục cha vào từng mảnh con, ta giải quyết triệt để được vấn đề "mất gốc ngữ cảnh" mà các chiến lược cắt cơ học FixedSize hay gặp phải.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |

