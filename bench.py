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
        "type": "Tra cứu số liệu",
        "query": "Sinh viên bình thường được đăng ký tối đa và tối thiểu bao nhiêu tín chỉ trong một học kỳ chính?",
        "filter": None,
        "gold_doc": "khoi-luong-hoc-tap-va-dang-ky",
        "gold_answer": "Tối thiểu 14 tín chỉ, tối đa 25 tín chỉ (với GPA >= 2.0).",
    },
    {
        "id": "Q2",
        "type": "Điều kiện học vụ",
        "query": "Sinh viên bị buộc thôi học trong những trường hợp nào theo quy chế đào tạo?",
        "filter": None,
        "gold_doc": "canh-bao-hoc-tap-va-buoc-thoi-hoc",
        "gold_answer": "Bị 2 lần cảnh báo học tập liên tiếp; hoặc quá thời gian tối đa 6 năm (12 học kỳ chính).",
    },
    {
        "id": "Q3",
        "type": "Quy trình học vụ",
        "query": "Quy định rút học phần từ tuần thứ 3 đến tuần thứ 6 như thế nào và sinh viên nhận điểm gì?",
        "filter": None,
        "gold_doc": "rut-hoc-phan-va-nghi-tam-thoi",
        "gold_answer": "Nộp đơn có xác nhận của Cố vấn học tập, số tín chỉ còn lại không dưới 14 TC, nhận điểm W và không hoàn học phí.",
    },
    {
        "id": "Q4",
        "type": "Quy định tốt nghiệp",
        "query": "Sinh viên có điểm CPA loại Giỏi hoặc Xuất sắc bị hạ một bậc xếp loại tốt nghiệp khi nào?",
        "filter": None,
        "gold_doc": "xet-va-cong-nhan-tot-nghiep",
        "gold_answer": "Khi số tín chỉ học lại do điểm F vượt quá 5% tổng số tín chỉ, hoặc bị kỷ luật từ mức khiển trách trở lên.",
    },
    {
        "id": "Q5",
        "type": "Phân định đối tượng (A/B Test Filter)",
        "query": "Hạn mức đăng ký học phần tối đa trong một học kỳ chính là bao nhiêu tín chỉ và ai có thẩm quyền phê duyệt khi vượt quá hạn mức thông thường?",
        "filter": {"audience": "student"},
        "gold_doc": "khoi-luong-hoc-tap-va-dang-ky",
        "gold_answer": "Sinh viên tự đăng ký tối đa 25 tín chỉ; muốn đăng ký vượt (tối đa 28 tín chỉ) phải do Cố vấn học tập phê duyệt cho sinh viên có CPA >= 3.20.",
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
