<div align="center">

# 🛡️ SecureVision

### Three-Level Image Password Authentication System

**A cybersecurity-focused authentication platform combining traditional passwords, graphical authentication, and visual security challenges.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-00C896?style=for-the-badge&logo=render&logoColor=white)](https://three-level-image-verification.onrender.com)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ommahavarkar-2006/Three-Level-Image-Verification)

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Security](https://img.shields.io/badge/Security-Focused-00C896?style=flat-square&logo=hackthebox&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-blue?style=flat-square)

</div>

---

## 📖 Table of Contents

- [About](#-about-securevision)
- [Authentication Flow](#-three-level-authentication-flow)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#️-project-structure)
- [Local Installation](#️-local-installation)
- [Production Deployment](#-production-deployment)
- [Demo Account](#-demo-account)
- [Security Architecture](#-security-architecture)
- [Project Highlights](#-project-highlights)
- [Future Improvements](#-future-improvements)
- [Developer](#-developer)
- [License](#-license)

---

## 🔐 About SecureVision

**SecureVision** is a full-stack cybersecurity-focused authentication platform that implements a **three-level authentication architecture**.

Unlike traditional authentication systems that depend only on an email and password, SecureVision introduces two additional graphical and visual verification layers to create a stronger authentication workflow. Users must successfully complete all three security levels before accessing the protected dashboard.

<p align="center">
  <a href="https://three-level-image-verification.onrender.com">
    <img src="https://img.shields.io/badge/OPEN%20LIVE%20APPLICATION-00C896?style=for-the-badge&logo=render&logoColor=white">
  </a>
</p>

---

## 🔒 Three-Level Authentication Flow

```text
┌───────────────────────────────────────────┐
│         LEVEL 1 · CREDENTIAL AUTH          │
│                                             │
│   Email + Password                         │
│   Werkzeug Password Hashing                │
│   Rate Limiting                            │
└──────────────────────┬──────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────┐
│         LEVEL 2 · IMAGE PASSWORD           │
│                                             │
│   Graphical Password Sequence              │
│   3–5 Images                               │
│   Order-Dependent Verification             │
└──────────────────────┬──────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────┐
│         LEVEL 3 · VISUAL CHALLENGE         │
│                                             │
│   Image Classification                     │
│   Backend Validation                       │
│   Security Challenge                       │
└──────────────────────┬──────────────────────┘
                        │
                        ▼
                ✅ ACCESS GRANTED
```

---

## ✨ Key Features

### 🛡️ Three-Level Authentication
- Email and password authentication
- Graphical image password sequence
- Visual image classification challenge
- Backend validation for every authentication layer
- Dashboard access only after successful verification

### 🔑 Secure Authentication
- Werkzeug password hashing
- CSRF protection using Flask-WTF
- Secure session management
- Rate limiting
- Failed login attempt tracking
- Automatic account lockout
- Session expiration
- HTTPOnly cookies
- SameSite cookie policy

### 🖼️ Image Password Authentication
Users can create a graphical password by selecting a sequence of images.

**Example:**

```
🏔️ Mountain  →  📷 Camera  →  🌊 Ocean
```

The user must select the same images in the correct order during authentication — an additional graphical authentication layer beyond traditional passwords.

### 🧩 Visual Security Challenge
The third authentication layer requires users to complete a visual image classification challenge, validated on the backend before dashboard access is granted.

### 📊 Security Dashboard
- Authentication activity monitoring
- Security overview
- Authentication history
- Login Event tracking
- Security score
- Account security status
- Chart.js data visualizations

### 📱 Responsive Design
Works seamlessly across 💻 Desktop, 📱 Mobile, and 📟 Tablet.

### 🎨 Modern Cybersecurity Interface
- Dark cybersecurity theme
- Glassmorphism UI
- Responsive cards
- Interactive components
- Modern authentication pages
- Real-time feedback
- Notification system
- Professional dashboard interface

---

## 🧰 Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.13+ |
| Backend Framework | Flask |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Password Security | Werkzeug |
| CSRF Protection | Flask-WTF |
| Rate Limiting | Flask-Limiter |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Bootstrap 5 |
| Data Visualization | Chart.js |
| Database Hosting | Aiven Cloud |
| Application Hosting | Render |
| Production Server | Gunicorn |

---

## 🏗️ Project Structure

```text
securevision/
│
├── app.py
├── wsgi.py
├── config.py
├── requirements.txt
├── .env.example
├── Procfile
├── runtime.txt
├── database.sql
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── image_password.py
│   │   ├── authentication_log.py
│   │   └── security_challenge.py
│   │
│   ├── auth/
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py
│   │
│   ├── dashboard/
│   │   └── routes.py
│   │
│   ├── security/
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── templates/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
└── README.md
```

---

## ⚙️ Local Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ommahavarkar-2006/Three-Level-Image-Verification.git
cd Three-Level-Image-Verification
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secure-secret-key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=securevision
```

> ⚠️ For production deployment, use a strong randomly generated secret key.

### 6️⃣ Create the Database
```bash
mysql -u root -p < database.sql
```

### 7️⃣ Run the Application
```bash
python app.py
```

Open the application at **http://localhost:5000**

---

## 🌐 Production Deployment

SecureVision is deployed using the following architecture:

```text
                    USER
                      │
                      ▼
              ┌─────────────────┐
              │      RENDER      │
              │                  │
              │   Flask App      │
              │   Gunicorn       │
              │   HTTPS          │
              └────────┬─────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   AIVEN CLOUD    │
              │                  │
              │  MySQL Database  │
              └─────────────────┘
```

### Production Services

| Service | Technology |
|---|---|
| Application Hosting | Render |
| Database Hosting | Aiven Cloud |
| Backend | Flask |
| Production Server | Gunicorn |
| Database | MySQL |
| ORM | SQLAlchemy |
| Security | HTTPS, CSRF Protection, Rate Limiting |

---

## 🧪 Demo Account

The deployed application includes a demo account for testing.

| Field | Value |
|---|---|
| Email | `demo@securevision.com` |
| Password | `demo123` |

> The image password and visual security challenge must be completed according to the configured demo account data.

---

## 🔒 Security Architecture

### Password Hashing
Passwords are never stored as plain text.

```text
Plain Password
      │
      ▼
Werkzeug Password Hashing
      │
      ▼
Secure Password Hash
      │
      ▼
Database
```

### CSRF Protection
Protected forms use CSRF tokens to help prevent unauthorized cross-site requests.

### Rate Limiting
Rate limiting helps protect authentication endpoints from excessive repeated requests and brute-force attempts.

### Account Lockout
Multiple failed authentication attempts can trigger temporary account protection.

### Secure Sessions
- HTTPOnly cookies
- SameSite cookie policy
- Secure cookies in production
- Configurable session lifetime

---

## 📈 Project Highlights

- ✅ Built a complete full-stack cybersecurity application
- ✅ Implemented a three-level authentication architecture
- ✅ Designed graphical image password authentication
- ✅ Implemented visual image classification challenges
- ✅ Integrated MySQL with SQLAlchemy ORM
- ✅ Implemented CSRF protection
- ✅ Implemented rate limiting
- ✅ Added secure password hashing
- ✅ Added account lockout protection
- ✅ Built authentication history tracking
- ✅ Created security analytics dashboard
- ✅ Deployed the application to Render
- ✅ Integrated Aiven Cloud MySQL
- ✅ Configured Gunicorn for production deployment

---

## 🔮 Future Improvements

- 🔐 Two-Factor Authentication using Email/SMS
- 🌐 OAuth2 Social Login
- 🔑 Passwordless Authentication
- 🤖 AI-Based Threat Detection
- 📱 Multi-Device Session Management
- 📄 Audit Log Export
- 🔔 Real-Time Security Alerts
- 👤 Profile Image Upload
- 🌓 Dark/Light Theme Toggle
- 🛡️ Advanced Anomaly Detection

---

## 👨‍💻 Developer

**Om Mahavarkar**

*B.Sc. Information Technology Student | Full Stack Developer | Cybersecurity Enthusiast*

I enjoy building practical full-stack applications that combine secure backend architecture, database design, modern user interfaces, and real-world problem solving.

### 🔗 Links

- 💻 [GitHub Repository](https://github.com/ommahavarkar-2006/Three-Level-Image-Verification)
- 🚀 [Live Application](https://three-level-image-verification.onrender.com)
- 👤 [GitHub Profile](https://github.com/ommahavarkar-2006)

---

## 📄 License

This project was developed for educational, cybersecurity learning, and portfolio purposes.

<div align="center">

⭐ **If you found this project interesting, consider giving it a star!** ⭐

</div>
