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

Chạy `ChunkingStrategyComparator().compare()` trên 3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `khoi-luong-hoc-tap-va-dang-ky.md` | FixedSizeChunker (`fixed_size`) | 5 | 266.60 | Kém — ngắt cơ học theo ký tự cố định, dễ cắt đôi câu quy định. |
| `khoi-luong-hoc-tap-va-dang-ky.md` | SentenceChunker (`by_sentences`) | 4 | 301.25 | Khá — giữ trọn cấu trúc ngữ pháp từng câu, ngữ nghĩa mạch lạc. |
| `khoi-luong-hoc-tap-va-dang-ky.md` | RecursiveChunker (`recursive`) | 5 | 241.00 | Tốt — ưu tiên ranh giới đoạn văn bản `\n\n` trước khi chia nhỏ. |
| `canh-bao-hoc-tap-va-buoc-thoi-hoc.md` | FixedSizeChunker (`fixed_size`) | 5 | 257.00 | Kém — làm đứt gãy các tiêu chí ngưỡng điểm GPA/CPA. |
| `canh-bao-hoc-tap-va-buoc-thoi-hoc.md` | SentenceChunker (`by_sentences`) | 4 | 288.75 | Khá — bảo toàn được từng điều kiện cảnh báo học tập. |
| `canh-bao-hoc-tap-va-buoc-thoi-hoc.md` | RecursiveChunker (`recursive`) | 5 | 231.40 | Tốt — giữ được khối điều khoản và gom các mảnh nhỏ hợp lý. |
| `xet-va-cong-nhan-tot-nghiep.md` | FixedSizeChunker (`fixed_size`) | 5 | 265.40 | Trung bình — dễ chia cắt các gạch đầu dòng tiêu chuẩn tốt nghiệp. |
| `xet-va-cong-nhan-tot-nghiep.md` | SentenceChunker (`by_sentences`) | 3 | 401.33 | Tốt — chunk dài hơn nhưng gom trọn vẹn các điều kiện liên quan. |
| `xet-va-cong-nhan-tot-nghiep.md` | RecursiveChunker (`recursive`) | 6 | 199.83 | Tốt — các chunk gọn gàng, độ dài đồng đều. |

### Chiến lược của từng thành viên

**Thành viên 1 — Nguyễn Hải Long (Strategy Lead)**
- **Loại chiến lược:** Custom `MarkdownSectionChunker` (Chia nhỏ theo Tiêu đề/Mục của văn bản quy chế — Bắt buộc K4-L3A)
- **Mô tả & lý do chọn cho chủ đề này:** Văn bản quy chế đào tạo đại học được cơ cấu chặt chẽ theo các đề mục (`## 1. Khối lượng...`, `## 2. Tiêu chí...`), mỗi mục là một đơn vị ngữ nghĩa trọn vẹn. Thuật toán tách theo tiêu đề `#` và `##`, đồng thời nếu mục nào dài quá ngưỡng sẽ chia nhỏ đệ quy và gắn lại tiêu đề mục cha vào đầu mỗi chunk con để không bị mất ngữ cảnh (context-aware heading chunking).
- **Code snippet (nếu custom):**
```python
class MarkdownSectionChunker:
    def __init__(self, max_chunk_size: int = 500) -> None:
        self.max_chunk_size = max_chunk_size
        self._fallback_chunker = RecursiveChunker(chunk_size=max_chunk_size)

    def chunk(self, text: str) -> list[str]:
        raw_sections = re.split(r"(?=(?:\n|^)#{1,3}\s+)", text.strip())
        sections = [s.strip() for s in raw_sections if s.strip()]
        chunks = []
        for sec in sections:
            if len(sec) <= self.max_chunk_size:
                chunks.append(sec)
            else:
                first_line = sec.split("\n", 1)[0].strip()
                for sub in self._fallback_chunker.chunk(sec):
                    chunks.append(f"{first_line}\n{sub}" if not sub.startswith("#") else sub)
        return chunks
```

**Thành viên 2 — [Thành viên nhóm 2]**
- **Loại chiến lược:** `RecursiveChunker` (chunk_size=300)
- **Mô tả & lý do chọn:** Dùng chiến lược đệ quy chuẩn với độ ưu tiên tách đoạn `\n\n`, sau đó đến dòng `\n` và câu `. `, giúp phân tách văn bản tự nhiên theo cấu trúc đoạn mà không phụ thuộc định dạng markdown.

