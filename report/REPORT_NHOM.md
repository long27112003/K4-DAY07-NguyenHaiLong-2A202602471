# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên từng thành viên]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Quy chế đào tạo đại học chính quy — Trường Đại học Kinh tế Quốc dân (NEU)

**Tại sao nhóm chọn chủ đề này?**
> Nhóm chọn chủ đề "Quy chế đào tạo NEU" vì đây là văn bản học vụ cốt lõi, bắt buộc và có tính pháp lý cao nhất đối với sinh viên và giảng viên, đáp ứng chuẩn yêu cầu K4-L3A. Văn bản quy định chi tiết về hạn mức đăng ký tín chỉ, cơ cấu tính điểm GPA/CPA, tiêu chí cảnh báo học tập, điều kiện tốt nghiệp và phân định thẩm quyền rõ ràng giữa Sinh viên (`student`) và Cố vấn học tập / Giảng viên (`faculty`), tạo điều kiện tối ưu để thử nghiệm retrieval và metadata filter.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Quy chế về khối lượng học tập và đăng ký học phần NEU | https://daotao.neu.edu.vn/Resources/Docs/SubDomain/daotao/NewFolder/Q%C4%90%20368_QUY%20CH%E1%BA%BE%20%C4%90%C3%80O%20T%E1%BA%A0O%20%C4%90%E1%BA%A0I%20H%E1%BB%8CC%202024-news.pdf | 2026-09-19 / 368/QD-DHKTQD-2024 | 1,780 | audience=student, department=academic-affairs, category=academic-regulations |
| 2 | Quy chế về đánh giá học phần và thang điểm đào tạo NEU | https://daotao.neu.edu.vn/Resources/Docs/SubDomain/daotao/NewFolder/Q%C4%90%20368_QUY%20CH%E1%BA%BE%20%C4%90%C3%80O%20T%E1%BA%A0O%20%C4%90%E1%BA%A0I%20H%E1%BB%8CC%202024-news.pdf | 2026-09-19 / 368/QD-DHKTQD-2024 | 2,220 | audience=student, department=academic-affairs, category=academic-regulations |
| 3 | Quy chế về cảnh báo học tập và buộc thôi học NEU | https://daotao.neu.edu.vn/Resources/Docs/SubDomain/daotao/Xulyhocvu/1155_Quyche-Daotao-Daihoc-K63%20tr%E1%BB%9F%20%C4%91i.pdf | 2026-09-19 / 1155/QD-DHKTQD | 2,060 | audience=student, department=academic-affairs, category=academic-regulations |
| 4 | Quy chế về rút bớt học phần và nghỉ học tạm thời NEU | https://daotao.neu.edu.vn/vi/quy-dinh-cua-truong/quy-dinh-dao-tao-dai-hoc-he-chinh-quy-theo-he-thong-tin-chi-tai-truong-dai-hoc-kinh-te-quoc-dan-2 | 2026-09-19 / 368/QD-DHKTQD-2024 | 1,980 | audience=student, department=academic-affairs, category=academic-regulations |
| 5 | Quy chế về điều kiện xét và công nhận tốt nghiệp NEU | https://daotao.neu.edu.vn/Resources/Docs/SubDomain/daotao/NewFolder/Q%C4%90%20368_QUY%20CH%E1%BA%BE%20%C4%90%C3%80O%20T%E1%BA%A0O%20%C4%90%E1%BA%A0I%20H%E1%BB%8CC%202024-news.pdf | 2026-09-19 / 368/QD-DHKTQD-2024 | 2,370 | audience=student, department=academic-affairs, category=graduation |
| 6 | Quy định về đào tạo theo chương trình tiên tiến AEP NEU | https://aep.neu.edu.vn/wp-content/uploads/2022/07/Quy-dinh-ve-dao-tao-theo-chuong-trinh-tien-tien.pdf | 2026-09-19 / AEP-2022 | 1,650 | audience=student, department=advanced-education-program, category=specialized-program |
| 7 | Quy chế về trách nhiệm của Cố vấn học tập và Giảng viên NEU | https://daotao.neu.edu.vn/Resources/Docs/SubDomain/daotao/NewFolder/Q%C4%90%20368_QUY%20CH%E1%BA%BE%20%C4%90%C3%80O%20T%E1%BA%A0O%20%C4%90%E1%BA%A0I%20H%E1%BB%8CC%202024-news.pdf | 2026-09-19 / 368/QD-DHKTQD-2024 | 1,890 | audience=faculty, department=academic-affairs, category=faculty-guidance |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | str | `khoi-luong-hoc-tap-va-dang-ky` | Định danh tài liệu duy nhất, liên kết các chunk về tài liệu gốc và hỗ trợ hàm `delete_document`. |
| `title` | str | `Quy chế về khối lượng học tập và đăng ký học phần NEU` | Hiển thị trích dẫn nguồn văn bản rõ ràng khi agent sinh câu trả lời. |
| `audience` | str | `student`, `faculty` | **Trọng yếu cho L3A:** Lọc đúng đối tượng qua `search_with_filter`, phân biệt quyền hạn sinh viên và thẩm quyền duyệt của cố vấn/giảng viên. |
| `department` | str | `academic-affairs`, `advanced-education-program` | Phân nhóm phòng ban/đơn vị quản lý (Phòng Đào tạo, Viện Đào tạo Tiên tiến AEP). |
| `category` | str | `academic-regulations`, `graduation`, `faculty-guidance` | Phân loại lĩnh vực quy chế đào tạo, giúp lọc sâu theo phân hệ nội dung. |
| `source_url` | str | `https://daotao.neu.edu.vn/...` | Cung cấp xuất xứ (provenance) chính thức từ QĐ 368, QĐ 1155 hoặc cổng NEU. |
| `retrieved_at` | str | `2026-09-19` | Kiểm soát tính mới và thời điểm thu thập dữ liệu. |
| `document_version` | str | `368/QD-DHKTQD-2024`, `1155/QD-DHKTQD` | Số hiệu quyết định pháp lý ban hành quy chế. |
| `language` | str | `vi` | Định danh ngôn ngữ tiếng Việt của tài liệu. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — [Tên]**
- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**
```python
# Dán mã nguồn (implementation) vào đây
```

**Thành viên 2 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

**Thành viên 3 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| | | | | |
| | | | | |
| | | | | |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |
