import streamlit as st
from database.repositories import Repository
from ui.components import render_section_header, render_kpi_card

def render_profile_view():
    user = st.session_state.get("user") or {}
    user_id = user.get("_id", "guest_traveler")
    user_name = user.get("full_name", "Traveler")
    user_email = user.get("email", "traveler@example.com")
    user_role = user.get("role", "Traveler")

    render_section_header("User Profile & Notifications 👤", "Manage your account, preferences, and system alerts")

    p_col1, p_col2 = st.columns([1, 1.5])
    with p_col1:
        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #0D9488, #0284C7); color: white; font-size: 2rem; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
                {user_name[0] if user_name else 'U'}
            </div>
            <h3 style="margin: 0; color: #F8FAFC;">{user_name}</h3>
            <p style="color: #94A3B8; margin-top: 0.2rem; font-size: 0.9rem;">{user_email}</p>
            <span style="background: rgba(14, 165, 233, 0.2); color: #38BDF8; padding: 0.3rem 0.8rem; border-radius: 9999px; font-weight: 700; font-size: 0.8rem; border: 1px solid rgba(56, 189, 248, 0.3);">
                {user_role} Account
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_role = "Traveler"
            st.session_state.current_page = "Landing"
            st.rerun()

    with p_col2:
        st.markdown("### 🔔 Notifications & Alerts")
        notifications = Repository.get_user_notifications(user_id)

        if st.button("✓ Mark All as Read", key="btn_mark_all_read"):
            Repository.mark_notifications_read(user_id)
            st.success("All notifications marked as read.")
            st.rerun()

        if not notifications:
            st.info("You have no notifications at this time.")
        else:
            for notif in notifications:
                t_color = "#38BDF8" if notif.get("type") == "info" else ("#34D399" if notif.get("type") == "success" else "#FBBF24")
                st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid {t_color}; border: 1px solid #334155; border-radius: 0 12px 12px 0; padding: 1rem; margin-bottom: 0.75rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #F8FAFC;">{notif.get('title')}</b>
                        <span style="font-size: 0.75rem; color: #94A3B8;">{notif.get('created_at', '')[:10]}</span>
                    </div>
                    <p style="color: #CBD5E1; font-size: 0.9rem; margin-top: 0.25rem; margin-bottom: 0;">{notif.get('message')}</p>
                </div>
                """, unsafe_allow_html=True)
