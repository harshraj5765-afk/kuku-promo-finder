import pytest
from src.parser import ScriptEvent, Scene, Episode
from src.detector import score_hook, score_cliffhanger
from src.ranker import find_candidate_promos

def test_hook_scoring():
    events = [
        ScriptEvent("ACTION", None, 0.0, 2.0, "He raises a dagger and tears her dress."),
        ScriptEvent("DIALOGUE", "GERALD", 1.0, 3.0, "I want a divorce right now!")
    ]
    res = score_hook(events)
    assert res["hook_score"] > 3.0
    assert "dagger" in res["hook_description"].lower() or "divorce" in res["hook_description"].lower()

def test_cliffhanger_scoring():
    events = [
        ScriptEvent("DIALOGUE", "JULIANA", 25.0, 28.0, "Who poisoned the Duchess?"),
        ScriptEvent("SOUND FX", None, 28.0, 30.0, "Ominous cliffhanger music cut to black.")
    ]
    res = score_cliffhanger(events)
    assert res["cliffhanger_score"] >= 4.0
    assert "unanswered" in res["cliffhanger_description"].lower() or "cliffhanger" in res["cliffhanger_description"].lower()

def test_promo_duration_constraints():
    events = []
    t = 0.0
    for i in range(20):
        events.append(ScriptEvent("DIALOGUE", f"CHAR_{i}", round(t, 2), round(t + 4.0, 2), f"Line {i} content"))
        t += 4.5
    
    dummy_scene = Scene("01", "INT. ROOM", 0.0, t, events)
    dummy_ep = Episode(1, "Test logline", [dummy_scene])
    
    candidates = find_candidate_promos(dummy_ep, min_dur=20.0, max_dur=60.0)
    assert len(candidates) > 0
    for cand in candidates:
        assert 20.0 <= cand["duration_sec"] <= 60.0, f"Promo duration {cand['duration_sec']} out of bounds!"
