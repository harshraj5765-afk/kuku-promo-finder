# Kuku Promo Finder

Automated tool to analyze AI microdrama screenplays and extract optimal 20-60 second promotional video cuts (Instagram Reels, TikTok, YouTube Shorts) by scoring 0-3 second hooks and terminal cliffhangers.

## Features
- Deterministic Timestamp Parser: Extracts scene boundaries, dialogue, actions, sound FX, and camera angles.
- Hook and Cliffhanger Detection: Evaluates 0-3s hook intensity and cut-off points.
- Duration Constraint Windowing: Strictly filters candidates to 20-60 seconds.
- Deduplicated Series Ranking: Ranks top candidates across all episodes.
- Interactive Review UI: Built-in Streamlit app for human editors.

## Installation & Setup
```bash
git clone [https://github.com/harshraj5765-afk/kuku-promo-finder.git](https://github.com/harshraj5765-afk/kuku-promo-finder.git)
cd kuku-promo-finder
python3 -m pip install -r requirements.txt
```

## Running the Pipeline
```bash
python3 -m src.pipeline
```

## Interactive Dashboard
```bash
python3 -m streamlit run app.py
```

## Running Tests
```bash
python3 -m pytest tests/
```
