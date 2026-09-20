# AI Smart Tourism & Travel Recommendation Platform

> **"Your Journey. Your Interests. Your AI-Powered Trip."**  
> *Plan smarter. Travel better. Stay within your budget.*

A complete, production-grade, full-stack travel-tech platform built entirely with **Python**, **Streamlit**, **MongoDB**, **Google Gemini AI**, **Folium**, and **Plotly**.

---

## 🌟 Key Features

1. **Multi-Step AI Trip Architect (9 Steps)**:
   - Accepts **ANY global destination** (Hyderabad, Goa, Paris, Tokyo, Bali, etc.).
   - Date duration validator, party size, custom budgets in multiple currencies (`INR`, `USD`, `EUR`, `GBP`).
   - Granular travel styles, multiple interest tags, accommodation, culinary, and transit preferences.

2. **Dual-Core AI & Resilient Engine**:
   - Live **Google Gemini API** integration with strict JSON structured outputs and self-healing parsing.
   - Intelligent procedural fallback recommendation engine: **The application never crashes even if the AI or external APIs are unavailable**.
   - Clear indicators identifying live vs. demo mode.

3. **Resilient MongoDB Database Layer**:
   - 14 distinct collections: `users`, `trips`, `destinations`, `hotels`, `restaurants`, `transportation`, `activities`, `bookings`, `reviews`, `favorites`, `notifications`, `providers`, `weather_cache`, `ai_recommendations`.
   - Dual-mode connection manager: Connects directly to live MongoDB when `MONGODB_URI` is reachable, or seamlessly operates on an in-memory dictionary-backed store with identical query syntax.

4. **Multi-Role Portals & RBAC**:
   - **Traveler Dashboard**: Interactive KPIs, upcoming and saved trips, favorites, and recommendations.
   - **Provider Portal**: Listings management (Hotels, Dining, Transit, Activities) and reservation confirmation workflow.
   - **Admin Control Center**: User moderation, partner verification, listing moderation, API status monitor, and macro analytics.

5. **Interactive Maps & Weather Intelligence**:
   - Interactive OpenStreetMap via **Folium** and **streamlit-folium** with category markers (Origin, Destination, Stays, Dining, Attractions).
   - Live weather metrics (Temperature, Humidity, Wind, Sunrise/Sunset, 7-Day trends) powered by Open-Meteo with Gemini weather-adaptive advice.

6. **Budget Analytics & AI Optimizer**:
   - Donut & bar chart visualizations using **Plotly**.
   - Automatic over-budget warnings and smart substitution recommendations (e.g., 5-star to boutique, flight to express rail).

7. **Export & Download Engine**:
   - High-quality PDF export (via `fpdf2`), structured CSV schedule, and JSON data dump.

---

## 🚀 Quick Start

### 1. Installation

Ensure Python 3.10+ is installed:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure your optional API keys inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017/tourism_ai
JWT_SECRET=super_secret_jwt_key_tourism_ai_2026
```
*(Note: The platform is fully functional in Demo Mode even without API keys!)*

### 3. Launch Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🔑 Demo Accounts

| Role | Email | Password |
|---|---|---|
| **Traveler** | `traveler@example.com` | `Traveler@123` |
| **Provider** | `provider@tajhotels.com` | `Provider@123` |
| **Admin** | `admin@tourism.ai` | `Admin@12345` |
