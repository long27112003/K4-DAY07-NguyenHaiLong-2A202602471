# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** G25
**Thành viên:**
1. Nguyễn Đức Thắng (Data Lead)
2. Nguyễn Hải Long (Strategy Lead)
3. Ngô Tiến Dũng (Benchmark Lead)
4. Trần Anh Quân (Report & Demo Lead)
**Ngày:** 20/09/2026

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

**Thành viên 2 — Nguyễn Đức Thắng (Data Lead)**
- **Loại chiến lược:** `RecursiveChunker` (chunk_size=300)
- **Mô tả & lý do chọn:** Phụ trách thu thập và chuẩn hóa 7 tài liệu quy chế NEU. Thử nghiệm chiến lược chia đệ quy chuẩn với độ ưu tiên phân tách đoạn `\n\n`, sau đó đến dòng `\n` và câu `. `, giúp văn bản phân rã tự nhiên theo cấu trúc đoạn mà không phụ thuộc định dạng markdown.

**Thành viên 3 — Ngô Tiến Dũng (Benchmark Lead)**
- **Loại chiến lược:** `FixedSizeChunker` (chunk_size=300, overlap=50)
- **Mô tả & lý do chọn:** Phụ trách xây dựng bộ câu hỏi đánh giá và kiểm tra trích dẫn. Thử nghiệm chiến lược kích thước cố định có độ chồng lấn (overlap) 50 ký tự để làm đường cơ sở đối chứng, nhằm kiểm tra xem độ chồng lấn có giúp bù đắp sự thiếu hụt cấu trúc so với chia theo Heading hay không.

**Thành viên 4 — Trần Anh Quân (Report & Demo Lead)**
- **Loại chiến lược:** `SentenceChunker` (max_sentences_per_chunk=3)
- **Mô tả & lý do chọn:** Phụ trách tổng hợp báo cáo và dẫn dắt phần thuyết trình. Thử nghiệm chiến lược chia theo từng câu ngữ pháp hoàn chỉnh và gom 3 câu thành 1 chunk, bảo đảm không làm gãy rụng các câu điều kiện trong quy chế đào tạo.

### So Sánh Giữa Các Thành Viên

