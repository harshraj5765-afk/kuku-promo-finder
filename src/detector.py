from typing import List, Dict, Any
from src.parser import Episode, ScriptEvent

# High-impact emotional and physical trigger words common in microdrama hooks & cliffhangers
HOOK_ACTION_KEYWORDS = {"slap", "grab", "push", "kneel", "tears", "shatter", "gun", "dagger", "sword", "blood", "handcuff", "ring"}
HOOK_DIALOGUE_KEYWORDS = {"divorce", "marry", "betray", "bastard", "liar", "kill", "poison", "pregnant", "disowned", "beggar", "duke", "who are you"}
CLIFFHANGER_KEYWORDS = {"wait", "stop", "who", "why", "reveal", "gasp", "cut to black", "freeze", "disbelief", "impossible", "truth"}

def score_hook(events_in_first_3s: List[ScriptEvent]) -> Dict[str, Any]:
    score = 0.0
    reasons = []

    for event in events_in_first_3s:
        text = event.content.lower()
        
        # High impact action in opening moments
        if event.event_type == "ACTION":
            matched_actions = [w for w in HOOK_ACTION_KEYWORDS if w in text]
            if matched_actions:
                score += 3.0
                reasons.append(f"Visual hook action: {', '.join(matched_actions)}")
        
        # Punchy line of dialogue
        elif event.event_type == "DIALOGUE":
            matched_dialogue = [w for w in HOOK_DIALOGUE_KEYWORDS if w in text]
            if matched_dialogue:
                score += 3.5
                reasons.append(f"Verbal hook ({event.speaker}): {', '.join(matched_dialogue)}")
            else:
                score += 1.0

        if event.event_type == "CAMERA" and ("close-up" in text or "push-in" in text):
            score += 0.5

    final_score = min(round(score, 2), 5.0)
    hook_desc = "; ".join(reasons) if reasons else "Standard scene opening"
    return {"hook_score": final_score, "hook_description": hook_desc}

def score_cliffhanger(events_in_last_5s: List[ScriptEvent]) -> Dict[str, Any]:
    score = 0.0
    reasons = []

    for event in events_in_last_5s:
        text = event.content.lower()

        # Unresolved dramatic cuts or audio swells
        if event.event_type in ["SOUND FX", "CAMERA"]:
            if any(term in text for term in ["cliffhanger", "cut to black", "drone", "swell", "silence"]):
                score += 3.0
                reasons.append("Cinematic/audio unresolved cut")

        if event.event_type == "ACTION":
            matched_actions = [w for w in HOOK_ACTION_KEYWORDS if w in text]
            if matched_actions:
                score += 2.0
                reasons.append(f"Unfinished action beat: {', '.join(matched_actions)}")

        elif event.event_type == "DIALOGUE":
            # Questions or shocking accusations make great cliffhangers
            if "?" in event.content:
                score += 2.5
                reasons.append("Unanswered dramatic question")
            matched_words = [w for w in CLIFFHANGER_KEYWORDS if w in text]
            if matched_words:
                score += 1.5
                reasons.append(f"Cliffhanger line: {', '.join(matched_words)}")

    final_score = min(round(score, 2), 5.0)
    cliff_desc = "; ".join(reasons) if reasons else "Standard scene transition"
    return {"cliffhanger_score": final_score, "cliffhanger_description": cliff_desc}
