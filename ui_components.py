"""
ui_components.py - Reusable UI component builders for Personal Finance Dashboard V2
Includes top navbar, KPI cards, AI insight cards, progress indicators, and Plotly theme styling.
"""

import streamlit as st
import plotly.graph_objects as go
from styles import CSS_STYLES

# Primary Fintech Color Palette Constants
COLOR_BG_MAIN = "#121417"
COLOR_BG_SURFACE = "#1B1F24"
COLOR_BG_CARD = "#22272E"
COLOR_BORDER = "#2F3742"
COLOR_PRIMARY_TEAL = "#0F766E"
COLOR_ACCENT_TEAL = "#14B8A6"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_SECONDARY = "#94A3B8"
COLOR_GREEN = "#22C55E"
COLOR_RED = "#EF4444"
COLOR_AMBER = "#F59E0B"
COLOR_BLUE = "#3B82F6"


def apply_custom_css():
    """Injects the custom Deep Teal & Charcoal CSS into Streamlit."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def render_top_navbar(active_page: str):
    """
    Renders a modern, horizontal top navbar for navigation across 5 primary views.
    Preserves navigation state via st.session_state.
    """
    pages = ["Dashboard", "Analytics", "Transactions", "AI Insights", "Settings"]
    
    # Top Bar Header
    col_brand, col_nav = st.columns([1.2, 3.8])

    with col_brand:
        st.markdown(
            """
            <div class="topnav-brand" style="padding-top: 4px;">
                <div class="topnav-logo">⚡</div>
                <div>
                    <div class="topnav-title">FINTRACK AI</div>
                    <div class="topnav-subtitle">Smart Personal Finance</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_nav:
        n_cols = st.columns(len(pages))
        for idx, p in enumerate(pages):
            is_active = (p == active_page)
            btn_class = "nav-btn-active" if is_active else "nav-btn"
            
            with n_cols[idx]:
                st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                if st.button(p, key=f"topnav_{p}", use_container_width=True):
                    if st.session_state.get("current_page") != p:
                        st.session_state["current_page"] = p
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #2F3742; margin-top: 12px; margin-bottom: 24px;'>", unsafe_allow_html=True)


def render_welcome_header(title: str, subtitle: str, badge_text: str = None):
    """Renders a modern top banner with title, subtitle, and optional status badge."""
    badge_html = f'<div class="welcome-pill">{badge_text}</div>' if badge_text else ""
    st.markdown(
        f"""
        <div class="welcome-banner">
            <div>
                <h1 class="welcome-title">{title}</h1>
                <p class="welcome-sub">{subtitle}</p>
            </div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(title: str, value: str, subtext: str = None, delta: str = None, delta_type: str = "positive", icon: str = None):
    """
    Renders a premium fintech KPI metric card.
    delta_type options: 'positive', 'negative', 'warning', 'neutral'
    """
    badge_class = f"badge-{delta_type}"
    badge_html = f'<span class="fin-card-badge {badge_class}">{delta}</span>' if delta else ""
    sub_html = f'<div class="fin-card-sub">{subtext}</div>' if subtext else ""
    icon_html = f'<div class="fin-card-icon">{icon}</div>' if icon else ""
    
    card_html = f'<div class="fin-card"><div class="fin-card-header"><span class="fin-card-title">{title}</span>{icon_html}</div><div class="fin-card-value">{value}</div><div style="display: flex; justify-content: space-between; align-items: center;">{sub_html}{badge_html}</div></div>'
    st.markdown(card_html, unsafe_allow_html=True)


def render_insight_card(title: str, message: str, tag_type: str = "info", icon: str = "💡"):
    """Renders an executive financial recommendation card."""
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-icon">{icon}</div>
            <div class="insight-content">
                <div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC; margin-bottom: 2px;">{title}</div>
                <div class="insight-text">{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_bar(pct: float, color: str = COLOR_ACCENT_TEAL, label: str = None):
    """Renders a sleek custom HTML progress bar with optional text label."""
    clamped_pct = max(0, min(100, pct))
    label_html = f'<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #94A3B8; margin-bottom: 4px;"><span>{label}</span><span>{pct:.1f}%</span></div>' if label else ""
    
    st.markdown(
        f"""
        {label_html}
        <div class="fin-progress-bg">
            <div class="fin-progress-fill" style="width: {clamped_pct}%; background-color: {color};"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_plotly_theme(fig: go.Figure) -> go.Figure:
    """
    Applies custom Deep Teal & Charcoal design system styling to any Plotly chart.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLOR_TEXT_PRIMARY, size=12),
        margin=dict(t=30, l=10, r=10, b=10),
        xaxis=dict(
            gridcolor=COLOR_BORDER,
            zerolinecolor=COLOR_BORDER,
            tickfont=dict(color=COLOR_TEXT_SECONDARY),
            title_font=dict(color=COLOR_TEXT_SECONDARY),
        ),
        yaxis=dict(
            gridcolor=COLOR_BORDER,
            zerolinecolor=COLOR_BORDER,
            tickfont=dict(color=COLOR_TEXT_SECONDARY),
            title_font=dict(color=COLOR_TEXT_SECONDARY),
        ),
        legend=dict(
            bgcolor="rgba(27, 31, 36, 0.7)",
            bordercolor=COLOR_BORDER,
            borderwidth=1,
            font=dict(color=COLOR_TEXT_PRIMARY),
        ),
        hoverlabel=dict(
            bgcolor=COLOR_BG_CARD,
            bordercolor=COLOR_ACCENT_TEAL,
            font=dict(color=COLOR_TEXT_PRIMARY, family="Inter"),
        ),
    )
    return fig
