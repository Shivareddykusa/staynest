# StayNest — Airbnb-Style Three-Tier Rental Application

StayNest is a lightweight, fully functional **three-tier vacation rental application** designed for modern cloud and DevOps workflows (Docker, Docker Compose, Git, Jenkins CI/CD, and AWS deployment).

---

## 🏗️ Architecture Overview

```text
               +------------------------------------+
               |      TIER 1: FRONTEND (Web)        |
               |  HTML5 + CSS3 + Vanilla JavaScript |
               |  Nginx Web Server (Port 80)        |
               +-----------------+------------------+
                                 |
                          HTTP / REST API
                          (JSON Payloads)
                                 |
                                 v
               +-----------------+------------------+
               |      TIER 2: BACKEND (API)         |
               |  Python 3.11 + Flask REST API      |
               |  JWT Auth + SQLAlchemy ORM (5000)  |
               +-----------------+------------------+
                                 |
                            PyMySQL / TCP
                                 |
                                 v
               +-----------------+------------------+
               |      TIER 3: DATABASE (Data)       |
               |  MySQL 8.0 Engine (Port 3306)      |
               |  Users, Properties, Bookings       |
               +------------------------------------+
```

### Communication Flow:
1. **Frontend to Backend**: The browser client (Vanilla JavaScript) interacts with Flask REST endpoints via standard asynchronous `fetch()` calls. No direct database connectivity exists on the frontend.
2. **Backend to Database**: Flask queries and persists relational entities via SQLAlchemy ORM using parameterized SQL queries over PyMySQL connector, securing against SQL injections.
3. **Authentication**: Stateless JSON Web Tokens (JWT) are issued upon login and sent via the `Authorization: Bearer <token>` header on protected routes.

---

## 📁 Repository Structure

```text
staynest/
├── backend/
│   ├── app.py                # Flask application factory & database init
│   ├── Dockerfile            # Python 3.11 container definition with Gunicorn
│   ├── models.py             # SQLAlchemy models (User, Property, Booking)
│   ├── requirements.txt      # Python backend dependencies
│   ├── routes.py             # REST API routes (Auth, Properties, Bookings)
│   └── .env.example          # Backend environment variables template
├── database/
│   └── init.sql              # MySQL DDL schema and initial seed data
├── frontend/
│   ├── css/
│   │   └── style.css         # Pure CSS styling & responsive layout system
│   ├── js/
│   │   ├── api.js            # Centralized API fetch layer
│   │   ├── auth.js           # JWT auth state & session manager
│   │   ├── bookings.js       # User reservations view logic
│   │   ├── host.js           # Property listing & host creation logic
│   │   ├── main.js           # Toast alerts & UI helper utilities
│   │   └── properties.js     # Home property catalog & search
│   ├── booking.html          # My Bookings page
│   ├── Dockerfile            # Nginx Alpine container definition
│   ├── host.html             # Host dashboard / Add Property page
│   ├── index.html            # Home page (Hero, search, featured stays)
│   ├── login.html            # User login page
│   ├── nginx.conf            # Nginx reverse proxy configuration
│   ├── property.html         # Property details & reservation calculator
│   └── register.html         # User registration page
├── .env.example              # Root environment template
├── .gitignore                # Git ignore rules
├── docker-compose.yml        # Multi-container orchestration (3 services)
└── README.md                 # Project documentation
```

---

## 🗄️ Database Schema

### 1. `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique User ID |
| `name` | VARCHAR(120) | NOT NULL | User Full Name |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | User Email Address |
| `password` | VARCHAR(255) | NOT NULL | Bcrypt Hashed Password |
| `role` | ENUM | NOT NULL, DEFAULT 'guest' | Role: 'guest' or 'host' |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp |

### 2. `properties`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique Property ID |
| `host_id` | INT | NOT NULL, FOREIGN KEY -> users(id) | Listing Host ID |
| `name` | VARCHAR(200) | NOT NULL | Property Title |
| `description`| TEXT | NULL | Detailed Overview |
| `location` | VARCHAR(255) | NOT NULL | City / Country |
| `price` | DECIMAL(10,2)| NOT NULL | Cost Per Night |
| `bedrooms` | INT | NOT NULL, DEFAULT 1 | Bedroom Count |
| `guests` | INT | NOT NULL, DEFAULT 2 | Max Guest Capacity |
| `image_url` | VARCHAR(500) | NULL | Banner Photo URL |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp |

### 3. `bookings`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique Booking ID |
| `user_id` | INT | NOT NULL, FOREIGN KEY -> users(id) | Guest ID |
| `property_id`| INT | NOT NULL, FOREIGN KEY -> properties(id)| Property ID |
| `check_in` | DATE | NOT NULL | Arrival Date |
| `check_out` | DATE | NOT NULL | Departure Date |
| `guests` | INT | NOT NULL, DEFAULT 1 | Number of Guests |
| `total_price`| DECIMAL(10,2)| NOT NULL | Calculated Total Cost |
| `status` | ENUM | DEFAULT 'pending' | 'pending', 'confirmed', 'cancelled' |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp |

---

## 🔌 REST API Reference

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/api/health` | No | System health check |
| `POST` | `/api/register` | No | Register a new user (guest or host) |
| `POST` | `/api/login` | No | Login and receive JWT access token |
| `GET` | `/api/me` | Yes (Bearer) | Get profile of logged-in user |
| `GET` | `/api/properties` | No | List all active property listings |
| `GET` | `/api/properties/<id>` | No | Get single property details |
| `POST` | `/api/properties` | Yes (Host) | Add a new property |
| `GET` | `/api/bookings` | Yes (Bearer) | Get all reservations for logged-in user |
| `POST` | `/api/bookings` | Yes (Bearer) | Book a stay for selected dates |

---

## 👥 Demo Credentials

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Host** | `host@staynest.com` | `password123` | Can view, search, book, and list new properties |
| **Guest** | `guest@staynest.com` | `password123` | Can view, search, and book properties |

---

## 🚀 Running with Docker Compose (Recommended)

To build and launch all 3 tiers with a single command:

```bash
docker compose up --build
```

### Application URLs:
- **Frontend**: [http://localhost](http://localhost) (Port 80)
- **Backend API**: [http://localhost:5000/api/health](http://localhost:5000/api/health)
- **MySQL Database**: `localhost:3306`

To shut down all containers and remove networks:
```bash
docker compose down
```

To remove containers and persistent volumes:
```bash
docker compose down -v
```

---

## 💻 Running Locally (Without Docker)

### Prerequisites:
- Python 3.9+
- MySQL Server 8.0+

### Step 1: Database Setup
1. Open MySQL terminal / Workbench and run `database/init.sql`:
   ```bash
   mysql -u root -p < database/init.sql
   ```

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`.

### Step 3: Frontend Setup
Open `frontend/index.html` in any modern web browser or serve with Python:
```bash
cd frontend
python -m http.server 8000
```
Open `http://localhost:8000` in your browser.