**Thành viên 3 — [Thành viên nhóm 3]**
- **Loại chiến lược:** `FixedSizeChunker` (chunk_size=300, overlap=50)
- **Mô tả & lý do chọn:** Chiến lược kích thước cố định có độ chồng lấn (overlap) 50 ký tự để làm đường cơ sở đối chứng, nhằm kiểm tra xem độ chồng lấn có giúp bù đắp sự thiếu hụt cấu trúc so với chia theo Heading hay không.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Nguyễn Hải Long | `MarkdownSectionChunker` (Heading) | 8/10 | Giữ trọn vẹn ngữ cảnh điều khoản, gắn kèm tiêu đề mục cha giúp agent hiểu chính xác phạm vi áp dụng. | Khó tối ưu nếu gặp văn bản thuần text không có tiêu đề markdown. |
| Thành viên 2 | `RecursiveChunker` | 7/10 | Linh hoạt với mọi định dạng văn bản, tránh sinh ra chunk vụn nhờ cơ chế gom mảnh. | Đôi khi cắt rời tiêu đề mục khỏi các điều khoản chi tiết bên dưới. |
| Thành viên 3 | `FixedSizeChunker` (overlap 50) | 5/10 | Dễ cài đặt, kích thước chunk rất đồng đều. | Cắt ngang câu và cụm số liệu (ví dụ cắt giữa mốc 14 và tín chỉ), gây nhiễu embedding. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Chiến lược **`MarkdownSectionChunker` (theo Heading/Section)** là tốt nhất cho chủ đề Quy chế đào tạo. Lý do là các quy định học vụ mang tính pháp lý cao, các điều kiện và con số ràng buộc lẫn nhau trong cùng một điều khoản; việc giữ trọn vẹn cả tiêu đề mục lẫn nội dung bên trong giúp vector embedding nắm bắt trọn vẹn ngữ nghĩa và hạn chế tối đa việc mất ngữ cảnh khi truy xuất.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Sinh viên bình thường được đăng ký tối đa và tối thiểu bao nhiêu tín chỉ trong một học kỳ chính? | Tối thiểu 14 tín chỉ (trừ học kỳ cuối khóa), tối đa 25 tín chỉ (đối với sinh viên có GPA >= 2.0). | `khoi-luong-hoc-tap-va-dang-ky#0` (Mục 1) |
| 2 | Sinh viên bị buộc thôi học trong những trường hợp nào theo quy chế đào tạo? | Bị 2 lần cảnh báo học tập liên tiếp; hoặc quá thời gian học tập tối đa 6 năm (12 học kỳ chính đối với khóa 4 năm). | `canh-bao-hoc-tap-va-buoc-thoi-hoc#2` (Mục 2) |
| 3 | Quy định rút học phần từ tuần thứ 3 đến tuần thứ 6 như thế nào và sinh viên nhận điểm gì? | Sinh viên nộp đơn có xác nhận của Cố vấn học tập, số tín chỉ còn lại không dưới 14 TC, nhận điểm W (không tính vào GPA/CPA) và không được hoàn trả học phí. | `rut-hoc-phan-va-nghi-tam-thoi#1` (Mục 1) |
| 4 | Sinh viên có điểm CPA loại Giỏi hoặc Xuất sắc bị hạ một bậc xếp loại tốt nghiệp khi nào? | Khi khối lượng các học phần phải học lại do bị điểm F vượt quá 5% tổng số tín chỉ toàn khóa, hoặc bị kỷ luật từ mức khiển trách trở lên. | `xet-va-cong-nhan-tot-nghiep#2` (Mục 2) |
| 5 | Hạn mức đăng ký học phần tối đa trong một học kỳ chính là bao nhiêu tín chỉ và ai có thẩm quyền phê duyệt khi vượt quá hạn mức thông thường? *(Câu hỏi cần filter `audience: student`)* | Đối với sinh viên, hạn mức tối đa thông thường là 25 tín chỉ; trường hợp muốn đăng ký vượt (tối đa 28 tín chỉ) phải do Cố vấn học tập phê duyệt cho sinh viên có CPA >= 3.20. | `khoi-luong-hoc-tap-va-dang-ky#0` & `trach-nhiem-co-van-va-giang-vien#1` |

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
