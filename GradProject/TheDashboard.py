import streamlit as st
import pandas as pd
import plotly.express as px
from TheModel import run_analysis

st.set_page_config(
    page_title="Temporal Sentiment Analysis for YouTube Highlights",
    layout="wide"
)

# =========================================================
# CUSTOM THEME
# =========================================================

st.markdown("""
<style>

/* =========================
   MAIN BACKGROUND
========================= */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1E1B4B 50%,
        #0F172A 100%
    );
}

/* =========================
   FONT
========================= */
html, body, [class*="css"]{
    font-family: "Georgia", serif;
}

/* =========================
   HEADINGS
========================= */
h1{
    color:#FFFFFF !important;
    font-weight:700 !important;
}

h2{
    color:#F8FAFC !important;
    font-weight:700 !important;
}

h3{
    color:#F1F5F9 !important;
    font-weight:700 !important;
}

/* Executive KPIs / Section Titles */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3{
    color:#F8FAFC !important;
}

/* =========================
   GENERAL TEXT
========================= */
p, span, label, div{
    color:#E5E7EB;
}

/* =========================
   INPUT LABEL
========================= */
label{
    color:#FFFFFF !important;
    font-weight:600 !important;
}

/* =========================
   VIDEO ID INPUT BOX
========================= */
.stTextInput input{
    background-color:#F8FAFC !important;
    color:#6B7280 !important;
    border-radius:10px;
    border:1px solid #CBD5E1 !important;
    font-weight:600;
}

/* Placeholder text */
.stTextInput input::placeholder{
    color:#9CA3AF !important;
}

/* =========================
   KPI CARDS
========================= */
[data-testid="metric-container"]{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px;
    padding:18px;
    backdrop-filter: blur(10px);
}

/* KPI Labels */
[data-testid="metric-container"] label{
    color:#E2E8F0 !important;
}

/* KPI Values */
[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#FFFFFF !important;
}

/* =========================
   TABLES
========================= */
[data-testid="stDataFrame"]{
    background-color:rgba(255,255,255,0.04);
    border-radius:12px;
}

/* =========================
   BUTTON
========================= */
.stButton button{
    background-color:#7F1D1D;
    color:white;
    border:none;
    border-radius:10px;
    height:42px;
    font-weight:600;
}

.stButton button:hover{
    background-color:#991B1B;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("Temporal Sentiment Analysis for YouTube Highlights")

# =========================================================
# VIDEO INPUT + BUTTON SAME ROW
# =========================================================

input_col, button_col = st.columns([5,1])

with input_col:
    video_id = st.text_input(
        "YouTube Video ID",
        value="f_lRdkH_QoY"
    )

with button_col:
    st.write("")
    st.write("")

    analyze = st.button(
        "Analyze",
        use_container_width=True
    )

# =========================================================
# RUN MODEL
# =========================================================

if analyze:

    with st.spinner("Analyzing Audience Reactions..."):

        df_raw,df_cleaned,df_model,peak_data,timestamp_counts = run_analysis(video_id)

    total_comments = len(df_raw)
    timestamp_comments = len(df_model)

    positive_pct = round(
        (df_model["label"].eq("positive").sum()/len(df_model))*100,
        1
    )

    negative_pct = round(
        (df_model["label"].eq("negative").sum()/len(df_model))*100,
        1
    )

    avg_confidence = round(
        df_model["confidence"].mean()*100,
        1
    )

    top_peak = peak_data.iloc[0]


    timeline = df_model.groupby("segment").agg(
        comments=("comment","count"),
        sentiment=("sentiment_score","mean"),
        likes=("likes","sum")
    ).reset_index()

    sentiment_timeline = (
        df_model
        .groupby(["segment", "label"])
        .size()
        .reset_index(name="count")
    )

    total_per_segment = (
        sentiment_timeline
        .groupby("segment")["count"]
        .transform("sum")
    )

    sentiment_timeline["percentage"] = (
        sentiment_timeline["count"]
        / total_per_segment
    ) * 100

    sentiment_counts = (
        df_model["label"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Count"
    ]

    # =====================================================
    # KPI SECTION
    # =====================================================

    st.subheader("Executive KPIs")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(
        "Comments",
        f"{total_comments:,}"
    )

    c2.metric(
        "Timestamp Mentions",
        f"{timestamp_comments:,}"
    )

    c3.metric(
        "Positive",
        f"{positive_pct}%"
    )

    c4.metric(
        "Negative",
        f"{negative_pct}%"
    )

    c5.metric(
        "Confidence",
        f"{avg_confidence}%"
    )

    st.divider()

    # =====================================================
    # ATTENTION TIMELINE
    # =====================================================

    left,right = st.columns([3,1])

    with left:

        fig=px.line(
            timeline,
            x="segment",
            y="comments",
            markers=True,
            title="Audience Attention Timeline"
        )

        fig.update_traces(
            line_color="#800020",
            line_width=4
        )

        fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
            family="Georgia",
            color="white",
            size=14
            ),

            title_font=dict(
            color="white",
            size=22
            ),

            legend=dict(
                font=dict(
                color="white",
                size=13
                )
            ),

            xaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),

            yaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🥇 Golden Moment")

        st.metric(
            "Top Segment",
            top_peak["time_range"]
        )

        st.metric(
            "Peak Score",
            int(top_peak["peak_score"])
        )

        st.metric(
            "Avg Sentiment",
            round(top_peak["avg_sentiment"],2)
        )

    st.divider()

    # =====================================================
    # PEAKS + SENTIMENT
    # =====================================================

    col1,col2 = st.columns(2)

    with col1:

        fig=px.bar(
            peak_data.head(10),
            y="time_range",
            x="peak_score",
            orientation="h",
            color="peak_score",
            color_continuous_scale=[
                "#5B3A82",
                "#800020",
                "#D4AF37"
         ],
            title="Top Video Moments"
        )

        fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
            family="Georgia",
            color="white",
            size=14
            ),

            title_font=dict(
            color="white",
            size=22
            ),

            legend=dict(
                font=dict(
                color="white",
                size=13
                )
            ),

            xaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),

            yaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        fig=px.pie(
            sentiment_counts,
             names="Sentiment",
            values="Count",
            hole=.65,
            title="Sentiment Distribution",
            color="Sentiment",
            color_discrete_map={
                "positive":"#16A34A",
                "neutral":"#94A3B8",
                "negative":"#DC2626"
         }
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                family="Georgia",
                color="white",
                size=14
                ),

                title_font=dict(
                color="white",
                size=22
                ),

                legend=dict(
                    font=dict(
                    color="white",
                    size=13
                    )
                ),

                xaxis=dict(
                    title_font=dict(color="white"),
                    tickfont=dict(color="white")
                ),

                yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
                )
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

    # =====================================================
    # SENTIMENT + ENGAGEMENT
    # =====================================================

    col3,col4 = st.columns([3,1])

    with col3:

        fig=px.line(
             timeline,
             x="segment",
             y="sentiment",
             markers=True,
            title="Sentiment Over Time"
        )

        fig.update_traces(
            line_color="#9E1B34",
            line_width=2
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                family="Georgia",
                color="white",
                size=14
                ),

                title_font=dict(
                color="white",
                size=22
                ),

                legend=dict(
                    font=dict(
                    color="white",
                    size=13
                    )
                ),

                xaxis=dict(
                    title_font=dict(color="white"),
                    tickfont=dict(color="white")
                ),

                yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
                )
            )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col4:

        fig = px.histogram(
            df_model,
            x="confidence",
            nbins=20,
            title="Model Confidence Distribution",
            color_discrete_sequence=["#800020"]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Georgia",
                color="white",
                size=14
            ),
            title_font=dict(
                color="white",
                size=22
            ),
            legend=dict(
                font=dict(
                    color="white",
                    size=13
                )
            ),
            xaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),
            yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()

    # =====================================================
    # TIMESTAMPS + CONFIDENCE
    # =====================================================



    col5, col6 = st.columns(2)

    with col5:

        fig = px.bar(
            timestamp_counts.reset_index(),
            x="count",
            y="timestamp",
            orientation="h",
            title="Most Referenced Timestamps",
            color="count",
            color_continuous_scale=[
            "#5B3A82",
            "#800020",
            "#D4AF37"
         ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Georgia",
                color="white",
                size=14
            ),
            title_font=dict(
                color="white",
                size=22
            ),
            legend=dict(
                font=dict(
                    color="white",
                    size=13
                )
            ),
            xaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),
            yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col6:

        impact_df=df_model[
        df_model["weight"]>df_model["weight"].quantile(0.9)
        ].copy()

        impact_df["bubble_size"]=impact_df["weight"]**0.5

        fig=px.scatter(
            df_model,
            x="likes",
            y="replies",
            size="weight",
            color="label",
            hover_data=["timestamp"],
            title="Likes vs Replies Impact",
            color_discrete_map={
                "positive":"#22C55E",
                "neutral":"#CBD5E1",
                "negative":"#EF4444"
            }
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                family="Georgia",
                color="white",
                size=14
                ),

                title_font=dict(
                color="white",
                size=22
                ),

                legend=dict(
                    font=dict(
                    color="white",
                    size=13
                    )
                ),

                xaxis=dict(
                    title_font=dict(color="white"),
                    tickfont=dict(color="white")
                ),

                yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
                )
            )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # GOLDEN MOMENTS TABLE
    # =====================================================

    st.divider()

    st.subheader("🏆 Golden Moments Ranking")

    ranking = peak_data.head(10).copy()

    medals = ["🥇", "🥈", "🥉"]

    ranking["Rank"] = [
    medals[i] if i < 3 else f"#{i+1}"
    for i in range(len(ranking))
    ]

    st.dataframe(
        ranking[
            [
            "Rank",
            "time_range",
            "comment_count",
            "total_likes",
            "total_replies",
            "avg_sentiment",
            "peak_score"
        ]
    ],
    use_container_width=True
    )

    # =====================================================
    # TOP COMMENTS
    # =====================================================

    st.subheader("💬 Most Influential Comments")

    top_comments = df_model.sort_values(
        by=["weight", "confidence"],
        ascending=False
    )[[
        "timestamp",
        "comment",
        "label",
        "likes",
        "replies",
        "confidence"
    ]].head(20)

    st.dataframe(
        top_comments,
        use_container_width=True
    )