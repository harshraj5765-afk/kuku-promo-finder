import re
from typing import List, Dict, Any
from src.parser import ScriptEvent

HOOK_ACTION_KEYWORDS = ["slap", "grab", "push", "kneel", "tears", "shatter", "gun", "dagger", "sword", "blood", "handcuff", "ring", "choke", "drag", "strike"]
HOOK_DIALOGUE_KEYWORDS = ["divorce", "marry", "betray", "bastard", "liar", "kill", "poison", "pregnant", "disowned", "beggar", "duke", "who are you", "mistake"]
CLIFFHANGER_KEYWORDS = ["wait", "stop", "who", "why", "reveal", "gasp", "cut to black", "freeze", "disbelief", "impossible", "truth", "no", "burn"]

def matches_word(word: str, text: str) -> bool:
    """Exact word boundary match so 'ring' doesn't match 'during' or 'storing'."""
    pattern = rf"\b{re.escape(word)}\b"
    return bool(re.search(pattern, text, re.IGNORECASE))

def score_hook(events_in_first_3s: List[ScriptEvent]) -> Dict[str, Any]:
    score = 0.0
    reasons = []

    for event in events_in_first_3s:
        text = event.content.lower()

        if event.event_type == "ACTION":
            matched = [w for w in HOOK_ACTION_KEYWORDS if matches_word(w, text)]
            if matched:
                score += 3.0
                reasons.append(f"Visual hook: {', '.join(matched)}")

        elif event.event_type == "DIALOGUE":
            matched = [w for w in HOOK_DIALOGUE_KEYWORDS if matches_word(w, text)]
            if matched:
                score += 3.5
                reasons.append(f"Verbal hook ({event.speaker}): {', '.join(matched)}")
            else:
                score += 1.0

        if event.event_type == "CAMERA" and any(k in text for k in ["close-up", "push-in", "extreme"]):
            score += 0.5

    final_score = min(round(score, 2), 5.0)
    hook_desc = "; ".join(reasons) if reasons else "Standard scene opening"
    return {"hook_score": final_score, "hook_description": hook_desc}

def score_cliffhanger(events_in_last_5s: List[ScriptEvent]) -> Dict[str, Any]:
    score = 0.0
    reasons = []

    for event in events_in_last_5s:
        text = event.content.lower()

        if event.event_type in ["SOUND FX", "CAMERA"]:
            if any(term in text for term in ["cliffhanger", "cut to black", "drone", "swell", "silence"]):
                score += 3.0
                reasons.append("Cinematic audio/visual cliffhanger cut")

        if event.event_type == "ACTION":
            matched = [w for w in HOOK_ACTION_KEYWORDS if matches_word(w, text)]
            if matched:
                score += 2.0
                reasons.append(f"Unfinished physical beat: {', '.join(matched)}")

        elif event.event_type == "DIALOGUE":
            if "?" in event.content:
                score += 2.5
                reasons.append("Unanswered dramatic question")
            matched = [w for w in CLIFFHANGER_KEYWORDS if matches_word(w, text)]
            if matched:
                score += 1.5
                reasons.append(f"High-stakes line: {', '.join(matched)}")

    final_score = min(round(score, 2), 5.0)
    cliff_desc = "; ".join(reasons) if reasons else "Standard scene transition"
    return {"cliffhanger_score": final_score, "cliffhanger_description": cliff_desc}
