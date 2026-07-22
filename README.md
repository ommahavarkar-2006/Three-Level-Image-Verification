# SecureVision — Three-Level Image Password Authentication System

A modern cybersecurity-focused authentication platform that verifies users through three independent security layers: traditional password, graphical image password sequence, and visual security challenge.

## Features

- **Three-Level Authentication**: Password + Image Sequence + Visual Challenge
- **Real-time Password Strength Indicator**: Visual feedback during registration
- **Image Password System**: Select 3-5 images in sequence as a visual password
- **Visual Security Challenge**: CAPTCHA-like image classification challenge
- **Security Dashboard**: Monitor authentication activity with Chart.js visualizations
- **Authentication History**: Filterable, paginated log of all auth events
- **Security Overview**: Real-time security score and status indicators
- **Account Protection**: Rate limiting, failed attempt tracking, automatic lockout
- **CSRF Protection**: All forms protected against cross-site request forgery
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Notification System**: localStorage-based UI notifications (no database table)
- **Professional UI**: Dark cybersecurity theme with glassmorphism cards

## Security Architecture

```
Level 1: Email + Password (Werkzeug hashed, rate-limited)
    ↓
Level 2: Image Password Sequence (order-dependent, stored securely)
    ↓
Level 3: Visual Challenge (backend-validated image classification)
    ↓
Dashboard Access Granted
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13+, Flask |
| Database | MySQL + SQLAlchemy ORM |
| Auth | Flask-Login, Werkzeug, Flask-WTF (CSRF) |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Charts | Chart.js |
| Security | Flask-Limiter, Session management, Password hashing |
| Deployment | Gunicorn, Render-ready |

## Project Structure

```
securevision/
├── app.py                  # Entry point
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── Procfile                # Deployment config
├── runtime.txt             # Python version
├── database.sql            # MySQL schema
├── app/
│   ├── __init__.py         # App factory
│   ├── extensions.py       # Flask extensions
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   ├── image_password.py
│   │   ├── authentication_log.py
│   │   └── security_challenge.py
│   ├── auth/               # Authentication blueprint
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py
│   ├── dashboard/          # Dashboard blueprint
│   │   └── routes.py
│   ├── security/           # Security blueprint
│   │   ├── routes.py
│   │   └── utils.py
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, images
```

## Installation

### Prerequisites

- Python 3.13+
- MySQL 8.0+

### Setup

1. **Clone the repository:**
```bash
git clone <repo-url>
cd securevision
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment:**
```bash
cp .env.example .env
```
Edit `.env` with your MySQL credentials and a secure `SECRET_KEY`.

6. **Create MySQL database:**
```bash
mysql -u root -p < database.sql
```

7. **Run the application:**
```bash
python app.py
```

8. **Open in browser:**
```
http://localhost:5000
```

## Deploy on Render

1. Push code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set environment variables from `.env.example`
5. Add a MySQL database on Render
6. Deploy — Render will use `Procfile` and `runtime.txt` automatically

## Demo Credentials

| Field | Value |
|-------|-------|
| Email | demo@securevision.com |
| Password | Demo@12345 |
| Image Password | Mountain → Camera → Ocean |

## Environment Variables

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Flask secret key (use a strong random string) |
| DATABASE_URL | Full MySQL connection URI |
| MYSQL_HOST | MySQL host (default: localhost) |
| MYSQL_PORT | MySQL port (default: 3306) |
| MYSQL_USER | MySQL username |
| MYSQL_PASSWORD | MySQL password |
| MYSQL_DATABASE | Database name |
| FLASK_ENV | `development` or `production` |

## Screenshots

> Add screenshots here

## Future Improvements

- Two-factor authentication via email/SMS
- OAuth2 social login integration
- Passwordless authentication option
- Advanced threat detection and anomaly alerts
- Multi-device session management
- Audit log export functionality
- Dark/Light theme toggle
- Profile picture upload

## License

This project is created for educational and portfolio purposes.
