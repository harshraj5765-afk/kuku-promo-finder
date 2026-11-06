from typing import List, Dict, Any
from src.parser import Episode, ScriptEvent
from src.detector import score_hook, score_cliffhanger

def find_candidate_promos(episode: Episode, min_dur: float = 20.0, max_dur: float = 60.0) -> List[Dict[str, Any]]:
    candidates = []

    for scene in episode.scenes:
        events = scene.events
        n = len(events)
        if n < 2:
            continue

        for i in range(n):
            start_time = events[i].start_time

            for j in range(i + 1, n):
                end_time = events[j].end_time
                duration = round(end_time - start_time, 2)

                # Strictly constrain promo clip length between 20s and 60s
                if duration < min_dur:
                    continue
                if duration > max_dur:
                    break  # Exceeds max window

                # Extract events within the candidate window
                window_events = events[i:j+1]
                
                # First 3 seconds for hook analysis
                hook_events = [e for e in window_events if e.start_time <= start_time + 3.0]
                # Last 5 seconds for cliffhanger cut analysis
                cliff_events = [e for e in window_events if e.end_time >= end_time - 5.0]

                hook_res = score_hook(hook_events)
                cliff_res = score_cliffhanger(cliff_events)

                # Composite score prioritizing early hook retention + unresolved ending
                total_score = round((hook_res["hook_score"] * 1.2) + (cliff_res["cliffhanger_score"] * 1.0), 2)

                # Generate brief explanation on why this clip works
                why_it_works = f"Starts with {hook_res['hook_description'].lower()} and cuts on {cliff_res['cliffhanger_description'].lower()}."

                candidates.append({
                    "episode": episode.episode_num,
                    "scene": scene.scene_number,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_sec": duration,
                    "hook_score": hook_res["hook_score"],
                    "hook": hook_res["hook_description"],
                    "cliffhanger_score": cliff_res["cliffhanger_score"],
                    "cliffhanger": cliff_res["cliffhanger_description"],
                    "overall_score": total_score,
                    "why_it_works": why_it_works
                })

    # Sort descending by overall score
    candidates.sort(key=lambda x: x["overall_score"], reverse=True)
    return candidates
