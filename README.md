# Flask Login System

## Project Description

This project is a Flask-based Login and Registration Portal developed using Python and SQLite. The application allows users to register, log in securely, verify credentials using OTP authentication, maintain login sessions, and log out safely.

The system also includes password hashing for secure password storage and rate limiting to prevent brute-force attacks.

---

## Features

* User Registration
* Secure Password Hashing
* Login Authentication
* OTP Verification
* Session Management
* Logout Functionality
* SQLite Database Integration
* Rate Limiting for Security

---

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Limiter
* SQLite
* HTML
* CSS
* Werkzeug Security
* PyOTP

---

## Project Structure

```plaintext
Flask-login-system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── users.db
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── otp.html
│   └── verify_success.html
│
├── screenshots/
│   ├── dashboard_page.png.png
│   ├── login_page.png.png
│   ├── otp_page.png.png
│   └── register_page.png.png
│
└── myenv/
```

---

## Installation Instructions

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/flask-login-system.git
```

### 2. Open Project Folder

```bash
cd flask-login-system
```

### 3. Create Virtual Environment

```bash
python -m venv myenv
```

### 4. Activate Virtual Environment

#### Windows

```bash
.\myenv\Scripts\activate
```

### 5. Install Required Packages

```bash
python -m pip install -r requirements.txt
```

---

## Usage Instructions

### Run Flask Application

```bash
python app.py
```

### Open Browser

```plaintext
http://127.0.0.1:5000
```

---

## Workflow

1. User registers an account.
2. Password is securely hashed and stored in SQLite database.
3. User logs in using email and password.
4. System generates OTP verification code.
5. User enters OTP successfully.
6. Session is created.
7. User accesses dashboard.
8. User logs out securely.

---

## Security Features

* Password Hashing using Werkzeug
* Session-Based Authentication
* OTP Verification
* Rate Limiting Protection

---

## Screenshots

### Register Page
![Register Page](screenshots/register_page.png)

### Login Page
![Login Page](screenshots/login_page.png)

### OTP Page
![OTP Page](screenshots/otp_page.png)

### Dashboard Page
![Dashboard Page](screenshots/dashboard_page.png)

---

## Live Demo

Local Host URL:

```plaintext
http://127.0.0.1:5000
```

GitHub Repository:

```plaintext
https://github.com/yourusername/flask-login-system
```

---

## Author

Alwin Joy
