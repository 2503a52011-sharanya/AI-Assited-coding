import streamlit as st
from database.repositories import Repository

def render_auth_view():
    """Authentication view supporting login and dual-role registration."""
    st.markdown("<div style='text-align: center; margin-top: 1rem; margin-bottom: 2rem;'>"
                "<h1 class='page-title' style='text-align: center;'>Welcome to AI Smart Tourism</h1>"
                "<p class='page-subtitle' style='text-align: center;'>Access your personalized travel itineraries and portals</p>"
                "</div>", unsafe_allow_html=True)

    tab_choice = st.session_state.get("auth_tab", "Login")
    tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])

    # 1. LOGIN TAB
    with tab1:
        st.markdown("#### Access Your Account")
        with st.form("form_login"):
            email = st.text_input("Email Address", placeholder="e.g. traveler@example.com").strip()
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Sign In", use_container_width=True, type="primary")

            if submit_login:
                if not email or not password:
                    st.error("Please provide both email and password.")
                else:
                    try:
                        user = Repository.authenticate_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.user_role = user.get("role", "Traveler")
                            st.success(f"Welcome back, {user.get('full_name')}!")
                            
                            # Redirect based on role
                            if user.get("role") == "Admin":
                                st.session_state.current_page = "Admin Portal"
                            elif user.get("role") == "Provider":
                                st.session_state.current_page = "Provider Portal"
                            else:
                                st.session_state.current_page = "Dashboard"
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")
                    except ValueError as ve:
                        st.error(str(ve))
                    except Exception as e:
                        st.error(f"Authentication error: {e}")

        # Quick Demo Credential Guide
        with st.expander("💡 Quick Demo Credentials"):
            st.markdown("""
            - **Traveler**: `traveler@example.com` / `Traveler@123`
            - **Provider**: `provider@tajhotels.com` / `Provider@123`
            - **Admin**: `admin@tourism.ai` / `Admin@12345`
            """)

    # 2. REGISTRATION TAB
    with tab2:
        st.markdown("#### Join Our Intelligent Tourism Network")
        with st.form("form_register"):
            full_name = st.text_input("Full Name", placeholder="e.g. Maya Patel")
            reg_email = st.text_input("Email Address", placeholder="e.g. maya@example.com").strip()
            phone = st.text_input("Phone Number (Optional)", placeholder="+91 9876543210")
            
            # Roles allowed for public registration: ONLY Traveler and Provider
            reg_role = st.selectbox(
                "Register As",
                ["Traveler", "Provider"],
                help="Travelers plan and book trips. Providers list hotels, dining, or experiences."
            )

            # Extra fields if Provider
            business_name = ""
            provider_type = ""
            if reg_role == "Provider":
                business_name = st.text_input("Business / Property Name", placeholder="e.g. Royal Heritage Stays")
                provider_type = st.selectbox("Provider Category", ["Hotel", "Restaurant", "Transport", "Tour/Activity"])

            pass1 = st.text_input("Create Password", type="password", placeholder="Minimum 6 characters")
            pass2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

            submit_reg = st.form_submit_button("Create Account", use_container_width=True, type="primary")

            if submit_reg:
                if not full_name or not reg_email or not pass1:
                    st.error("Please fill in all required fields.")
                elif pass1 != pass2:
                    st.error("Passwords do not match.")
                elif len(pass1) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif reg_role == "Provider" and not business_name:
                    st.error("Please provide your Business or Property name.")
                else:
                    try:
                        user_doc = Repository.create_user({
                            "email": reg_email,
                            "password": pass1,
                            "full_name": full_name,
                            "role": reg_role,
                            "phone": phone,
                            "provider_business_name": business_name,
                            "provider_type": provider_type
                        })
                        if reg_role == "Provider":
                            st.success("Provider account created! Awaiting Admin approval before first sign-in.")
                        else:
                            st.success("Account created successfully! You can now sign in.")
                            st.session_state.auth_tab = "Login"
                    except ValueError as ve:
                        st.error(str(ve))
                    except Exception as e:
                        st.error(f"Registration failed: {e}")
