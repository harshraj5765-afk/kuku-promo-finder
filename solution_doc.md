# Solution Document: Microdrama Promo Finder (Problem 1)

## 1. Problem Choice, Framing & Assumptions
Microdramas (1-2 min episodes) depend on short-form organic acquisition (TikTok, Reels, Shorts)[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span). Today, editors manually scour 50+ episodes to identify promotional cuts[span_15](start_span)[span_15](end_span).

### Scoping & Core Heuristics:
1. **0-3s Hook Window**: Detects immediate disruption (physical slaps, verbal confrontations, dramatic camera cuts)[span_16](start_span)[span_16](end_span).
2. **Terminal Cliffhanger**: Pinpoints narrative drop-offs (unresolved questions, gasps, sound swell peaks)[span_17](start_span)[span_17](end_span).
3. **Strict Duration Bounds**: Constrains clips to 20 <= Delta t <= 60 seconds[span_18](start_span)[span_18](end_span).

### Working Assumptions:
- Single-scene continuous cuts preserve narrative pacing and coherence best without disorienting cuts across scenes[span_19](start_span)[span_19](end_span).
- Timestamp accuracy in the screenplay text is ground truth[span_20](start_span)[span_20](end_span).

## 2. Code vs. AI Trade-Offs & Workflow
- **Deterministic Code Engine (Python/Regex)**:
  Screenplay tokenization and duration windowing are handled entirely by deterministic code. Parsing 50 episodes runs locally in <2 seconds at $0 cost.
- **AI Tool Usage & Failure Reflection**:
  LLMs (Gemini / Claude) assisted in prototyping lexical scoring patterns and Streamlit UI code. 
  *Where AI got it wrong*: The LLM initially attempted to slice screenplays across loose paragraph breaks, ignoring sub-second dialogue timestamps and hallucinating clip durations longer than 60 seconds. This confirmed that mathematical sliding windows must remain strictly in code.

## 3. Real-World Economics & Swappable Architecture
- **Production Cost**: Standard pipeline runs locally with zero API overhead. 
- **Swappable Architecture**: Candidate scoring in `src/detector.py` is decoupled from windowing. In production, vision-language or embedding APIs can be swapped into candidate scoring without altering core logic.

## 4. Quality Checking & Failure Analysis
- **Successes**: Accurately extracts high-stakes confrontations (e.g., wedding altar abandonment in Ep 1-2, garden confrontations)[span_21](start_span)[span_21](end_span).
- **Known Failure Modes**:
  1. Subtle dramatic tension spoken quietly receives lower heuristic weights than overt physical actions.
  2. Background character context: strong standalone dialogue lines occasionally require prior episode context.
