import streamlit as st
from utils.authentication import get_current_user, hash_password
from database.queries import (
    get_user_preferences, update_user_preferences, get_user_trips,
    get_user_bookings, execute_query
)
from config.settings import (
    TRAVEL_STYLES, TRANSPORT_TYPES, ACCOMMODATION_TYPES,
    FOOD_PREFERENCES, INTEREST_CATEGORIES
)
from utils.helpers import format_currency


def render_profile_page():
    st.title("👤 Traveler Profile & Smart Personalization")
    st.caption("Customize your personal travel DNA. The AI recommendation engine uses these settings to tailor destinations and budgets.")

    user = get_current_user()
    if not user:
        # Fallback to test user if not logged in
        user = {"id": 2, "name": "Rohit Sharma", "email": "traveler@example.com", "phone": "+91 9123456780", "role": "user"}

    user_id = user["id"]
    prefs = get_user_preferences(user_id) or {}

    # Metrics Row
    trips = get_user_trips(user_id)
    bookings = get_user_bookings(user_id)
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Total Trips Planned", len(trips))
    with mcol2:
        st.metric("Total Bookings", len(bookings))
    with mcol3:
        active_b = sum(1 for b in bookings if b["status"] == "Confirmed")
        st.metric("Active Bookings", active_b)
    with mcol4:
        st.metric("Membership Tier", "Explorer Gold ⭐")

    st.markdown("---")

    tab_prefs, tab_account, tab_security = st.tabs([
        "⚙️ Travel Preferences", "📋 Personal Details", "🔒 Security & Password"
    ])

    with tab_prefs:
        st.subheader("Smart Personalization Engine Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            curr_style = prefs.get("travel_style", "Comfortable")
            style_idx = TRAVEL_STYLES.index(curr_style) if curr_style in TRAVEL_STYLES else 2
            style = st.selectbox("Preferred Travel Style", TRAVEL_STYLES, index=style_idx)
            
            budget_range = st.selectbox(
                "Typical Budget Range",
                ["₹5,000 - ₹10,000", "₹10,000 - ₹25,000", "₹25,000 - ₹50,000", "₹50,000+"],
                index=1
            )
            
            curr_trans = prefs.get("preferred_transport", "Train")
            trans_idx = TRANSPORT_TYPES.index(curr_trans) if curr_trans in TRANSPORT_TYPES else 1
            trans = st.selectbox("Preferred Transportation", TRANSPORT_TYPES, index=trans_idx)

        with col2:
            curr_acc = prefs.get("preferred_accommodation", "Budget hotel")
            acc_idx = ACCOMMODATION_TYPES.index(curr_acc) if curr_acc in ACCOMMODATION_TYPES else 1
            acc = st.selectbox("Preferred Accommodation", ACCOMMODATION_TYPES, index=acc_idx)
            
            curr_food = prefs.get("food_preference", "Local food")
            food_idx = FOOD_PREFERENCES.index(curr_food) if curr_food in FOOD_PREFERENCES else 3
            food = st.selectbox("Food Preference", FOOD_PREFERENCES, index=food_idx)

            curr_interests_str = prefs.get("interests", "Nature, Photography")
            default_interests = [i.strip() for i in curr_interests_str.split(",") if i.strip() in INTEREST_CATEGORIES]
            interests = st.multiselect("Core Travel Passions", INTEREST_CATEGORIES, default=default_interests)

        access_notes = st.text_input("Special Accessibility or Mobility Requirements", value=prefs.get("accessibility_requirements", ""))

        if st.button("💾 Save Preferences", type="primary"):
            interests_str = ", ".join(interests)
            update_user_preferences(user_id, style, budget_range, trans, acc, food, interests_str, access_notes)
            st.success("Travel preferences updated successfully! Recommendations will now prioritize these choices.")

    with tab_account:
        st.subheader("Account Information")
        st.markdown(f"**Full Name:** {user['name']}")
        st.markdown(f"**Registered Email:** `{user['email']}`")
        st.markdown(f"**Phone Number:** {user.get('phone', 'Not provided')}")
        st.markdown(f"**Role:** `{user.get('role', 'user')}`")

    with tab_security:
        st.subheader("Change Account Password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        if st.button("Update Password"):
            if new_pw and new_pw == confirm_pw:
                hashed = hash_password(new_pw)
                execute_query("UPDATE users SET password_hash = :pw WHERE id = :uid", {"pw": hashed, "uid": user_id})
                st.success("Password changed successfully!")
            else:
                st.error("Passwords do not match or are empty.")


render_profile_page()