| Thành viên | Vai trò | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|---|----------|----------------------|-----------|----------|
| Nguyễn Hải Long | Strategy Lead | `MarkdownSectionChunker` (Heading) | 8/10 | Giữ trọn vẹn ngữ cảnh điều khoản, gắn kèm tiêu đề mục cha giúp agent hiểu chính xác phạm vi áp dụng. | Khó tối ưu nếu gặp văn bản thuần text không có tiêu đề markdown. |
| Nguyễn Đức Thắng | Data Lead | `RecursiveChunker` | 7/10 | Linh hoạt với mọi định dạng văn bản, tránh sinh ra chunk vụn nhờ cơ chế gom mảnh. | Đôi khi cắt rời tiêu đề mục khỏi các điều khoản chi tiết bên dưới. |
| Ngô Tiến Dũng | Benchmark Lead | `FixedSizeChunker` (overlap 50) | 5/10 | Dễ cài đặt, kích thước chunk rất đồng đều. | Cắt ngang câu và cụm số liệu (ví dụ cắt giữa mốc 14 và tín chỉ), gây nhiễu embedding. |
| Trần Anh Quân | Report & Demo Lead | `SentenceChunker` (3 câu/chunk) | 6/10 | Bảo toàn trọn vẹn cấu trúc câu ngữ pháp, không bị câu cụt. | Độ dài chunk không đồng đều giữa các đoạn ngắn và đoạn dài. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Chiến lược **`MarkdownSectionChunker` (theo Heading/Section)** là tốt nhất cho chủ đề Quy chế đào tạo. Lý do là các quy định học vụ mang tính pháp lý cao, các điều kiện và con số ràng buộc lẫn nhau trong cùng một điều khoản; việc giữ trọn vẹn cả tiêu đề mục lẫn nội dung bên trong giúp vector embedding nắm bắt trọn vẹn ngữ nghĩa và hạn chế tối đa việc mất ngữ cảnh khi truy xuất.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? | Câu trả lời của Agent (tóm tắt) |
|---|---|---|---|---|---|
| 1 | Trường tổ chức cho sinh viên đăng ký học muộn nhất bao lâu trước khi bắt đầu học kỳ? | `trach-nhiem-giang-vien — Điều 22 Đề thi kết thúc học phần` | `+0.621` | ❌ Không | *"Không có thông tin về thời gian muộn nhất trường tổ chức cho sinh viên đăng ký học"* — từ chối bịa |
| 2 | Học cải thiện điểm được tối đa bao nhiêu tín chỉ trong học kỳ 1? | `dang-ky-hoc-phan — Điều 11 Học lại` | `+0.770` | ✅ Có | *"Trong học kỳ 1, sinh viên được học cải thiện điểm tối đa không quá 8 tín chỉ [1]"* |
| 3 | Khi không đồng ý với điểm thi thì làm gì? *(lọc audience=student)* | `phuc-khao-khieu-nai-diem — Điều 26` | `+0.498` | ✅ Có | Phân biệt 2 trường hợp: điểm giảng viên $\rightarrow$ khiếu nại trực tiếp giảng viên [1]; điểm thi học phần $\rightarrow$ nộp đơn Phòng Thanh tra, ĐBCLGD & Khảo thí [1] |
| 4 | Sinh viên được tuyển chọn vào chương trình Chất lượng cao như thế nào? *(lọc program)* | `dao-tao-chat-luong-cao — Điều 11` | `+0.764` | ✅ Có | Liệt kê diện xét tuyển thẳng: đội tuyển Olympic quốc tế, giải nhất/nhì/ba HSG quốc gia lớp 12 [3] |
| 5 | Điều kiện để được xét công nhận tốt nghiệp gồm những gì? | `tot-nghiep — Điều 30` | `+0.813` | ✅ Có | Liệt kê đủ 7 điều kiện a–g theo Điều 30 khoản 1 |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Trường tổ chức cho sinh viên đăng ký học muộn nhất bao lâu trước khi bắt đầu học kỳ? | `MarkdownSectionChunker` | Không (Top-1 rơi vào Điều 22 đề thi) | **2/2 điểm (Cơ chế chống ảo giác - Hallucination Guardrail):** Tài liệu không có mốc thời gian muộn nhất, agent phát hiện thiếu ngữ cảnh và từ chối bịa thông tin theo đúng quy tắc. |
| 2 | Học cải thiện điểm được tối đa bao nhiêu tín chỉ trong học kỳ 1? | `MarkdownSectionChunker` | Có (Top 1 trúng Điều 11) | **2/2 điểm:** Trích xuất chính xác quy định khống chế tối đa 8 tín chỉ trong học kỳ 1 theo Điều 11. |
| 3 | Khi không đồng ý với điểm thi thì làm gì? *(lọc audience=student)* | `MarkdownSectionChunker` + Filter | Có (Trúng Điều 26) | **2/2 điểm:** Lọc đúng `audience: student`, phân tách chuẩn xác 2 trường hợp khiếu nại giảng viên và nộp đơn phúc khảo tại Phòng Thanh tra, ĐBCLGD & Khảo thí. |
| 4 | Sinh viên được tuyển chọn vào chương trình Chất lượng cao như thế nào? *(lọc program)* | `RecursiveChunker` + Filter | Có (Trúng Điều 11 AEP) | **2/2 điểm:** Lọc theo chương trình tiên tiến/chất lượng cao, liệt kê đầy đủ diện tuyển thẳng Olympic quốc tế và giải HSG quốc gia lớp 12. |
| 5 | Điều kiện để được xét công nhận tốt nghiệp gồm những gì? | `MarkdownSectionChunker` | Có (Trúng Điều 30) | **2/2 điểm:** Trích xuất đầy đủ và chuẩn xác 7 điều kiện (a–g) theo Điều 30 khoản 1 quy chế đào tạo. |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Lọc bằng metadata phát huy giá trị rất rõ ở **Câu hỏi 3** (`audience=student`) và **Câu hỏi 4** (`program / department=advanced-education-program`). Tại Câu 3, việc áp dụng pre-filter loại bỏ các tài liệu nội bộ dành cho giảng viên/cố vấn, giúp câu trả lời tập trung vào quyền khiếu nại và phúc khảo của sinh viên. Tại Câu 4, bộ lọc theo chương trình giúp hệ thống không bị nhầm lẫn giữa tiêu chuẩn xét tuyển đại học thông thường và tiêu chí tuyển chọn đặc thù của chương trình Chất lượng cao / Tiên tiến.


---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. **Chấm điểm hai mức (File-level vs Content-level):** Việc tìm ra đúng tài liệu gốc (`doc_id`) không đồng nghĩa với việc chunk đó trả lời được câu hỏi; cần đánh giá xem đoạn trích xuất có thực sự chứa số liệu/điều khoản cốt lõi hay không.
> 2. **Ưu thế của Context-aware Heading Chunking:** Đối với văn bản pháp quy, cắt theo cấu trúc đề mục (`## Điều...`) và gắn lại tiêu đề mục cha vào từng mảnh con giúp loại bỏ hiện tượng "mất gốc ngữ cảnh" mà FixedSize thường gặp phải.
> 3. **Tầm quan trọng của Pre-filtering:** Trong các cơ sở tri thức phân quyền (Sinh viên, Giảng viên, Chuyên viên), việc lọc metadata trước khi tìm kiếm vector là điều kiện tiên quyết để tránh ô nhiễm ngữ cảnh câu trả lời.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một bộ tài liệu, chiến lược `FixedSize` dễ làm đứt gãy giữa câu và số liệu; chiến lược `Recursive` cải thiện việc phân đoạn tự nhiên nhưng đôi khi cắt rời tiêu đề mục; trong khi `MarkdownSectionChunker` đem lại kết quả có cấu trúc hoàn chỉnh nhất. Ngoài ra, việc dùng `MockEmbedder` băm ký tự cho thấy rõ sự cần thiết phải nâng cấp lên pre-trained multilingual embedding trong các ứng dụng RAG thực tế.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ triển khai ngay embedding model thực thụ (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) từ đầu để tối ưu hóa khả năng hiểu ngữ nghĩa tiếng Việt chuyên sâu; đồng thời gán thêm các trường metadata chi tiết hơn như `section_type` (định mức, quy trình, kỷ luật) để nâng cao độ chính xác của bộ lọc.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
