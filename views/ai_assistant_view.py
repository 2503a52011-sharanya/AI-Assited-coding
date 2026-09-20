import streamlit as st
from services.ai_service import ai_service
from config.constants import MOOD_OPTIONS
from ui.components import render_section_header, render_ai_badge

def render_ai_assistant_view():
    render_section_header("AI Travel Concierge & Smart Features 🤖", "Interact with our AI assistant, craft mood-based getaways, or explore hidden gems")
    render_ai_badge("Session Context & Chat Memory Active")

    tab_chat, tab_mood, tab_hidden, tab_group = st.tabs([
        "💬 Interactive Assistant",
        "🎭 AI Mood Planner",
        "💎 AI Hidden Gems",
        "👥 Group Trip Harmonizer"
    ])

    # 1. TAB: CHAT INTERFACE
    with tab_chat:
        st.markdown("#### Ask Your AI Travel Assistant")
        st.markdown("Ask anything about your destination, budget hacks, weather adjustments, or itinerary tips.")

        # Quick Suggestion Chips
        st.markdown("**Quick Prompts:**")
        qp1, qp2, qp3 = st.columns(3)
        quick_prompt = None
        with qp1:
            if st.button("🌦️ Will rain affect my itinerary?", use_container_width=True):
                quick_prompt = "Will rain affect my itinerary?"
        with qp2:
            if st.button("🏨 Suggest a cheaper hotel alternative", use_container_width=True):
                quick_prompt = "Suggest a cheaper hotel alternative"
        with qp3:
            if st.button("💰 How can I reduce my overall trip cost?", use_container_width=True):
                quick_prompt = "How can I reduce my overall trip cost?"

        # Initialize Chat History in session_state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I am your AI Travel Concierge. How can I assist with your travel planning or destination questions today?"}
            ]

        # Display Chat Messages
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])

        # Chat input
        user_input = st.chat_input("Type your travel question here...") or quick_prompt
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            context = st.session_state.get("active_trip") or {}
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    reply = ai_service.ask_travel_assistant(
                        question=user_input,
                        context=context,
                        chat_history=st.session_state.chat_history
                    )
                    st.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # 2. TAB: AI MOOD PLANNER
    with tab_mood:
        st.markdown("#### Travel by Vibe & Emotion")
        st.markdown("Select a mood and let our AI configure tailored pacing and thematic activities.")
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            selected_mood = st.selectbox("Current Travel Mood", MOOD_OPTIONS)
            mood_dest = st.text_input("Destination", value="Goa").strip()
        with m_col2:
            mood_days = st.slider("Duration (Days)", 1, 10, 4)
            mood_curr = st.selectbox("Currency", ["INR", "USD", "EUR"], index=0)

        if st.button("✨ Craft Mood-Based Experience", type="primary"):
            mood_res = ai_service.generate_mood_trip(
                mood=selected_mood,
                destination=mood_dest,
                days=mood_days,
                budget=25000,
                currency=mood_curr
            )
            st.success(f"Tailored {selected_mood} plan generated!")
            st.markdown(f"""
            <div style="background: #1E293B; border-left: 4px solid #FB923C; border: 1px solid #334155; padding: 1.25rem; border-radius: 0 12px 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="color: #38BDF8; margin-top: 0;">🎭 {selected_mood} Experience: {mood_dest}</h4>
                <p style="color: #F8FAFC;"><b>Pacing:</b> {mood_res['pacing']}</p>
                <p style="color: #2DD4BF;"><b>Core Focus:</b> {mood_res['theme_focus']}</p>
                <p style="color: #CBD5E1;">{mood_res['summary']}</p>
            </div>
            """, unsafe_allow_html=True)

    # 3. TAB: HIDDEN GEMS
    with tab_hidden:
        st.markdown("#### 💎 AI Off-The-Beaten-Path & Hidden Gems")
        st.markdown("Discover lesser-known scenic vistas, heritage secrets, and uncrowded spots.")
        gem_city = st.text_input("Enter city to uncover secrets", value="Hyderabad")
        if st.button("Uncover Hidden Gems", type="primary"):
            st.markdown(f"""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; margin-top: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <b style="color: #38BDF8; font-size: 1.1rem;">Hidden Gems in {gem_city}:</b>
                <ul style="color: #CBD5E1; margin-top: 0.5rem; line-height: 1.8;">
                    <li><b style="color: #2DD4BF;">Paigah Tombs:</b> Intricate stucco architectural marvel tucked away in the old quarter with a fraction of the Charminar crowds.</li>
                    <li><b style="color: #2DD4BF;">Qutb Shahi Tombs Heritage Garden:</b> Peaceful manicured Persian-Deccani stepwells and sandstone mausoleums ideal for photography.</li>
                    <li><b style="color: #2DD4BF;">Khajaguda Rock Hills:</b> Prehistoric granite formations offering panoramic city views and quiet sunset spots.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # 4. TAB: GROUP TRIP HARMONIZER
    with tab_group:
        st.markdown("#### 👥 Group Travel Harmonizer")
        st.markdown("Traveling with friends or family with conflicting interests? Harmonize different preferences.")
        st.text_area("List Group Members & Conflicting Interests", "1. Aarav (History & Forts)\n2. Priya (Beaches & Relaxing)\n3. Rohan (Food & Nightlife)")
        if st.button("Harmonize Group Schedule", type="primary"):
            st.success("Balanced Group Formula Generated!")
            st.markdown("""
            - **Morning (09:00 - 13:00):** Guided historic fort exploration for Aarav while morning temperatures are cool.
            - **Afternoon (14:00 - 17:30):** Shaded beachside cafe relaxation, hammock lounge, and spa for Priya.
            - **Evening (18:30 - 23:00):** Vibrant coastal night market, live seafood bbq, and lounge music for Rohan.
            """)
