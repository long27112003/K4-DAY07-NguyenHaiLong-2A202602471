import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunking import compute_similarity
from src.embeddings import MockEmbedder

embedder = MockEmbedder()

pairs = [
    ("Sinh viên đăng ký tối thiểu 14 tín chỉ trong mỗi học kỳ chính.", "Người học hệ cử nhân bắt buộc tích lũy không dưới 14 tín chỉ mỗi kỳ chuẩn."),
    ("Quy chế đào tạo đại học chính quy theo hệ thống tín chỉ.", "Quy chế đào tạo đại học chính quy theo hệ thống tín chỉ."),
    ("Sinh viên hoàn thành đủ 130 tín chỉ để được xét tốt nghiệp.", "Trận đấu bóng đá giao hữu bị hoãn do trời mưa bão."),
    ("Học phần bị điểm F bắt buộc phải đăng ký học lại.", "Sinh viên đạt điểm D và C được quyền học cải thiện nâng cao GPA."),
    ("Sinh viên được phép rút học phần trong 2 tuần đầu.", "Sinh viên không được phép rút học phần trong 2 tuần đầu.")
]

print("=== SIMILARITY EXPERIMENT ===")
for i, (a, b) in enumerate(pairs, 1):
    va = embedder(a)
    vb = embedder(b)
    sim = compute_similarity(va, vb)
    print(f"Cap {i}: {sim:.4f}")
