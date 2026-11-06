# Solution Document: Microdrama Promo Finder (Problem 1)

## 1. Problem Choice and Framing
Microdrama apps rely on organic and paid ad loops on short-form video channels (TikTok, Reels, Shorts) to acquire viewers. Today, editors manually review every 1-2 minute episode to identify 20-60s hooks and cliffhangers.

We scoped this problem down to an automated script-parsing and candidate-ranking pipeline that pinpoints:
1. **0-3 Second Hook**: A visual shock, high-stakes accusation, or physical confrontation that stops scrolling feeds.
2. **Terminal Cliffhanger**: A narrative drop-off or unresolved dramatic question that forces viewers to click through.
3. **Standalone Coherence**: Ensuring the selected window does not rely on obscure prior episode context.

## 2. Approach: Code vs. AI Trade-offs
Instead of sending 50 episodes of raw text to an LLM (costly, high token latency, prone to loose timestamp hallucinations), we implemented a two-stage hybrid approach:
- **Code (Deterministic Engine)**:
  - Regex-based screenplay tokenization extracting sub-second start and end points across dialogue, actions, camera directions, and sound FX.
  - Strict mathematical sliding window filtering ensuring all candidates respect 20 to 60 seconds duration constraints.
  - Word-boundary lexical scoring for emotional triggers, camera close-ups, and dramatic punctuation.
- **AI / LLM Role**:
  - LLMs are reserved for evaluating ambiguous candidates or generating one-sentence marketing copy explaining why a specific dialogue hook converts.
  - At real-world volume, this hybrid model keeps inference costs near zero while remaining 100% reproducible.

## 3. Real-World Scaling & Economics
- **Processing Cost**: Processing 50 episodes takes less than 2 seconds locally using standard Python libraries ($0 API cost).
- **Model Swapping**: The scoring module (src/detector.py) is decoupled. If deeper reasoning is required, low-cost API endpoints can be plugged directly into candidate scoring without rewriting the windowing engine.

## 4. Quality Checking & Failure Analysis
### Where the Tool Excels:
- Accurately captures high-drama action and sound cues across episodes.
- Guarantees strict compliance with video duration ad formats.

### Known Failure Modes:
1. **Understated Irony / Subtle Tension**: The heuristic relies on explicit physical actions and high-intensity vocabulary. Subtle dramatic reveals spoken quietly can receive lower scores.
2. **Context Bleed**: A clip might contain a strong verbal accusation that sounds compelling on its own, but requires knowing who a background character is for full emotional payoff.
3. **Action Continuity Across Scene Boundaries**: The current candidate window evaluates single continuous scenes. Multi-scene cuts require stitching logic to ensure visual continuity.
