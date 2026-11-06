import glob
import json
import csv
import os
from src.parser import parse_episode_file
from src.ranker import find_candidate_promos

def run_pipeline(raw_dir: str = "data/raw", out_dir: str = "data/outputs"):
    os.makedirs(out_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(raw_dir, "*.txt")))
    
    if not files:
        print(f"No files found in {raw_dir}.")
        return

    print(f"Processing {len(files)} script episodes...")
    all_promos = []

    for fpath in files:
        ep = parse_episode_file(fpath)
        candidates = find_candidate_promos(ep)
        # Keep top candidate per scene to prevent overlapping duplicates
        seen_scenes = set()
        for cand in candidates:
            key = (cand["episode"], cand["scene"])
            if key not in seen_scenes:
                all_promos.append(cand)
                seen_scenes.add(key)

    # Global ranking across all episodes
    all_promos.sort(key=lambda x: x["overall_score"], reverse=True)
    print(f"Generated {len(all_promos)} unique candidate promos.")

    # Save to JSON
    json_path = os.path.join(out_dir, "ranked_promos.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_promos, f, indent=2)
    print(f"Saved JSON to: {json_path}")

    # Save to CSV
    csv_path = os.path.join(out_dir, "ranked_promos.csv")
    if all_promos:
        keys = all_promos[0].keys()
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_promos)
        print(f"Saved CSV to: {csv_path}")

    # Preview Top 5 Promos
    print("\n--- TOP 5 RANKED PROMOS ---")
    for idx, p in enumerate(all_promos[:5], 1):
        print(f"{idx}. Episode {p['episode']} | {p['start_time']}s - {p['end_time']}s ({p['duration_sec']}s) | Score: {p['overall_score']}")
        print(f"   Hook: {p['hook']}")
        print(f"   Cliffhanger: {p['cliffhanger']}")
        print(f"   Rationale: {p['why_it_works']}\n")

if __name__ == "__main__":
    run_pipeline()
