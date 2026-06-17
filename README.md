# 🛡️ SecureShield AI

SecureShield AI is an AI-powered API security platform designed to protect modern AI applications from prompt injection attacks, sensitive data exposure, and malicious requests. The platform provides real-time threat monitoring, project-based security management, API key protection, and advanced analytics through an intuitive dashboard.

---

## 🚀 Features

### 🔐 Authentication & Security

* Secure User Registration & Login
* JWT-Based Authentication
* Protected Routes & Session Management
* Role-Based Access Control Ready

### 📂 Project Management

* Create and Manage Multiple Projects
* Project-Based Security Isolation
* Dedicated Security Monitoring per Project

### 🔑 API Key Management

* Secure API Key Storage
* Project-Specific API Keys
* API Key Tracking & Monitoring

### 🛡️ Prompt Security Scanner

* Prompt Injection Detection
* Sensitive Data Exposure Detection
* Threat Classification
* Risk Scoring System
* Real-Time Security Analysis

### 📊 Analytics Dashboard

* Threat Overview
* Security Metrics
* Request Monitoring
* Threat Activity Tracking
* Project-Level Analytics

### 📋 Threat Logging

* Detailed Threat History
* Timestamped Security Events
* Threat Severity Monitoring
* Security Audit Trail

### 📱 Mobile Ready

* Responsive Design
* Capacitor Android Support
* Mobile-Friendly Dashboard
* Cross-Platform Architecture

---

## 🏗️ Architecture

```text
SecureShield-AI/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── database/
│   ├── core/
│   ├── middleware/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── android/
│   └── package.json
│
└── README.md
```

---

## 💻 Tech Stack

### Frontend

* React
* Vite
* React Router
* Axios
* Tailwind CSS
* Capacitor

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Pydantic

### Security

* Prompt Injection Detection
* Threat Analysis Engine
* API Key Protection
* Security Logging

---

## ⚙️ Local Setup

### Clone Repository

```bash
git clone https://github.com/Tanish-2006/SecureShield-AI.git
cd SecureShield-AI
```

### Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 🌐 Deployment

### Backend

* Render

### Frontend

* Vercel

### Database

* PostgreSQL

---

## 🔮 Future Enhancements

* AI-Based Threat Intelligence
* Real-Time Alert System
* Advanced Threat Analytics
* Team Collaboration Features
* Security Reports Export
* Multi-Tenant Enterprise Support
* AI Security Recommendations

---

## 👨‍💻 Author

**Tanish Agrawal**

B.Tech (CSE - AI & ML)
MIET College, Meerut

Interested in:

* Artificial Intelligence
* Cybersecurity
* Backend Development
* AI Security Systems

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
