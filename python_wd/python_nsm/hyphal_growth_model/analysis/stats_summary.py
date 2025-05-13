# analysis/stats_summary.py

from core.mycel import Mycel
from core.section import Section
import numpy as np

def summarise(mycel: Mycel):
    segments = mycel.get_all_segments()
    tips = [s for s in segments if s.is_tip and not s.is_dead]
    depths = [get_depth(s) for s in tips]

    ages = [s.age for s in segments]
    lengths = [s.length for s in segments]
    child_counts = [len(s.children) for s in segments]

    print("\n📊 FINAL SIMULATION SUMMARY")
    print(f"🧩 Total segments: {len(segments)}")
    print(f"🌱 Active tips: {len(tips)}")
    print(f"📏 Avg segment length: {np.mean(lengths):.2f}")
    print(f"⏳ Avg segment age: {np.mean(ages):.2f}")
    print(f"🌿 Max depth from root: {max(depths) if depths else 0}")
    print(f"🔗 Avg branches per node: {np.mean(child_counts):.2f}")

def get_depth(section: Section) -> int:
    """Recursively computes depth from root."""
    depth = 0
    current = section
    while current.parent:
        current = current.parent
        depth += 1
    return depth
