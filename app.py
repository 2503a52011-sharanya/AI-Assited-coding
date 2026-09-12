import streamlit as st
from config.database import init_db
from utils.authentication import login_user, logout_user, is_authenticated, is_admin
from database.queries import create_user
from services.ai_assistant_service import AIAssistantService

# Page configuration
st.set_page_config(
    page_title="AI Smart Tourism & Travel System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Clean Light UI Custom CSS
st.markdown("""
<style>
    /* Global App Container */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    p, span, label {
        color: #334155;
    }

    /* Labels above Inputs */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        margin-bottom: 8px !important;
    }

    /* Standard Professional Input Styling - Light, Clean, No Heavy Shadows */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        color: #0f172a !important;
        transition: border-color 0.15s ease-in-out;
    }

    /* Text Inside Inputs - NEVER Transparent, Fully Readable */
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="select"] input,
    textarea {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        background-color: #ffffff !important;
        opacity: 1 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
    }

    /* Focus Behavior - Crisp Subtle Blue Border, NO Glow, NO Disappearing Text */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #0284c7 !important;
        box-shadow: 0 0 0 1px #0284c7 !important;
        background-color: #ffffff !important;
    }

    div[data-baseweb="input"] input:focus,
    div[data-baseweb="base-input"] input:focus,
    div[data-baseweb="select"] input:focus,
    textarea:focus {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        background-color: #ffffff !important;
        opacity: 1 !important;
    }

    /* Multi-select Pills */
    span[data-baseweb="tag"] {
        background-color: #f1f5f9 !important;
        color: #0369a1 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }

    /* Cards & Container Containers - Subtle Flat Border */
    div[data-testid="stExpander"],
    div[data-testid="stForm"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
    }

    /* Modern Flat Clean Buttons */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }

    .stButton > button:hover {
        background-color: #f8fafc !important;
        border-color: #94a3b8 !important;
        transform: none !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #0284c7 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #0369a1 !important;
        border-color: #0369a1 !important;
        transform: none !important;
    }

    /* Sidebar - Clean, Simple, Professional */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database schema & seed data
try:
    init_db()
except Exception as e:
    st.error(f"Database initialization warning: {e}")

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True # Default logged in as demo traveler
    st.session_state["user_id"] = 2
    st.session_state["user_name"] = "Rohit Sharma"
    st.session_state["user_email"] = "traveler@example.com"
    st.session_state["user_role"] = "user"

if "nav_choice" not in st.session_state:
    st.session_state["nav_choice"] = "Home"

# Unified Streamlit Multipage Navigation Definition
# Base pages available to all users (Travelers, Persons, Guests)
pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/explore.py", title="Explore Destinations", icon="🌍"),
    st.Page("pages/planner.py", title="Plan My Trip", icon="🗺️"),
    st.Page("pages/destinations.py", title="Destinations", icon="📍"),
    st.Page("pages/transportation.py", title="Transportation", icon="🚆"),
    st.Page("pages/hotels.py", title="Hotels & Stays", icon="🏨"),
    st.Page("pages/hostels.py", title="Hostel Dashboard", icon="🛏️"),
    st.Page("pages/activities.py", title="Activities", icon="🧗"),
    st.Page("pages/budget.py", title="Budget Planner", icon="💰"),
    st.Page("pages/trips.py", title="My Trips", icon="🧳"),
    st.Page("pages/bookings.py", title="Booking Dashboard", icon="🎫"),
    st.Page("pages/profile.py", title="Profile", icon="👤"),
]

# Admin Dashboard is ONLY shown if user is authenticated AND has role == 'admin'
if is_authenticated() and is_admin():
    pages.append(st.Page("pages/admin.py", title="Admin Dashboard", icon="🛡️"))

pg = st.navigation(pages)

PAGE_ROUTES = {
    "Home": "pages/home.py",
    "Explore Destinations": "pages/explore.py",
    "Explore": "pages/explore.py",
    "Plan My Trip": "pages/planner.py",
    "Plan Trip": "pages/planner.py",
    "Planner": "pages/planner.py",
    "Destinations": "pages/destinations.py",
    "Transportation": "pages/transportation.py",
    "Hotels": "pages/hotels.py",
    "Hotels & Stays": "pages/hotels.py",
    "Hostel Dashboard": "pages/hostels.py",
    "Hostels": "pages/hostels.py",
    "Activities": "pages/activities.py",
    "Budget Planner": "pages/budget.py",
    "Budget": "pages/budget.py",
    "My Trips": "pages/trips.py",
    "Trips": "pages/trips.py",
    "Booking Dashboard": "pages/bookings.py",
    "My Bookings": "pages/bookings.py",
    "Bookings": "pages/bookings.py",
    "Profile": "pages/profile.py",
    "Admin Dashboard": "pages/admin.py",
    "Admin": "pages/admin.py",
}

if "nav_choice" in st.session_state and st.session_state["nav_choice"] in PAGE_ROUTES and st.session_state["nav_choice"] != "Home":
    target_choice = st.session_state.pop("nav_choice")
    st.switch_page(PAGE_ROUTES[target_choice])

# -------------------------------------------------------------
# SIDEBAR: USER AUTH & EMBEDDED AI ASSISTANT
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding-bottom: 8px;">
        <h2 style="margin: 0; color: #0284c7; font-size: 1.5rem;">✈️ SmartTourism</h2>
        <span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">AI Travel & Tourism Platform</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # User Profile / Switcher Widget
    st.markdown("##### 👤 User Account")
    if is_authenticated():
        if is_admin():
            st.markdown(f"**🛡️ {st.session_state.get('user_name', 'Admin')}** (Administrator)")
            st.caption(f"Email: `{st.session_state.get('user_email', 'admin@smarttourism.com')}`")
            st.success("🔓 Admin Dashboard is unlocked in the navigation above.")
            col_sw1, col_sw2 = st.columns(2)
            with col_sw1:
                if st.button("👤 Person Login", width="stretch", key="sw_to_person", help="Switch to standard Traveler account"):
                    login_user("traveler@example.com", "Traveler@123")
                    st.rerun()
            with col_sw2:
                if st.button("Log Out", width="stretch", key="admin_logout"):
                    logout_user()
                    st.rerun()
        else:
            st.markdown(f"**🧳 {st.session_state.get('user_name', 'Traveler')}** (Person / Traveler)")
            st.caption(f"Email: `{st.session_state.get('user_email', 'traveler@example.com')}`")
            col_sw1, col_sw2 = st.columns(2)
            with col_sw1:
                if st.button("🛡️ Admin Login", width="stretch", key="sw_to_admin", help="Switch to Administrator account"):
                    login_user("admin@smarttourism.com", "Admin@123")
                    st.rerun()
            with col_sw2:
                if st.button("Log Out", width="stretch", key="user_logout"):
                    logout_user()
                    st.rerun()
    else:
        st.info("Currently in Guest Mode.")
        with st.expander("🔑 Login / Access Options", expanded=True):
            auth_mode = st.radio("Login Options", ["👤 Person Login", "🛡️ Admin Login", "📝 Register"], horizontal=False)
            
            if auth_mode == "👤 Person Login":
                st.markdown("<small style='color: #475569;'>Standard Traveler / Person Account</small>", unsafe_allow_html=True)
                if st.button("⚡ 1-Click Person Demo Login", type="primary", width="stretch", key="demo_person_btn"):
                    success, msg = login_user("traveler@example.com", "Traveler@123")
                    st.rerun()
                st.markdown("<div style='text-align: center; margin: 4px 0; color: #94a3b8; font-size: 0.8rem;'>— OR LOGIN WITH DETAILS —</div>", unsafe_allow_html=True)
                email_in = st.text_input("Email", value="traveler@example.com", key="login_person_email")
                pw_in = st.text_input("Password", type="password", value="Traveler@123", key="login_person_pw")
                if st.button("Log In as Person", width="stretch", key="btn_person_submit"):
                    success, msg = login_user(email_in, pw_in)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
            elif auth_mode == "🛡️ Admin Login":
                st.markdown("<small style='color: #475569;'>Platform Administrator Account</small>", unsafe_allow_html=True)
                if st.button("⚡ 1-Click Admin Demo Login", type="primary", width="stretch", key="demo_admin_btn"):
                    success, msg = login_user("admin@smarttourism.com", "Admin@123")
                    st.rerun()
                st.markdown("<div style='text-align: center; margin: 4px 0; color: #94a3b8; font-size: 0.8rem;'>— OR LOGIN WITH DETAILS —</div>", unsafe_allow_html=True)
                email_admin = st.text_input("Admin Email", value="admin@smarttourism.com", key="login_admin_email")
                pw_admin = st.text_input("Admin Password", type="password", value="Admin@123", key="login_admin_pw")
                if st.button("Log In as Admin", width="stretch", key="btn_admin_submit"):
                    success, msg = login_user(email_admin, pw_admin)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
            else:
                name_in = st.text_input("Full Name", value="New Traveler", key="reg_name_in")
                email_reg = st.text_input("Email", value="newtraveler@example.com", key="reg_email_in")
                pw_reg = st.text_input("Password", type="password", value="Pass@123", key="reg_pw_in")
                phone_in = st.text_input("Phone Number", value="+91 9876543210", key="reg_phone_in")
                if st.button("Register Account", type="primary", width="stretch", key="reg_submit_btn"):
                    from utils.authentication import hash_password
                    new_uid = create_user(name_in, email_reg, hash_password(pw_reg), phone_in)
                    st.success("Account created! Logging you in...")
                    login_user(email_reg, pw_reg)
                    st.rerun()

    # Quick action button near Login / Account
    if st.button("🗺️ Plan a Trip", key="side_plan_trip_btn", type="primary", width="stretch"):
        target_tt = st.session_state.get("selected_traveler_type", "Solo")
        if target_tt == "All Travelers":
            target_tt = "Solo"
        st.session_state["plan_traveler_type"] = target_tt
        st.session_state["plan_travelers"] = 1 if target_tt == "Solo" else (2 if target_tt == "Couple" else 4)
        st.session_state.pop("plan_generated", None)
        st.switch_page("pages/planner.py")

    st.markdown("---")

    # Embedded AI Travel Assistant in Sidebar
    with st.expander("🤖 AI Travel Assistant", expanded=False):
        st.caption("Ask questions with budgets, origins, and days!")
        assistant_prompt = st.text_area(
            "What would you like to plan?",
            value="I have ₹15,000 and 3 days. I am starting from Hyderabad and like nature and photography.",
            height=85,
            key="side_ai_prompt"
        )
        if st.button("Ask Assistant", type="primary", width="stretch"):
            with st.spinner("AI Assistant analyzing system database and pricing..."):
                reply = AIAssistantService.answer_query(assistant_prompt)
                st.markdown(reply)

# -------------------------------------------------------------
# RUN CURRENT PAGE
# -------------------------------------------------------------
pg.run()

