import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import MemoryDecayForgettingCurveAuditorClient

def main():
    client = MemoryDecayForgettingCurveAuditorClient()
    res = client.audit_memory_decay()
    print("=== Memory Decay Forgetting Curve Auditor Output ===")
    print(f"User: {res['user_id']} | Total Memories: {res['total_memories_audited']}")
    print(f"Stale Flagged: {res['stale_facts_flagged_count']} ({res['garbage_collection_ratio']}) | Action: {res['recommended_gc_action']}")
    print("\nAudited Memory Retention Scores:")
    for m in res['audited_memory_dossier']:
        stale_tag = "[PRUNE]" if m['is_stale_garbage_collection_candidate'] else "[RETAIN]"
        print(f"  * {stale_tag:8s} Retention: {m['retention_probability']*100:5.1f}% (Idle {m['days_idle']:3d}d) | {m['content']}")

if __name__ == '__main__':
    main()
