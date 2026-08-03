"""
styles.py - Custom CSS styling for Personal Finance Dashboard V2
Implements a modern, premium Deep Teal & Charcoal design system inspired by Revolut & Wise.
"""

CSS_STYLES = """
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Color Variables & Root Theme */
:root {
    --bg-main: #121417;
    --bg-surface: #1B1F24;
    --bg-card: #22272E;
    --bg-card-hover: #2A3038;
    --border-color: #2F3742;
    --primary-teal: #0F766E;
    --accent-teal: #14B8A6;
    --accent-light: #2DD4BF;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --positive-green: #22C55E;
    --warning-amber: #F59E0B;
    --negative-red: #EF4444;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.25);
    --shadow-glow: 0 0 15px rgba(20, 184, 166, 0.15);
}

/* Global App Styling */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Hide Sidebar since we use Top Navigation */
[data-testid="stSidebar"] {
    display: none !important;
}

/* Top Navigation Bar Container */
.topnav-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 10px 20px;
    margin-bottom: 28px;
    box-shadow: var(--shadow-subtle);
}

.topnav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.topnav-logo {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--primary-teal), var(--accent-teal));
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: var(--shadow-glow);
}

.topnav-title {
    font-weight: 800;
    font-size: 1.15rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.topnav-subtitle {
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-weight: 500;
}

/* Modern Top Navigation Buttons Container */
.topnav-menu {
    display: flex;
    gap: 8px;
    align-items: center;
}

/* Styling Streamlit Buttons inside Top Nav */
div[data-testid="stHorizontalBlock"] .nav-btn button {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius-md) !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="stHorizontalBlock"] .nav-btn button:hover {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}

div[data-testid="stHorizontalBlock"] .nav-btn-active button {
    background: linear-gradient(135deg, rgba(15, 118, 110, 0.3), rgba(20, 184, 166, 0.2)) !important;
    color: var(--accent-teal) !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: var(--radius-md) !important;
    padding: 8px 16px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    box-shadow: var(--shadow-glow) !important;
}

/* Custom Card Container */
.fin-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 22px 24px;
    margin-bottom: 18px;
    transition: all 0.2s ease-in-out;
    box-shadow: var(--shadow-subtle);
}

.fin-card:hover {
    border-color: rgba(20, 184, 166, 0.4);
}

.fin-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.fin-card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.fin-card-icon {
    width: 38px;
    height: 38px;
    border-radius: var(--radius-md);
    background: rgba(47, 55, 66, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}

.fin-card-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    margin-bottom: 6px;
}

.fin-card-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.fin-card-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}

.badge-positive {
    background: rgba(34, 197, 94, 0.15);
    color: var(--positive-green);
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.badge-negative {
    background: rgba(239, 68, 68, 0.15);
    color: var(--negative-red);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-neutral {
    background: rgba(148, 163, 184, 0.15);
    color: var(--text-secondary);
    border: 1px solid rgba(148, 163, 184, 0.3);
}

.badge-warning {
    background: rgba(245, 158, 11, 0.15);
    color: var(--warning-amber);
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Page Header & Welcome Banner */
.welcome-banner {
    background: linear-gradient(135deg, #1B262C 0%, #121E23 100%);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--accent-teal);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.welcome-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}

.welcome-sub {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin: 0;
}

.welcome-pill {
    background: rgba(20, 184, 166, 0.12);
    border: 1px solid var(--accent-teal);
    color: var(--accent-teal);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
}

/* Insight Card Styling */
.insight-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: all 0.2s ease;
}

.insight-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--accent-teal);
}

.insight-icon {
    font-size: 1.25rem;
    padding: 8px;
    border-radius: var(--radius-sm);
    background: rgba(20, 184, 166, 0.1);
    color: var(--accent-teal);
}

.insight-content {
    flex: 1;
}

.insight-text {
    font-size: 0.92rem;
    color: var(--text-primary);
    font-weight: 500;
    line-height: 1.5;
}

/* Custom Streamlit Input & Widget Overrides */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
}

div[data-baseweb="input"]:focus-within > div,
div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 1px var(--accent-teal) !important;
}

/* Button Overrides */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary-teal), #0D6961) !important;
    color: #F8FAFC !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 2px 10px rgba(15, 118, 110, 0.2) !important;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, #14B8A6, var(--primary-teal)) !important;
    box-shadow: var(--shadow-glow) !important;
    transform: translateY(-1px) !important;
}

/* Streamlit Tabs Overrides */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    color: var(--text-secondary) !important;
    padding: 8px 16px;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: var(--primary-teal) !important;
    color: #FFFFFF !important;
}

/* Custom Progress Bar Track */
.fin-progress-bg {
    background-color: var(--border-color);
    border-radius: 10px;
    height: 10px;
    width: 100%;
    overflow: hidden;
    margin: 8px 0;
}

.fin-progress-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.4s ease;
}

/* Table Wrapper */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    background-color: var(--bg-card) !important;
    overflow: hidden;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: var(--bg-main);
}
::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent-teal);
}
</style>
"""
