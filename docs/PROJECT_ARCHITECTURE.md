# AI-Powered Smart Tourism and Travel Recommendation System
## Project Architecture Documentation

**Project Phase:** PHASE 1 - Architecture and Planning  
**Status:** In Progress  
**Last Updated:** 2026-08-30

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Database Design](#database-design)
5. [API Architecture](#api-architecture)
6. [Frontend Architecture](#frontend-architecture)
7. [Backend Architecture](#backend-architecture)
8. [AI/ML Components](#aiml-components)
9. [External API Integrations](#external-api-integrations)
10. [Security Architecture](#security-architecture)
11. [Development Phases](#development-phases)
12. [Directory Structure](#directory-structure)

---

## Project Overview

### Objective

Build a comprehensive full-stack web application for intelligent tourism and travel planning that leverages AI/ML to provide personalized recommendations, intelligent itinerary generation, and complete trip management.

### Key Features

- **Personalized Recommendations:** AI-driven destination suggestions based on user preferences
- **Intelligent Itinerary Generation:** AI-generated day-wise travel plans using LLM
- **Trip Management:** Create, plan, and manage complete travel experiences
- **Budget Planning & Tracking:** Real-time expense tracking and budget analysis
- **Booking Management:** Handle flights, hotels, trains, and activities
- **Reviews & Ratings:** Community-driven destination feedback
- **Weather Integration:** Real-time weather forecasts for destinations
- **Maps & Places:** Tourist attractions and location information
- **Currency Conversion:** Multi-currency support for international travel
- **Admin Dashboard:** Destination management and analytics
- **User Authentication:** Secure registration, login, and authorization

### Target Users

1. **Regular Users:** Travelers seeking personalized recommendations and trip planning
2. **Administrators:** Managing destinations, users, and system analytics

---

## Technology Stack

### Frontend Development

```
Framework:     React.js (UI library)
Build Tool:    Vite (fast build and dev server)
Styling:       Tailwind CSS (utility-first CSS framework)
Routing:       React Router v6
HTTP Client:   Axios
State Mgmt:    Context API / React Hooks
Language:      JavaScript (ES6+)
Markup:        HTML5
Styling:       CSS3
```

**Frontend Skills:**
- Component-based architecture
- Responsive & mobile-first design
- Form validation and error handling
- Protected route management
- API integration and state management
- Authentication state persistence
- Loading and error states

### Backend Development

```
Language:      Python 3.10+
Framework:     FastAPI (modern async web framework)
Web Server:    Uvicorn (ASGI server)
Validation:    Pydantic (data validation)
ORM:           SQLAlchemy (database abstraction)
API Style:     REST (RESTful API design)
```

**Backend Responsibilities:**
- REST API development
- Business logic implementation
- Database operations and optimization
- Authentication & Authorization
- AI service integration
- External API consumption
- Input validation & error handling
- Security: environment config, no hardcoded secrets

### Database

```
DBMS:          PostgreSQL (relational database)
ORM:           SQLAlchemy (Python ORM)
```

**Database Skills:**
- Relational data modeling
- Entity-relationship design
- Primary & foreign key constraints
- One-to-many & many-to-one relationships
- CRUD operations
- Query optimization

### AI/ML Components

```
Language:      Python
Libraries:     
  - Pandas (data manipulation)
  - NumPy (numerical computations)
  - Scikit-learn (machine learning algorithms)
LLM API:       Google Gemini API (for itinerary generation)
```

**AI Capabilities:**
- Content-based recommendation system
- Destination similarity calculations
- User preference matching
- Budget compatibility analysis
- Historical preference learning
- LLM-powered itinerary generation
- Explainable AI recommendations

### Development & Version Control

```
Version Control: Git & GitHub
Package Manager: pip (Python), npm (Node.js)
```

---

## System Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                    React.js + Tailwind CSS                       │
│                      (Vite Dev Server)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    Axios (HTTP Client)
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    REST API GATEWAY                              │
│                   FastAPI + Uvicorn                              │
│                   (Backend Server)                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │   Services   │  │ External APIs│
│  Database    │  │ (AI, Logic)  │  │(Weather, Map,│
│ SQLAlchemy   │  │              │  │  Currency)   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Communication Flow

**Request Flow (Frontend → Backend):**
1. React component initiates request via Axios
2. Request sent to FastAPI endpoint
3. FastAPI validates input using Pydantic
4. Business logic processes request
5. Database query executed via SQLAlchemy
6. Response formatted and returned to frontend
7. Frontend updates UI with response data

**AI Integration Flow:**
1. Frontend sends recommendation request
2. Backend extracts user preferences from database
3. AI system computes similarity scores
4. Top recommendations ranked and explained
5. Formatted response sent to frontend

**External API Flow:**
1. Frontend requests external data (weather, maps, currency)
2. Backend receives request
3. Backend validates request
4. Backend queries external API (API key kept secure)
5. Response parsed and transformed
6. Data sent to frontend

---

## Database Design

### Entity-Relationship Diagram (Conceptual)

```
USER (1) ─────────── (M) TRIP
  │                    │
  │                    ├─── ITINERARY (1) ─── (M) ITINERARY_ITEM
  │                    │
  │                    ├─── BOOKING
  │                    │
  │                    └─── EXPENSE
  │
  ├─── USER_PREFERENCE
  │
  ├─── REVIEW ────── DESTINATION
  │
  └─── BOOKINGS

DESTINATION (1) ─────────── (M) TRIP
     │
     └─── REVIEW
```

### Database Entities

#### USER
Core user management and authentication

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique user identifier |
| name | String(255) | NOT NULL | User's full name |
| email | String(255) | NOT NULL, Unique | User email (login identifier) |
| password_hash | String(255) | NOT NULL | Hashed password (never plaintext) |
| role | Enum (User/Admin) | Default: User | Authorization role |
| created_at | DateTime | NOT NULL, Default: now() | Account creation timestamp |

**Relationships:**
- One User → Many Trips
- One User → Many Reviews
- One User → Many Bookings
- One User → One User Preference

#### DESTINATION
Catalog of travel destinations

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique destination ID |
| name | String(255) | NOT NULL | Destination name (e.g., "Manali") |
| country | String(100) | NOT NULL | Country name |
| state | String(100) | NOT NULL | State/Province |
| description | Text | Nullable | Detailed description |
| category | String(100) | NOT NULL | Category (Adventure, Beach, Cultural, etc.) |
| estimated_budget | Integer | Nullable | Budget in base currency (e.g., INR) |
| climate | String(100) | NOT NULL | Climate type (Cool, Tropical, Desert, etc.) |
| activities | String(500) | Nullable | Comma-separated activities |
| latitude | Float | Nullable | Geographic latitude |
| longitude | Float | Nullable | Geographic longitude |
| image_url | String(500) | Nullable | Image for destination |
| created_at | DateTime | NOT NULL, Default: now() | Creation timestamp |

**Relationships:**
- One Destination → Many Trips
- One Destination → Many Reviews

#### USER_PREFERENCE
Stores user travel preferences for personalization

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique preference ID |
| user_id | Integer (FK) | NOT NULL, References USER.id | User identifier |
| preferred_category | String(100) | Nullable | Preferred destination category |
| preferred_climate | String(100) | Nullable | Preferred climate |
| preferred_activities | String(500) | Nullable | Comma-separated activities |
| budget_range | String(50) | Nullable | Budget range (e.g., "Budget", "Moderate", "Premium") |
| travel_companions | String(100) | Nullable | Travel type (Solo, Friends, Family, Couple) |

**Relationships:**
- One User (via FK) → One User Preference

#### TRIP
Represents a planned travel experience

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique trip ID |
| user_id | Integer (FK) | NOT NULL, References USER.id | Trip owner |
| destination_id | Integer (FK) | NOT NULL, References DESTINATION.id | Destination |
| title | String(255) | NOT NULL | Trip title (e.g., "Manali Adventure 2026") |
| start_date | Date | NOT NULL | Trip start date |
| end_date | Date | NOT NULL | Trip end date |
| total_budget | Integer | NOT NULL | Total allocated budget |
| status | Enum (Planning/Confirmed/Completed/Cancelled) | Default: Planning | Trip status |
| created_at | DateTime | NOT NULL, Default: now() | Creation timestamp |

**Relationships:**
- One Trip → Many Itineraries
- One Trip → Many Bookings
- One Trip → Many Expenses

#### ITINERARY
High-level trip itinerary structure

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique itinerary ID |
| trip_id | Integer (FK) | NOT NULL, References TRIP.id | Associated trip |
| title | String(255) | NOT NULL | Itinerary title |
| description | Text | Nullable | Detailed description |
| created_at | DateTime | NOT NULL, Default: now() | Creation timestamp |

**Relationships:**
- One Itinerary → Many Itinerary Items

#### ITINERARY_ITEM
Day-by-day breakdown of activities

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique item ID |
| itinerary_id | Integer (FK) | NOT NULL, References ITINERARY.id | Parent itinerary |
| day_number | Integer | NOT NULL | Day number (1, 2, 3, ...) |
| activity | String(255) | NOT NULL | Activity name |
| location | String(255) | Nullable | Activity location |
| start_time | Time | Nullable | Activity start time |
| estimated_cost | Integer | Nullable | Estimated cost in base currency |
| description | Text | Nullable | Activity details |

**Relationships:**
- Many Items → One Itinerary

#### BOOKING
Travel booking records

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique booking ID |
| user_id | Integer (FK) | NOT NULL, References USER.id | Booking owner |
| trip_id | Integer (FK) | NOT NULL, References TRIP.id | Associated trip |
| booking_type | Enum (Hotel/Flight/Train/Activity) | NOT NULL | Type of booking |
| provider | String(255) | NOT NULL | Service provider name |
| booking_date | DateTime | NOT NULL | Booking creation date |
| amount | Integer | NOT NULL | Booking cost |
| status | Enum (Pending/Confirmed/Cancelled) | Default: Pending | Booking status |

**Relationships:**
- One User → Many Bookings
- One Trip → Many Bookings

#### EXPENSE
Actual travel expenses tracking

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique expense ID |
| trip_id | Integer (FK) | NOT NULL, References TRIP.id | Associated trip |
| category | String(100) | NOT NULL | Expense category |
| amount | Integer | NOT NULL | Expense amount |
| description | String(255) | Nullable | Expense details |
| expense_date | Date | NOT NULL | When expense occurred |

**Relationships:**
- One Trip → Many Expenses

#### REVIEW
User reviews and ratings for destinations

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | Integer (PK) | Auto-increment, Unique | Unique review ID |
| user_id | Integer (FK) | NOT NULL, References USER.id | Review author |
| destination_id | Integer (FK) | NOT NULL, References DESTINATION.id | Reviewed destination |
| rating | Integer | NOT NULL, Range: 1-5 | Star rating |
| comment | Text | Nullable | Review text |
| created_at | DateTime | NOT NULL, Default: now() | Review creation timestamp |

**Relationships:**
- One User → Many Reviews
- One Destination → Many Reviews

---

## API Architecture

### REST API Design Principles

- **Stateless:** Each request contains all required information
- **Modular:** Organized by resource domain
- **Consistent:** Uniform response formats
- **Secure:** JWT authentication, role-based access
- **Documented:** Clear endpoint specifications

### API Endpoint Categories

#### 1. Health & Status
```
GET /api/health
  Purpose: System health check
  Auth: None required
  Response: { status: "healthy", timestamp: ISO8601 }
```

#### 2. Authentication
```
POST /api/auth/register
  Input: { name, email, password }
  Output: { user_id, email, token }

POST /api/auth/login
  Input: { email, password }
  Output: { user_id, email, token, role }

GET /api/auth/me
  Auth: Required (Bearer JWT)
  Output: { user_id, name, email, role }
```

#### 3. User Management
```
GET /api/users/me
  Auth: Required
  Output: User profile details

PUT /api/users/me
  Auth: Required
  Input: { name, email }
  Output: Updated user profile
```

#### 4. Destinations
```
GET /api/destinations
  Query: ?search=...&category=...&budget_max=...
  Output: List of destinations with filters

GET /api/destinations/{id}
  Output: Single destination details

POST /api/destinations
  Auth: Admin only
  Input: Destination data
  Output: Created destination

PUT /api/destinations/{id}
  Auth: Admin only
  Input: Updated destination data
  Output: Updated destination

DELETE /api/destinations/{id}
  Auth: Admin only
  Output: Deletion confirmation
```

#### 5. Recommendations
```
POST /api/recommendations
  Auth: Required
  Input: {
    budget: 30000,
    duration: 5,
    category: "Adventure",
    climate: "Cool",
    activities: ["Trekking", "Nature"],
    travel_companions: "Friends"
  }
  Output: [
    {
      destination: {...},
      match_score: 0.95,
      reasons: ["matches adventure preference", ...]
    }
  ]
```

#### 6. Trips
```
POST /api/trips
  Auth: Required
  Input: { destination_id, title, start_date, end_date, budget }
  Output: Created trip

GET /api/trips
  Auth: Required
  Output: User's trips

GET /api/trips/{id}
  Auth: Required
  Output: Trip details

PUT /api/trips/{id}
  Auth: Required
  Input: Updated trip data
  Output: Updated trip

DELETE /api/trips/{id}
  Auth: Required
  Output: Deletion confirmation
```

#### 7. Itineraries
```
POST /api/itineraries
  Auth: Required
  Input: { trip_id, title, description }
  Output: Created itinerary

POST /api/itineraries/generate
  Auth: Required
  Input: {
    destination_id,
    days: 5,
    budget: 30000,
    interests: [...],
    travel_companions: "Friends",
    activities: [...]
  }
  Output: AI-generated itinerary

GET /api/itineraries/{trip_id}
  Auth: Required
  Output: Itinerary for trip

PUT /api/itineraries/{id}
  Auth: Required
  Input: Updated itinerary data
  Output: Updated itinerary

DELETE /api/itineraries/{id}
  Auth: Required
  Output: Deletion confirmation
```

#### 8. Bookings
```
POST /api/bookings
  Auth: Required
  Input: { trip_id, booking_type, provider, amount }
  Output: Created booking

GET /api/bookings
  Auth: Required
  Output: User's bookings

GET /api/bookings/{id}
  Auth: Required
  Output: Booking details

PUT /api/bookings/{id}
  Auth: Required
  Input: Updated booking data
  Output: Updated booking

DELETE /api/bookings/{id}
  Auth: Required
  Output: Deletion confirmation
```

#### 9. Budget & Expenses
```
POST /api/expenses
  Auth: Required
  Input: { trip_id, category, amount, description, expense_date }
  Output: Created expense

GET /api/expenses/{trip_id}
  Auth: Required
  Output: {
    expenses: [...],
    total_budget: 50000,
    total_expenses: 32000,
    remaining_budget: 18000,
    utilization_percentage: 64%
  }

PUT /api/expenses/{id}
  Auth: Required
  Input: Updated expense data
  Output: Updated expense

DELETE /api/expenses/{id}
  Auth: Required
  Output: Deletion confirmation
```

#### 10. Reviews
```
POST /api/reviews
  Auth: Required
  Input: { destination_id, rating, comment }
  Output: Created review

GET /api/destinations/{id}/reviews
  Auth: Optional
  Output: List of reviews for destination
```

#### 11. External APIs
```
GET /api/weather/{destination}
  Auth: Optional
  Output: {
    temperature,
    humidity,
    condition,
    wind_speed,
    forecast: [...]
  }

GET /api/places/{destination}
  Auth: Optional
  Output: {
    places: [
      {
        name,
        category,
        location,
        description,
        rating
      }
    ]
  }

GET /api/currency
  Query: ?from=USD&to=INR&amount=100
  Auth: Optional
  Output: {
    source_currency,
    target_currency,
    original_amount,
    converted_amount,
    exchange_rate
  }
```

### Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { /* resource data */ },
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-readable error message"
}
```

### Authentication Mechanism

- **Method:** JWT (JSON Web Tokens)
- **Flow:** Login → Receive token → Include in Authorization header
- **Header Format:** `Authorization: Bearer <token>`
- **Storage:** JWT secret in environment variable
- **Token Expiry:** 24 hours (configurable)

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Shared components (Navbar, Footer)
│   │   ├── auth/            # Auth-related components
│   │   ├── destinations/    # Destination components
│   │   ├── trips/           # Trip components
│   │   ├── bookings/        # Booking components
│   │   ├── budget/          # Budget components
│   │   ├── admin/           # Admin components
│   │   └── forms/           # Form components
│   ├── pages/               # Page components
│   │   ├── public/          # Public pages (Home, Login, Register)
│   │   ├── user/            # User pages (Dashboard, Trips, etc.)
│   │   └── admin/           # Admin pages
│   ├── services/            # API communication
│   │   └── api.js          # Centralized API client
│   ├── context/             # React Context for state management
│   │   ├── AuthContext.jsx
│   │   ├── TripContext.jsx
│   │   └── UIContext.jsx
│   ├── hooks/               # Custom React hooks
│   ├── assets/              # Images, icons, fonts
│   ├── App.jsx              # Root component
│   ├── main.jsx             # Entry point
│   ├── index.css            # Global styles
│   └── .env.example         # Environment variable template
├── public/                  # Static files
├── vite.config.js          # Vite configuration
├── package.json            # Dependencies
└── tailwind.config.js      # Tailwind CSS configuration
```

### Key Features

**Component-Based Architecture:**
- Reusable UI components (DestinationCard, TripCard, etc.)
- Container/Presentational pattern
- Props-based configuration

**State Management:**
- Context API for global state
- React Hooks for local component state
- Authentication state persistence in localStorage

**Routing:**
- React Router v6
- Protected routes for authenticated users
- Admin routes with role-based access
- Nested route structure

**API Communication:**
- Centralized Axios service (single point of API URLs)
- Request/response interceptors
- Error handling middleware
- Loading state management

**Styling:**
- Tailwind CSS utility classes
- Responsive design (mobile-first)
- CSS Grid and Flexbox layouts
- Custom theme configuration

**User Experience:**
- Loading spinners
- Error messages
- Form validation feedback
- Toast notifications
- Mobile-responsive navigation

---

## Backend Architecture

### Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration (DB, env vars)
│   ├── database.py          # Database connection setup
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── destination.py
│   │   ├── trip.py
│   │   ├── itinerary.py
│   │   ├── booking.py
│   │   ├── expense.py
│   │   ├── review.py
│   │   └── user_preference.py
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── destination.py
│   │   └── ... (one per domain)
│   ├── routes/              # API endpoint routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── destinations.py
│   │   ├── recommendations.py
│   │   ├── trips.py
│   │   ├── itineraries.py
│   │   ├── bookings.py
│   │   ├── expenses.py
│   │   ├── reviews.py
│   │   ├── weather.py
│   │   ├── places.py
│   │   ├── currency.py
│   │   └── admin.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── recommendation_service.py
│   │   ├── itinerary_service.py
│   │   ├── booking_service.py
│   │   ├── expense_service.py
│   │   ├── weather_service.py
│   │   ├── places_service.py
│   │   └── currency_service.py
│   ├── ai/                  # AI/ML logic
│   │   ├── __init__.py
│   │   ├── recommendation_engine.py  # Scikit-learn models
│   │   └── itinerary_generator.py    # LLM integration
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   ├── security.py      # Password hashing, JWT
│   │   ├── validators.py    # Input validation
│   │   └── helpers.py       # Helper functions
│   ├── middleware/          # Custom middleware
│   │   └── __init__.py
│   └── .env.example         # Environment template
├── tests/                   # Unit and integration tests
├── requirements.txt         # Python dependencies
└── .gitignore
```

### Key Principles

**Modular Architecture:**
- Separation of concerns
- Routes → Services → Database
- AI logic isolated
- External APIs abstracted

**Security:**
- No hardcoded credentials
- Environment variables for secrets
- Password hashing with bcrypt
- JWT for authentication
- Input validation

**Error Handling:**
- Custom exceptions
- Proper HTTP status codes
- Meaningful error messages
- Logging

**Database Operations:**
- SQLAlchemy ORM
- Connection pooling
- Query optimization
- Transaction management

---

## AI/ML Components

### Recommendation System Architecture

**Approach:** Content-Based Filtering

**Input Processing:**
1. Extract user preferences (budget, climate, activities, category)
2. Retrieve available destinations
3. Extract destination features
4. Convert to numerical vectors

**Similarity Calculation:**
1. Cosine similarity between user vector and destination vectors
2. Budget compatibility check
3. Category matching
4. Climate matching
5. Activity overlap calculation

**Ranking & Scoring:**
1. Weighted combination of similarity scores
2. Apply budget constraints
3. Penalize over-budget destinations
4. Sort by match score (descending)

**Explainability:**
- Generate human-readable reasons for each recommendation
- Example: "Manali recommended because: matches adventure preference (0.92), cool climate (0.88), trekking activity (0.95), within budget (50000 INR)"

**Implementation Location:** `backend/app/ai/recommendation_engine.py`

### Itinerary Generation System

**Approach:** LLM-Based (Google Gemini API)

**Input:**
- Destination name
- Number of days
- Budget
- User interests
- Travel companions
- Preferred activities

**Output Generation:**
1. Format prompt with user inputs
2. Call Gemini API
3. Parse LLM response
4. Validate structure
5. Store in database

**Validation:**
- Ensure day-wise breakdown
- Verify activity feasibility
- Check cost estimates
- Validate location accuracy

**Error Handling:**
- Graceful fallback if API fails
- Retry mechanism
- User-friendly error messages

**Implementation Location:** `backend/app/ai/itinerary_generator.py`

---

## External API Integrations

### Weather API Integration

**Purpose:** Fetch weather and forecasts for destinations

**Approach:**
- Use OpenWeatherMap or similar
- API key in backend environment variables
- Never expose to frontend

**Data Transformation:**
- Convert API response to standard format
- Cache results (30 minutes TTL)
- Handle missing data gracefully

**Implementation Location:** `backend/app/services/weather_service.py`

### Maps & Places API Integration

**Purpose:** Tourist attractions and location information

**Approach:**
- Use Google Maps API or similar
- Backend queries only
- Secure API key handling

**Data Features:**
- Tourist place names
- Categories
- Ratings and reviews
- Address information
- Open/closed status

**Implementation Location:** `backend/app/services/places_service.py`

### Currency Conversion API

**Purpose:** Multi-currency support for budgeting

**Approach:**
- Use exchangerate-api.com or similar
- Real-time conversion rates
- Cache rates (24-hour TTL)

**Response Format:**
- Source currency
- Target currency
- Original amount
- Converted amount
- Exchange rate
- Timestamp

**Implementation Location:** `backend/app/services/currency_service.py`

---

## Security Architecture

### Authentication Flow

```
1. User Registration:
   - Submit email, password, name
   - Validate input
   - Hash password with bcrypt
   - Store in database
   - Return success

2. User Login:
   - Submit email, password
   - Verify email exists
   - Verify password hash
   - Generate JWT token
   - Return token + user info

3. Authenticated Request:
   - Include Authorization: Bearer <token>
   - Backend validates token
   - Extract user_id from token
   - Proceed with request
```

### Authorization Levels

**Public Access (No Auth):**
- GET /api/health
- GET /api/destinations (list)
- GET /api/destinations/{id} (details)
- GET /api/destinations/{id}/reviews

**User Access (Authenticated):**
- All user-owned resources (trips, bookings, expenses)
- Personal profile endpoints
- Recommendations

**Admin Access (Admin Role):**
- POST/PUT/DELETE /api/destinations
- Admin dashboard endpoints
- User management
- Analytics endpoints

### Password Security

- Minimum 8 characters
- Hash with bcrypt (rounds: 12)
- Never store plaintext
- No password recovery via email (redesign)

### Secret Management

**Environment Variables (.env):**
```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=<strong-random-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

GEMINI_API_KEY=<api-key>
WEATHER_API_KEY=<api-key>
MAPS_API_KEY=<api-key>
CURRENCY_API_KEY=<api-key>

CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### CORS Configuration

- Restrict to frontend domain
- Allow credentials
- Specific headers and methods

### Input Validation

- Pydantic schemas for all inputs
- Type checking
- Range validation
- Format validation (email, dates, etc.)
- SQL injection prevention (via ORM)

---

## Development Phases

### Phase 1: Architecture & Planning ✓
**Deliverable:** PROJECT_ARCHITECTURE.md

### Phase 2: Project Setup
**Tasks:**
- Initialize React + Vite frontend
- Initialize FastAPI backend
- Setup PostgreSQL locally
- Create CORS configuration
- Create environment variable files
- Implement health check endpoint

### Phase 3: Database Setup
**Tasks:**
- Define SQLAlchemy models
- Create relationships
- Set up database migrations
- Create seed data script
- Test database connectivity

### Phase 4: Backend REST APIs
**Tasks:**
- Implement CRUD routes for all entities
- Add request/response schemas
- Implement business logic services
- Add error handling
- Add input validation

### Phase 5: Authentication & Authorization
**Tasks:**
- Implement user registration
- Implement user login with JWT
- Add protected route decorators
- Implement role-based access
- Test authentication flow

### Phase 6: Frontend Development
**Tasks:**
- Create page structure
- Build reusable components
- Implement routing
- Connect to backend APIs
- Add authentication UI
- Implement state management

### Phase 7: AI Recommendation System
**Tasks:**
- Implement recommendation engine
- Train on destination data
- Create recommendation API endpoint
- Add explainability
- Test with real data

### Phase 8: AI Itinerary Generation
**Tasks:**
- Integrate Gemini API
- Implement prompt engineering
- Create itinerary endpoint
- Add validation logic
- Store in database
- Error handling

### Phase 9: External APIs Integration
**Tasks:**
- Integrate weather API
- Integrate maps/places API
- Integrate currency API
- Add caching where needed
- Error handling
- Test all integrations

### Phase 10: Booking, Budget & Admin
**Tasks:**
- Implement booking management
- Implement budget tracking
- Implement admin dashboard
- Add analytics
- Add destination management

### Phase 11: Testing, Debugging & Documentation
**Tasks:**
- Write unit tests
- Write integration tests
- Debug issues
- Complete documentation
- Prepare deployment

---

## Directory Structure (Complete)

```
AI-Assited-coding/
├── docs/
│   ├── PROJECT_ARCHITECTURE.md     (This file)
│   ├── DATABASE.md                 (Phase 3)
│   ├── API_DOCUMENTATION.md        (Phase 4)
│   ├── AUTHENTICATION.md           (Phase 5)
│   ├── AI_RECOMMENDATION.md        (Phase 7)
│   ├── AI_ITINERARY.md            (Phase 8)
│   ├── EXTERNAL_APIS.md           (Phase 9)
│   ├── ADMIN_AND_MANAGEMENT.md    (Phase 10)
│   └── DEPLOYMENT.md              (Phase 11)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── auth/
│   │   │   ├── destinations/
│   │   │   ├── trips/
│   │   │   ├── bookings/
│   │   │   ├── budget/
│   │   │   ├── admin/
│   │   │   └── forms/
│   │   ├── pages/
│   │   │   ├── public/
│   │   │   ├── user/
│   │   │   └── admin/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── .env.example
│   ├── public/
│   ├── vite.config.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── .gitignore
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── destination.py
│   │   │   ├── trip.py
│   │   │   ├── itinerary.py
│   │   │   ├── booking.py
│   │   │   ├── expense.py
│   │   │   ├── review.py
│   │   │   └── user_preference.py
│   │   ├── schemas/
│   │   │   └── (request/response models)
│   │   ├── routes/
│   │   │   └── (API endpoints)
│   │   ├── services/
│   │   │   └── (business logic)
│   │   ├── ai/
│   │   │   ├── recommendation_engine.py
│   │   │   └── itinerary_generator.py
│   │   ├── utils/
│   │   ├── middleware/
│   │   └── .env.example
│   ├── tests/
│   ├── requirements.txt
│   └── .gitignore
│
├── README.md
└── .gitignore
```

---

## Key Design Decisions

### 1. Monolithic vs Microservices
**Decision:** Modular Monolithic Architecture
**Reasoning:** Simpler deployment, easier debugging, sufficient for project scope

### 2. Frontend Framework
**Decision:** React.js with Vite
**Reasoning:** Modern, componentized, large ecosystem, fast build times

### 3. Backend Framework
**Decision:** FastAPI
**Reasoning:** Modern, async-capable, auto-documentation, fast, Pythonic

### 4. Database
**Decision:** PostgreSQL with SQLAlchemy
**Reasoning:** Robust relational database, ORM abstraction, complex relationships needed

### 5. AI Approach
**Decision:** Content-Based Filtering (not Deep Learning)
**Reasoning:** Simpler implementation, explainable, sufficient for use case

### 6. Itinerary Generation
**Decision:** LLM API (Gemini)
**Reasoning:** Fast, professional-quality output, no training needed

### 7. Authentication
**Decision:** JWT-based
**Reasoning:** Stateless, scalable, industry standard

---

## Performance Considerations

### Frontend
- Lazy loading of pages
- Image optimization
- Code splitting with React Router
- Caching with Axios interceptors

### Backend
- Database connection pooling
- Query optimization (eager/lazy loading)
- Caching for external APIs
- Rate limiting on endpoints

### Database
- Indexing on frequently queried columns
- Proper relationship design
- Query analysis and optimization

---

## Scalability Roadmap

**Current (Phase 1-11):** Monolithic application

**Future Enhancements:**
- Microservices separation
- Caching layer (Redis)
- Search engine (Elasticsearch)
- Message queue (RabbitMQ)
- CDN for static assets
- Horizontal scaling

---

## Testing Strategy

### Frontend Testing
- Component testing with Vitest/React Testing Library
- Integration testing
- E2E testing with Cypress/Playwright

### Backend Testing
- Unit tests with pytest
- Integration tests with test database
- API endpoint testing

### Database Testing
- Migration testing
- Data integrity testing

---

## Deployment Strategy

**Frontend:**
- Build with Vite
- Deploy to Vercel/Netlify/GitHub Pages

**Backend:**
- Docker containerization
- Deploy to Heroku/Railway/DigitalOcean

**Database:**
- Managed PostgreSQL (AWS RDS, Supabase, etc.)

---

## Documentation Maintenance

Update documentation after each phase:
- Database schema changes → DATABASE.md
- New APIs → API_DOCUMENTATION.md
- Security updates → AUTHENTICATION.md
- AI improvements → AI_RECOMMENDATION.md, AI_ITINERARY.md

---

## Conclusion

This architecture provides a professional, scalable foundation for an AI-powered tourism platform. Each component is modular, allowing independent development and testing. The phased approach ensures incremental progress with functional applications at each stage.

**Ready for Phase 2: Project Setup** when instructed.
