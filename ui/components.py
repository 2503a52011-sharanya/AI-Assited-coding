import streamlit as st
from typing import Optional

def render_hero():
    """Renders the top SaaS hero banner."""
    st.markdown("""
    <div class="hero-container">
        <div style="text-transform: uppercase; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.12em; color: #F97316; margin-bottom: 0.5rem;">
            ✦ NEXT-GEN INTELLIGENT TRAVEL ARCHITECTURE
        </div>
        <div class="hero-tagline">
            Your Journey. Your Interests. <span>Your AI-Powered Trip.</span>
        </div>
        <div class="hero-subtitle">
            Plan smarter. Travel better. Stay within your budget. Discover hyper-personalized itineraries, dynamic hotel and dining discovery, real-time routing, and automated budget optimization.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(label: str, value: str, subtext: str = ""):
    """Renders modern glassmorphism KPI card."""
    sub_html = f'<div class="kpi-sub">{subtext}</div>' if subtext else ''
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str):
    """Renders colored pill for booking statuses."""
    s_lower = status.lower()
    if s_lower == "confirmed":
        return '<span class="status-confirmed">● Confirmed</span>'
    elif s_lower == "pending":
        return '<span class="status-pending">◐ Pending</span>'
    elif s_lower == "rejected":
        return '<span class="status-rejected">✕ Rejected</span>'
    elif s_lower == "cancelled":
        return '<span class="status-rejected">○ Cancelled</span>'
    return f'<span>{status}</span>'

def render_demo_badge(message: str = "Demo Mode — Live API data is unavailable."):
    st.markdown(f'<div class="badge-demo">⚠️ {message}</div>', unsafe_allow_html=True)

def render_ai_badge(message: str = "AI-Powered Intelligence Active"):
    st.markdown(f'<div class="badge-ai">✨ {message}</div>', unsafe_allow_html=True)

def render_section_header(title: str, subtitle: Optional[str] = None):
    sub_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ''
    st.markdown(f"""
    <div style="margin-top: 1.2rem; margin-bottom: 0.8rem;">
        <h2 class="section-title">{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)
