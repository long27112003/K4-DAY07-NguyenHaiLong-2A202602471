from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.chunking import FixedSizeChunker, RecursiveChunker, SentenceChunker
from src.embeddings import _mock_embed
from src.models import Document
from src.store import EmbeddingStore


class MarkdownSectionChunker:
    """
    Chiến lược chia nhỏ theo Tiêu đề/Mục (Heading/Section Chunker).
    Đặc biệt tối ưu cho văn bản quy chế, điều lệ đại học (K4-L3A).
    Tách theo các tiêu đề cấp 1-3 (#, ##, ###). Nếu mục nào quá dài,
    sử dụng RecursiveChunker để chia nhỏ và gắn lại tiêu đề mục để bảo toàn ngữ cảnh.
    """

    def __init__(self, max_chunk_size: int = 500) -> None:
        self.max_chunk_size = max_chunk_size
        self._fallback_chunker = RecursiveChunker(chunk_size=max_chunk_size)

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        # Tách theo các heading markdown (#, ##, ###)
        raw_sections = re.split(r"(?=(?:\n|^)#{1,3}\s+)", text.strip())
        sections = [s.strip() for s in raw_sections if s.strip()]

        chunks: list[str] = []
        for sec in sections:
            if len(sec) <= self.max_chunk_size:
                chunks.append(sec)
            else:
                # Nếu một mục quá dài, lấy tiêu đề của mục gắn vào từng mảnh con
                first_line = sec.split("\n", 1)[0].strip()
                sub_chunks = self._fallback_chunker.chunk(sec)
                for sub in sub_chunks:
                    if not sub.startswith("#") and first_line.startswith("#"):
                        chunks.append(f"{first_line}\n{sub}")
                    else:
                        chunks.append(sub)

        return chunks


def parse_markdown_file(file_path: Path) -> tuple[dict, str]:
    """Tách YAML frontmatter và nội dung thân văn bản."""
    raw_content = file_path.read_text(encoding="utf-8")
    if raw_content.startswith("---"):
        parts = raw_content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            metadata = dict(re.findall(r"^(\w+):\s*(.+)$", fm_text, re.M))
            return metadata, body
    return {}, raw_content.strip()


# Bộ 5 Benchmark Queries chuẩn chung của nhóm (theo quy chế NEU)
BENCHMARK_QUERIES = [
    {
        "id": "Q1",
        "type": "Ca Thất Bại / Từ Chối Bịa (Failure & Hallucination Guardrail)",
        "query": "Trường tổ chức cho sinh viên đăng ký học muộn nhất bao lâu trước khi bắt đầu học kỳ?",
        "filter": None,
        "gold_doc": "trach-nhiem-co-van-va-giang-vien",
        "gold_answer": "Không có thông tin về thời gian muộn nhất trường tổ chức cho sinh viên đăng ký học — từ chối bịa.",
    },
    {
        "id": "Q2",
        "type": "Định lượng học vụ & Đăng ký",
        "query": "Học cải thiện điểm được tối đa bao nhiêu tín chỉ trong học kỳ 1?",
        "filter": None,
        "gold_doc": "khoi-luong-hoc-tap-va-dang-ky",
        "gold_answer": "Trong học kỳ 1, sinh viên được học cải thiện điểm tối đa không quá 8 tín chỉ [1].",
    },
    {
        "id": "Q3",
        "type": "Quy trình khiếu nại (Lọc audience=student)",
        "query": "Khi không đồng ý với điểm thi thì làm gì?",
        "filter": {"audience": "student"},
        "gold_doc": "thang-diem-va-danh-gia-hoc-phan",
        "gold_answer": "Phân biệt 2 trường hợp: điểm giảng viên -> khiếu nại trực tiếp giảng viên [1]; điểm thi học phần -> nộp đơn Phòng Thanh tra, ĐBCLGD & Khảo thí [1].",
    },
    {
        "id": "Q4",
        "type": "Chương trình đào tạo đặc thù (Lọc program)",
        "query": "Sinh viên được tuyển chọn vào chương trình Chất lượng cao như thế nào?",
        "filter": {"department": "advanced-education-program"},
        "gold_doc": "quy-dinh-chuong-trinh-tien-tien-aep",
        "gold_answer": "Liệt kê diện xét tuyển thẳng: đội tuyển Olympic quốc tế, giải nhất/nhì/ba HSG quốc gia lớp 12 [3].",
    },
    {
        "id": "Q5",
        "type": "Điều kiện tốt nghiệp tổng hợp",
        "query": "Điều kiện để được xét công nhận tốt nghiệp gồm những gì?",
        "filter": None,
        "gold_doc": "xet-va-cong-nhan-tot-nghiep",
        "gold_answer": "Liệt kê đủ 7 điều kiện a–g theo Điều 30 khoản 1.",
    },
]



