# Flask Login System with OTP Verification

## Project Description

This project is a secure Flask-based Login and Registration System with OTP Email Verification.
It includes user authentication, session management, password hashing, rate limiting, CAPTCHA validation, and modern UI design.

Users can:

* Register an account
* Login securely
* Receive OTP verification through Gmail
* Access dashboard after verification
* Logout safely

---

# Features

* User Registration
* Secure Login System
* OTP Email Verification
* Password Hashing
* Session Management
* Rate Limiting Protection
* CAPTCHA Checkbox
* Strong Password Validation
* SQLite Database
* Modern Glassmorphism UI
* Environment Variable Security using `.env`

---

# Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Mail
* Flask-Limiter
* Flask-WTF
* SQLite
* HTML
* CSS
* dotenv

---

# Folder Structure

```plaintext
Flask-login-system/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── register.html
│   ├── login.html
│   ├── otp.html
│   └── dashboard.html
│
├── screenshots/
│   ├── register-page.png
│   ├── login-page.png
│   ├── otp-page.png
│   └── dashboard-page.png
│
├── instance/
│   └── users.db
│
├── .env
├── .gitignore
├── README.md
├── app.py
└── requirements.txt
```

---

# Installation

## Clone Repository

```bash
git clone <your-github-repository-link>
```

---

## Open Project Folder

```bash
cd Flask-login-system
```

---

## Create Virtual Environment

```bash
python -m venv myenv
```

---

## Activate Virtual Environment

### Windows

```bash
myenv\Scripts\activate
```

### Linux / Mac

```bash
source myenv/bin/activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file in the root folder.

Add:

```env
SECRET_KEY=secret123

MAIL_USERNAME=yourgmail@gmail.com

MAIL_PASSWORD=your_16_digit_app_password
```

---

# Run Flask App

```bash
python app.py
```

Open browser:

```plaintext
http://127.0.0.1:5000
```

---

# Security Features

* Password Hashing
* OTP Authentication
* Rate Limiting
* CSRF Protection
* Environment Variable Protection
* Session Security

---

# Screenshots


* [Register Page](screenshots/register-page.png)
* [Login Page](screenshots/login-page.png)
* [OTP Page](screenshots/otp-page.png)
* [Dashboard Page](screenshots/dashboard-page.png)

---

# Future Improvements

* Google reCAPTCHA
* Password Reset System
* Email Verification Links
* Cloud Deployment
* JWT Authentication

---

# Cloud Deployment

This Flask Login System is deployed using Railway cloud hosting.

## Deployment Features

* Public cloud hosting
* Automatic GitHub deployment
* Environment variable support
* Gunicorn production server
* HTTPS support

## Deployment Platform

* Railway

## Live Features Tested

* User Registration
* Login Authentication
* OTP Email Sending
* Dashboard Access
* Logout System

# Live Demo

🚀 Live Website:

https://flask-login-system-production-2f2a.up.railway.app


# Author

Alwin Joy

hello
