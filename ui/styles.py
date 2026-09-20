def get_custom_css() -> str:
    """
    Global CSS rules guaranteeing 100% text visibility across all pages,
    cards, containers, tabs, and modals in both dark and light contexts.
    """
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');

    /* Global Body and Streamlit Base Container */
    body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0B0F19 !important;
        color: #CBD5E1 !important;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1280px !important;
    }

    /* =========================================================================
       1. GLOBAL HEADING VISIBILITY (ALL HEADINGS ON DARK BACKGROUNDS)
       ========================================================================= */

    /* H1 / Main Page Titles */
    h1,
    h1 *,
    .page-title,
    .page-title *,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h1 *,
    [data-testid="stHeadingWithActionElements"] h1,
    [data-testid="stHeadingWithActionElements"] h1 * {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        color: #FFFFFF !important; /* Pure Crisp White */
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5) !important;
        text-decoration: none !important;
    }

    /* H2 / Section Headings */
    h2,
    h2 *,
    .section-title,
    .section-title *,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h2 *,
    [data-testid="stHeadingWithActionElements"] h2,
    [data-testid="stHeadingWithActionElements"] h2 * {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #F8FAFC !important; /* Crisp Ivory White */
        text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4) !important;
        text-decoration: none !important;
    }

    /* H3 / Subheadings */
    h3,
    h3 *,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h3 *,
    [data-testid="stHeadingWithActionElements"] h3,
    [data-testid="stHeadingWithActionElements"] h3 * {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #E2E8F0 !important; /* Light Slate */
        text-decoration: none !important;
    }

    /* H4, H5, H6 / Minor & Accent Headings */
    h4, h4 *,
    h5, h5 *,
    h6, h6 *,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h4 *,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h5 *,
    [data-testid="stMarkdownContainer"] h6,
    [data-testid="stMarkdownContainer"] h6 *,
    [data-testid="stHeadingWithActionElements"] h4,
    [data-testid="stHeadingWithActionElements"] h4 * {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #38BDF8 !important; /* Accent Radiant Sky Blue */
        text-decoration: none !important;
    }

    /* =========================================================================
       2. BODY, LABELS, PARAGRAPHS, AND LISTS
       ========================================================================= */

    p, span, li, label, div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li {
        color: #CBD5E1; /* Normal body text */
        line-height: 1.6;
    }

    /* Form and Widget Labels */
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] {
        color: #E2E8F0 !important; /* High contrast widget label */
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Secondary / Muted Text */
    .page-subtitle,
    .section-subtitle,
    p.page-subtitle,
    p.section-subtitle,
    .text-muted,
    small {
        color: #94A3B8 !important; /* Secondary / Muted Text */
        font-size: 1.0rem !important;
        line-height: 1.5 !important;
    }

    /* Anchor and Links */
    a[data-testid="stHeaderActionElements"],
    .stMarkdown a,
    h1 a, h2 a, h3 a, h4 a {
        color: #38BDF8 !important;
        text-decoration: none !important;
    }

    /* =========================================================================
       3. DARK CARDS (High-Contrast, Light Headings, Clear Labels)
       ========================================================================= */

    .kpi-card {
        background: #131B2E !important;
        border: 1px solid #23324F !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.4rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
        min-height: 115px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    .kpi-card:hover {
        transform: translateY(-2px) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 12px 25px rgba(56, 189, 248, 0.2) !important;
    }
    .kpi-label {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #94A3B8 !important; /* Secondary / Muted */
        margin-bottom: 0.35rem !important;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important; /* Main page heading color */
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        line-height: 1.2 !important;
    }
    .kpi-sub {
        font-size: 0.82rem !important;
        color: #2DD4BF !important; /* Vibrant mint teal */
        font-weight: 600 !important;
        margin-top: 0.35rem !important;
        white-space: nowrap !important;
    }

    /* Travel Listing Cards */
    .travel-card {
        background: #131B2E !important;
        border: 1px solid #23324F !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.25s ease !important;
    }
    .travel-card:hover {
        border-color: #38BDF8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.4) !important;
    }
    .travel-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .travel-card-body {
        padding: 1.25rem !important;
        color: #CBD5E1 !important;
    }
    .travel-card-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important; /* Crisp White Heading */
        margin-bottom: 0.4rem !important;
    }
    .travel-card-subtitle {
        font-size: 0.9rem !important;
        color: #94A3B8 !important; /* Muted */
        margin-bottom: 0.75rem !important;
    }
    .travel-card-price {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #FB923C !important; /* Accent Amber */
    }

    /* Timeline Day Box */
    .timeline-day {
        background: #131B2E !important;
        border-left: 4px solid #2DD4BF !important;
        border-top: 1px solid #23324F !important;
        border-right: 1px solid #23324F !important;
        border-bottom: 1px solid #23324F !important;
        border-radius: 0 14px 14px 0 !important;
        padding: 1.25rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
        color: #FFFFFF !important;
    }
    .timeline-period {
        background: #0B0F19 !important;
        border-radius: 10px !important;
        padding: 0.85rem 1rem !important;
        margin-top: 0.6rem !important;
        border: 1px solid #1E293B !important;
        color: #CBD5E1 !important;
    }

    /* =========================================================================
       4. LIGHT CARDS (Context-Aware: Dark Headings on White/Light Backgrounds)
       ========================================================================= */
    .light-card,
    .light-card * {
        color: #0F172A !important;
    }
    .light-card h1, .light-card h2, .light-card h3, .light-card h4 {
        color: #0F172A !important;
        text-shadow: none !important;
    }
    .light-card p, .light-card span, .light-card li {
        color: #334155 !important;
    }
    .light-card .text-muted {
        color: #64748B !important;
    }

    /* =========================================================================
       5. STATUS COLORS & ACCENTS (Preserved for Semantics)
       ========================================================================= */

    /* Notice & Alert Badges */
    .badge-demo {
        display: inline-block;
        background-color: rgba(254, 243, 199, 0.15) !important;
        color: #FDE047 !important; /* Warning Yellow */
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 600;
        border: 1px solid rgba(253, 224, 71, 0.35) !important;
        margin-bottom: 1rem;
    }
    .badge-ai {
        display: inline-block;
        background-color: rgba(236, 253, 245, 0.15) !important;
        color: #6EE7B7 !important; /* Success Green */
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 600;
        border: 1px solid rgba(110, 231, 183, 0.35) !important;
        margin-bottom: 1rem;
    }

    /* Status Pills */
    .status-confirmed {
        background-color: rgba(16, 185, 129, 0.2) !important;
        color: #34D399 !important; /* Success */
        padding: 0.25rem 0.7rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(52, 211, 153, 0.3) !important;
    }
    .status-pending {
        background-color: rgba(245, 158, 11, 0.2) !important;
        color: #FBBF24 !important; /* Warning */
        padding: 0.25rem 0.7rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
    }
    .status-rejected {
        background-color: rgba(239, 68, 68, 0.2) !important;
        color: #F87171 !important; /* Error */
        padding: 0.25rem 0.7rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(248, 113, 113, 0.3) !important;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 20px;
        padding: 3rem 2.5rem;
        color: #FFFFFF !important;
        margin-bottom: 2rem;
        box-shadow: 0 20px 30px -5px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(249,115,22,0.3) 0%, rgba(249,115,22,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-tagline {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        color: #FFFFFF !important;
        margin-bottom: 0.8rem !important;
    }
    .hero-tagline span {
        color: #FB923C !important;
        background: linear-gradient(90deg, #FB923C, #FBBF24) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .hero-subtitle {
        font-size: 1.15rem !important;
        color: #E2E8F0 !important;
        max-width: 700px !important;
        line-height: 1.6 !important;
        margin-bottom: 1.5rem !important;
    }

    /* =========================================================================
       6. STREAMLIT WIDGETS & NAVIGATION (TABS, EXPANDERS, INPUTS, SIDEBAR)
       ========================================================================= */

    /* Sidebar Navigation Enhancement */
    [data-testid="stSidebar"] {
        background-color: #070B14 !important;
        border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #1E293B !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #131B2E !important;
        border: 1px solid #23324F !important;
        border-radius: 8px 8px 0 0 !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        border-color: #38BDF8 !important;
        color: #FFFFFF !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #131B2E !important;
        border: 1px solid #23324F !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] summary * {
        color: #FFFFFF !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    /* Form Inputs */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #131B2E !important;
        color: #F8FAFC !important;
        border-color: #23324F !important;
    }
    </style>
    """
