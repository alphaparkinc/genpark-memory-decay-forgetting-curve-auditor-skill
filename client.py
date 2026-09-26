import json
import math
from typing import Dict, Any, List, Optional

class MemoryDecayForgettingCurveAuditorClient:
    """
    Production-grade memory retention and Ebbinghaus forgetting curve auditor.
    Evaluates stored memory items based on elapsed days, access count, and reinforcement strength;
    calculates retention probabilities and identifies stale facts for automatic garbage collection.
    """
    def __init__(self, half_life_days: float = 30.0, gc_retention_threshold: float = 0.35):
        self.half_life = half_life_days
        self.threshold = gc_retention_threshold

    def audit_memory_decay(
        self,
        user_id: str = "usr_sarah_connor",
        memory_store_items: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        if not memory_store_items:
            memory_store_items = [
                {"fact_id": "f_01", "content": "User prefers dark mode in all IDEs", "days_since_last_access": 3, "access_count": 18, "reinforcement_level": 3},
                {"fact_id": "f_02", "content": "Attended React conference in June 2024", "days_since_last_access": 120, "access_count": 1, "reinforcement_level": 1},
                {"fact_id": "f_03", "content": "Enterprise GitHub org is alphaparkinc", "days_since_last_access": 1, "access_count": 45, "reinforcement_level": 5},
                {"fact_id": "f_04", "content": "Temporary discount code PROMO2024 expired", "days_since_last_access": 95, "access_count": 2, "reinforcement_level": 1}
            ]

        audited_memories = []
        gc_candidates = []

        for item in memory_store_items:
            t = item["days_since_last_access"]
            s = item["reinforcement_level"] * (1.0 + (item["access_count"] * 0.1))
            # Ebbinghaus memory retention model: R = e^(-t / S)
            retention_prob = round(math.exp(-t / max(1.0, s * self.half_life)), 3)

            is_stale = retention_prob < self.threshold
            entry = {
                "fact_id": item["fact_id"],
                "content": item["content"],
                "days_idle": t,
                "retention_probability": retention_prob,
                "is_stale_garbage_collection_candidate": is_stale
            }
            audited_memories.append(entry)
            if is_stale:
                gc_candidates.append(item["fact_id"])

        gc_percentage = round((len(gc_candidates) / max(1, len(memory_store_items))) * 100, 1)

        return {
            "audit_id": "dcy_aud_4412",
            "user_id": user_id,
            "total_memories_audited": len(memory_store_items),
            "stale_facts_flagged_count": len(gc_candidates),
            "garbage_collection_ratio": f"{gc_percentage}%",
            "flagged_fact_ids_for_eviction": gc_candidates,
            "audited_memory_dossier": audited_memories,
            "recommended_gc_action": "EXECUTE_PRUNE_STALE_MEMORIES" if gc_candidates else "RETAIN_ACTIVE_STORAGE"
        }