def run_benchmark(
    data_dir: str = "data/quy-che-dao-tao-neu",
    strategy_name: str = "section_heading",
    output_file: str = "ket_qua_benchmark.txt",
) -> None:
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"Lỗi: Không tìm thấy thư mục dữ liệu {data_dir}")
        return

    md_files = sorted(data_path.glob("*.md"))
    if not md_files:
        print(f"Lỗi: Không có file .md nào trong {data_dir}")
        return

    # Chọn chiến lược chunking
    if strategy_name == "section_heading":
        chunker = MarkdownSectionChunker(max_chunk_size=400)
    elif strategy_name == "recursive":
        chunker = RecursiveChunker(chunk_size=300)
    elif strategy_name == "sentence":
        chunker = SentenceChunker(max_sentences_per_chunk=3)
    else:
        chunker = FixedSizeChunker(chunk_size=300, overlap=30)

    # Nạp và chunk tài liệu
    documents: list[Document] = []
    for p in md_files:
        metadata, body = parse_markdown_file(p)
        chunks = chunker.chunk(body)
        for idx, chunk_text in enumerate(chunks):
            doc_id = p.stem
            chunk_metadata = {**metadata, "doc_id": doc_id, "chunk_idx": idx}
            documents.append(
                Document(
                    id=f"{doc_id}#{idx}",
                    content=chunk_text,
                    metadata=chunk_metadata,
                )
            )

    store = EmbeddingStore(collection_name="neu_regulations", embedding_fn=_mock_embed)
    store.add_documents(documents)

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("BÁO CÁO KẾT QUẢ BENCHMARK RETRIEVAL — LAB 07 (K4-L3A)")
    lines.append(f"Chủ đề: Quy chế đào tạo đại học NEU")
    lines.append(f"Chiến lược sử dụng: {strategy_name}")
    lines.append(f"Số file văn bản gốc: {len(md_files)}")
    lines.append(f"Tổng số chunks đã nạp: {store.get_collection_size()}")
    lines.append("=" * 70 + "\n")

    for q_idx, q_item in enumerate(BENCHMARK_QUERIES, start=1):
        lines.append(f"Câu hỏi {q_idx} [{q_item['type']}]: {q_item['query']}")
        lines.append(f"Đáp án chuẩn (Gold): {q_item['gold_answer']}")
        lines.append(f"Tài liệu nguồn mong đợi: {q_item['gold_doc']}.md")
        lines.append(f"Metadata filter áp dụng: {q_item['filter']}")

        # Truy xuất
        results = store.search_with_filter(
            query=q_item["query"],
            top_k=3,
            metadata_filter=q_item["filter"],
        )

        lines.append("Top-3 Chunks tìm được:")
        for rank, res in enumerate(results, start=1):
            doc_id = res["metadata"].get("doc_id", "unknown")
            score = res["score"]
            chunk_preview = res["content"][:120].replace("\n", " ")
            is_gold = " [TRÚNG GOLD DOC]" if doc_id == q_item["gold_doc"] else ""
            lines.append(
                f"  Top {rank}: [score={score:.4f}] doc_id={doc_id} ({res['id']}){is_gold}"
            )
            lines.append(f"         Preview: {chunk_preview}...")

        # Thử nghiệm A/B đối với câu hỏi có filter
        if q_item["filter"]:
            unfiltered_results = store.search(query=q_item["query"], top_k=3)
            lines.append("  --> Đối chiếu khi KHÔNG dùng filter:")
            for rank, res in enumerate(unfiltered_results, start=1):
                doc_id = res["metadata"].get("doc_id", "unknown")
                score = res["score"]
                lines.append(
                    f"      Top {rank}: [score={score:.4f}] doc_id={doc_id} ({res['id']}) [audience={res['metadata'].get('audience')}]"
                )

        lines.append("-" * 70)

    report_text = "\n".join(lines)
    print(report_text)

    # Lưu kết quả ra file
    Path(output_file).write_text(report_text, encoding="utf-8")
    print(f"\n[OK] Đã lưu toàn bộ kết quả benchmark vào file: {output_file}")


if __name__ == "__main__":
    run_benchmark()
