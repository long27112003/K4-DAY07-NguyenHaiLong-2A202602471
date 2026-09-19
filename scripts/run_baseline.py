import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunking import ChunkingStrategyComparator

comparator = ChunkingStrategyComparator()
files = [
    "data/quy-che-dao-tao-neu/khoi-luong-hoc-tap-va-dang-ky.md",
    "data/quy-che-dao-tao-neu/canh-bao-hoc-tap-va-buoc-thoi-hoc.md",
    "data/quy-che-dao-tao-neu/xet-va-cong-nhan-tot-nghiep.md",
]

print("=== BASELINE CHUNKING ANALYSIS ===")
for f in files:
    content = Path(f).read_text(encoding="utf-8")
    body = content.split("---", 2)[-1].strip()
    res = comparator.compare(body, chunk_size=300)
    print(f"File: {Path(f).name} (len={len(body)} chars)")
    for strat, data in res.items():
        print(f"  {strat:15}: count={data['count']:2d}, avg_length={data['avg_length']:6.2f}")
