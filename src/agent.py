from __future__ import annotations

from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        if self.store.get_collection_size() == 0:
            return "Cơ sở tri thức hiện chưa có dữ liệu để trả lời câu hỏi."

        results = self.store.search(question, top_k=top_k)
        if not results:
            return "Không tìm thấy thông tin phù hợp trong cơ sở tri thức để trả lời câu hỏi này."

        context_blocks = []
        for i, res in enumerate(results, start=1):
            source = (
                res["metadata"].get("source")
                or res["metadata"].get("doc_id")
                or res.get("id")
                or f"Doc_{i}"
            )
            content = res["content"].strip()
            context_blocks.append(f"[{i}] (Nguồn: {source})\n{content}")

        context_text = "\n\n".join(context_blocks)

        prompt = (
            "Bạn là một trợ lý ảo học vụ thông minh, trả lời câu hỏi dựa trên các tài liệu được cung cấp.\n\n"
            f"=== NGỮ CẢNH TRÍCH XUẤT ===\n"
            f"{context_text}\n\n"
            f"=== CÂU HỎI ===\n"
            f"{question}\n\n"
            "=== YÊU CẦU TRẢ LỜI ===\n"
            "1. Chỉ sử dụng thông tin có trong ngữ cảnh trên để trả lời. Không tự suy đoán thông tin ngoài ngữ cảnh.\n"
            "2. Trích dẫn số thứ tự của tài liệu nguồn tương ứng dạng [1], [2] khi đưa ra các điều khoản hoặc thông tin cụ thể.\n"
            "3. Nếu ngữ cảnh không chứa đủ thông tin để trả lời, hãy nêu rõ rằng thông tin không tìm thấy trong tài liệu."
        )

        return self.llm_fn(prompt)
