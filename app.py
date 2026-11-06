import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kuku Promo Finder", layout="wide")
st.title("🎬 Microdrama Promo Finder")
st.caption("Automated extraction of 20–60s promotional clips based on Hook & Cliffhanger scoring")

csv_path = "data/outputs/ranked_promos.csv"

if not os.path.exists(csv_path):
    st.error("No outputs found. Please run: python3 -m src.pipeline")
else:
    df = pd.read_csv(csv_path)

    # Sidebar controls
    st.sidebar.header("Filter Candidates")
    episodes = sorted(df["episode"].unique().tolist())
    selected_ep = st.sidebar.selectbox("Filter by Episode", ["All"] + episodes)
    
    min_score = st.sidebar.slider("Minimum Composite Score", float(df["overall_score"].min()), float(df["overall_score"].max()), float(df["overall_score"].min()))
    dur_range = st.sidebar.slider("Duration (seconds)", 20.0, 60.0, (20.0, 60.0))

    # Apply filters
    filtered_df = df[(df["overall_score"] >= min_score) & (df["duration_sec"] >= dur_range[0]) & (df["duration_sec"] <= dur_range[1])]
    if selected_ep != "All":
        filtered_df = filtered_df[filtered_df["episode"] == selected_ep]

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Promos Found", len(df))
    col2.metric("Filtered Promos", len(filtered_df))
    col3.metric("Top Score", f"{df['overall_score'].max():.1f}")

    st.subheader("Top Ranked Promotional Cuts")
    
    for idx, row in filtered_df.head(10).reset_index().iterrows():
        with st.expander(f"⭐ Rank #{idx+1} | Episode {row['episode']} (Scene {row['scene']}) | Duration: {row['duration_sec']}s | Score: {row['overall_score']}"):
            st.markdown(f"**⏱️ Window:** `{row['start_time']}s` to `{row['end_time']}s`")
            st.markdown(f"**🎣 Hook (First 3s):** {row['hook']} *(Score: {row['hook_score']}/5.0)*")
            st.markdown(f"**✂️ Cliffhanger (Last 5s):** {row['cliffhanger']} *(Score: {row['cliffhanger_score']}/5.0)*")
            st.info(f"**Why it works:** {row['why_it_works']}")

    # Raw Data Table
    st.subheader("Raw Outputs Table")
    st.dataframe(filtered_df, use_container_width=True)
