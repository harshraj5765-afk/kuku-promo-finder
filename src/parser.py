import re
import os
import glob
from dataclasses import dataclass, field
from typing import List, Optional

def parse_timestamp(ts_str: str) -> float:
    """Converts (MM:SS.ms) or MM:SS.ms to total seconds."""
    ts_str = ts_str.strip("()")
    parts = ts_str.split(":")
    if len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
        return round(minutes * 60 + seconds, 2)
    elif len(parts) == 3:
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return round(hours * 3600 + minutes * 60 + seconds, 2)
    return float(ts_str)

@dataclass
class ScriptEvent:
    event_type: str  # CAMERA, ACTION, DIALOGUE, SOUND FX
    speaker: Optional[str]
    start_time: float
    end_time: float
    content: str

@dataclass
class Scene:
    scene_number: str
    heading: str
    start_time: float
    end_time: float
    events: List[ScriptEvent] = field(default_factory=list)

@dataclass
class Episode:
    episode_num: int
    logline: str
    scenes: List[Scene] = field(default_factory=list)

def parse_episode_file(filepath: str) -> Episode:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Extract episode number
    ep_num_match = re.search(r"EPISODE NUMBER:\s*Episode\s*(\d+)", text, re.IGNORECASE)
    ep_num = int(ep_num_match.group(1)) if ep_num_match else 0

    # Extract logline
    logline_match = re.search(r"EPISODE LOGLINE:\s*(.*?)(?=\n[A-Z\s]+:|\n---)", text, re.DOTALL)
    logline = logline_match.group(1).strip() if logline_match else ""

    episode = Episode(episode_num=ep_num, logline=logline)

    # Split into scenes
    scene_blocks = re.split(r"(?=SCENE\s+\d+)", text)
    for block in scene_blocks:
        if not block.strip().startswith("SCENE"):
            continue
        
        heading_match = re.search(r"Scene heading:\s*(.*?)\n", block)
        heading = heading_match.group(1).strip() if heading_match else ""

        start_match = re.search(r"Scene start:\s*([\d:\.]+)", block)
        end_match = re.search(r"Scene end:\s*([\d:\.]+)", block)
        sc_start = parse_timestamp(start_match.group(1)) if start_match else 0.0
        sc_end = parse_timestamp(end_match.group(1)) if end_match else 0.0

        num_match = re.search(r"SCENE\s+(\d+)", block)
        sc_num = num_match.group(1) if num_match else "01"

        scene = Scene(scene_number=sc_num, heading=heading, start_time=sc_start, end_time=sc_end)

        # Regex for timed actions, camera, and dialogue
        pattern = re.compile(
            r"\*\*(CAMERA|ACTION|SOUND FX|[A-Z\s\(\)\.\'\/]+?)\:\*\*\s*"
            r"Start:\s*\(([\d:\.]+)\)\s*\|\s*End:\s*\(([\d:\.]+)\)\s*"
            r"(.*?)(?=\*\*[A-Z]|\n---|\Z)",
            re.DOTALL
        )

        for match in pattern.finditer(block):
            tag = match.group(1).strip()
            t_start = parse_timestamp(match.group(2))
            t_end = parse_timestamp(match.group(3))
            body = match.group(4).strip()

            if tag in ["CAMERA", "ACTION", "SOUND FX"]:
                event_type = tag
                speaker = None
            else:
                event_type = "DIALOGUE"
                speaker = tag

            scene.events.append(ScriptEvent(
                event_type=event_type,
                speaker=speaker,
                start_time=t_start,
                end_time=t_end,
                content=body
            ))

        episode.scenes.append(scene)

    return episode

if __name__ == "__main__":
    files = sorted(glob.glob("data/raw/*.txt"))
    if not files:
        print("No script files found in data/raw/. Please add them first.")
    else:
        ep = parse_episode_file(files[0])
        print(f"Parsed Episode {ep.episode_num} with {len(ep.scenes)} scenes.")
        if ep.scenes:
            print(f"Scene 1 has {len(ep.scenes[0].events)} timed events.")
