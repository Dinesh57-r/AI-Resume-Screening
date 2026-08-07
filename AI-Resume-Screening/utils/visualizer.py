"""
visualizer.py – Plotly chart factory for the AI Resume Screening dashboard.
"""
from typing import List, Dict, Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ── Colour palette ─────────────────────────────────────────────────────────────
ACCENT_GRADIENT = ["#6366f1", "#8b5cf6", "#a855f7", "#c084fc", "#d946ef"]
TIER_COLORS = {
    "🏆 Excellent": "#22c55e",
    "✅ Good": "#3b82f6",
    "⚠️ Average": "#f59e0b",
    "❌ Below Average": "#ef4444",
}
BG_COLOR = "rgba(0,0,0,0)"
PAPER_COLOR = "rgba(0,0,0,0)"
FONT_COLOR = "#e2e8f0"
GRID_COLOR = "rgba(255,255,255,0.08)"


def _base_layout(title: str = "") -> Dict:
    """Common Plotly layout settings for dark theme."""
    return dict(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=16)),
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
    )


def score_bar_chart(candidates: List[Dict[str, Any]]) -> go.Figure:
    """Horizontal bar chart of candidate scores, colour-coded by tier."""
    df = pd.DataFrame(
        [
            {
                "Name": c.get("name", c["filename"]),
                "Score (%)": c["percentage_score"],
                "Tier": c.get("tier_label", ""),
            }
            for c in candidates
        ]
    ).sort_values("Score (%)", ascending=True)

    colors = [TIER_COLORS.get(t, "#6366f1") for t in df["Tier"]]

    fig = go.Figure(
        go.Bar(
            x=df["Score (%)"],
            y=df["Name"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=df["Score (%)"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout("Candidate Ranking"),
        xaxis=dict(
            title="Match Score (%)",
            range=[0, 105],
            showgrid=True,
            gridcolor=GRID_COLOR,
        ),
        yaxis=dict(showgrid=False),
        height=max(300, 50 * len(candidates)),
    )
    return fig


def score_distribution(candidates: List[Dict[str, Any]]) -> go.Figure:
    """Histogram showing score distribution across all candidates."""
    scores = [c["percentage_score"] for c in candidates]
    fig = go.Figure(
        go.Histogram(
            x=scores,
            nbinsx=10,
            marker=dict(
                color=ACCENT_GRADIENT[0],
                line=dict(color=ACCENT_GRADIENT[2], width=1),
            ),
            hovertemplate="Score: %{x:.0f}%<br>Count: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout("Score Distribution"),
        xaxis=dict(title="Score (%)", showgrid=True, gridcolor=GRID_COLOR),
        yaxis=dict(title="# Candidates", showgrid=True, gridcolor=GRID_COLOR),
    )
    return fig


def skill_frequency_chart(candidates: List[Dict[str, Any]], top_n: int = 20) -> go.Figure:
    """Bar chart of the most common skills across all resumes."""
    from collections import Counter

    all_skills = []
    for c in candidates:
        all_skills.extend(c.get("skills", []))

    if not all_skills:
        fig = go.Figure()
        fig.update_layout(**_base_layout("No skills found"))
        return fig

    counter = Counter(all_skills)
    top = counter.most_common(top_n)
    skills, counts = zip(*top)

    fig = go.Figure(
        go.Bar(
            x=list(skills),
            y=list(counts),
            marker=dict(
                color=list(counts),
                colorscale="Purp",
                showscale=False,
            ),
            hovertemplate="<b>%{x}</b><br>Mentions: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(f"Top {top_n} Skills Across All Resumes"),
        xaxis=dict(tickangle=-35, showgrid=False),
        yaxis=dict(title="Frequency", showgrid=True, gridcolor=GRID_COLOR),
        height=400,
    )
    return fig


def skill_gap_sunburst(candidate: Dict[str, Any]) -> go.Figure:
    """Sunburst chart for matched vs missing skills of a single candidate."""
    matched = candidate.get("matched_skills", [])
    missing = candidate.get("missing_skills", [])

    labels = ["Skills"] + [f"✓ {s}" for s in matched] + [f"✗ {s}" for s in missing]
    parents = [""] + ["Matched"] * len(matched) + ["Missing"] * len(missing)

    if matched:
        labels.insert(1, "Matched")
        parents.insert(1, "Skills")
    if missing:
        labels.append("Missing")
        parents.append("Skills")

    # Recompute properly
    labels = ["Skills"]
    parents = [""]
    values = [len(matched) + len(missing)]

    if matched:
        labels.append("Matched")
        parents.append("Skills")
        values.append(len(matched))
        for s in matched:
            labels.append(s)
            parents.append("Matched")
            values.append(1)

    if missing:
        labels.append("Missing")
        parents.append("Skills")
        values.append(len(missing))
        for s in missing:
            labels.append(s)
            parents.append("Missing")
            values.append(1)

    colors_map = {"Matched": "#22c55e", "Missing": "#ef4444", "Skills": "#6366f1"}
    item_colors = []
    for lbl, par in zip(labels, parents):
        if lbl in colors_map:
            item_colors.append(colors_map[lbl])
        elif par == "Matched":
            item_colors.append("#4ade80")
        elif par == "Missing":
            item_colors.append("#f87171")
        else:
            item_colors.append("#818cf8")

    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=item_colors),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
            branchvalues="total",
        )
    )
    fig.update_layout(
        **_base_layout("Skill Gap Analysis"),
        height=420,
    )
    return fig


def radar_chart(candidates: List[Dict[str, Any]], top_n: int = 5) -> go.Figure:
    """Radar chart comparing top N candidates across scoring dimensions."""
    top = candidates[:top_n]
    categories = ["TF-IDF Match", "Skill Match", "Experience", "Overall"]

    fig = go.Figure()
    for c in top:
        name = c.get("name", c["filename"])
        values = [
            c.get("tfidf_score", 0) * 100,
            c.get("skill_score", 0) * 100,
            c.get("experience_score", 0) * 100,
            c.get("percentage_score", 0),
        ]
        # Close the radar loop
        values_closed = values + [values[0]]
        cats_closed = categories + [categories[0]]

        fig.add_trace(
            go.Scatterpolar(
                r=values_closed,
                theta=cats_closed,
                fill="toself",
                name=name,
                opacity=0.75,
            )
        )

    fig.update_layout(
        **_base_layout("Top Candidates — Radar Comparison"),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showgrid=True,
                gridcolor=GRID_COLOR,
                tickfont=dict(color=FONT_COLOR),
            ),
            angularaxis=dict(tickfont=dict(color=FONT_COLOR)),
            bgcolor=BG_COLOR,
        ),
        showlegend=True,
        legend=dict(font=dict(color=FONT_COLOR)),
        height=450,
    )
    return fig


def experience_distribution(candidates: List[Dict[str, Any]]) -> go.Figure:
    """Pie chart of experience buckets."""
    from collections import Counter

    buckets = []
    for c in candidates:
        yrs = c.get("experience_years", 0)
        if yrs == 0:
            buckets.append("Not Specified")
        elif yrs <= 1:
            buckets.append("0–1 yr")
        elif yrs <= 3:
            buckets.append("1–3 yrs")
        elif yrs <= 5:
            buckets.append("3–5 yrs")
        elif yrs <= 8:
            buckets.append("5–8 yrs")
        else:
            buckets.append("8+ yrs")

    counter = Counter(buckets)
    fig = go.Figure(
        go.Pie(
            labels=list(counter.keys()),
            values=list(counter.values()),
            hole=0.45,
            marker=dict(colors=ACCENT_GRADIENT),
            textfont=dict(color="#fff"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
        )
    )
    fig.update_layout(**_base_layout("Experience Distribution"), height=350)
    return fig
