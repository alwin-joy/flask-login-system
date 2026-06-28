from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random, re
import os

load_dotenv()

# Create Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Session Security
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Gmail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


# Initialize Database
db = SQLAlchemy(app)

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

# Initialize Mail
mail = Mail(app)

# Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

# Temporary OTP Storage
otp_storage = {}

# User Table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    verified = db.Column(db.Boolean, default=True)

# Create Tables
with app.app_context(): 
    db.create_all()


# Home Page
@app.route('/')
def home():

    return redirect(url_for('register'))


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        checks = [
            (r".{8,}", "Minimum 8 characters required"),
            (r"[A-Z]", "Add an uppercase letter"),
            (r"[a-z]", "Add a lowercase letter"),
            (r"[0-9]", "Add a number"),
            (r"[!@#$%^&*]", "Add a special character")
        ]

        for pattern, message in checks:
            if not re.search(pattern, password):
                return message

        # Check Existing User
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        # Hash Password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create User
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            verified=True
        )

        # Save User
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # Find User
        user = User.query.filter_by(email=email).first()

        # Check Password
        if user and bcrypt.check_password_hash(user.password, password):

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store OTP
            otp_storage[email] = otp

            # Send OTP Email
            msg = Message(
                'Your OTP Code',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f'''
Your OTP Code is:

{otp}

Do not share this OTP with anyone.
'''

            mail.send(msg)

            # Temporary Session
            session['temp_email'] = email

            return redirect(url_for('verify_otp'))

        return "Invalid Email or Password"

    return render_template('login.html')


# OTP Verification Page
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():

    if request.method == 'POST':

        entered_otp = request.form['otp']

        email = session.get('temp_email')

        if not email:
            return redirect(url_for('login'))

        real_otp = otp_storage.get(email)

        # Verify OTP
        if real_otp and str(real_otp) == entered_otp:

            user = User.query.filter_by(email=email).first()

            # Create Login Session
            session['user_id'] = user.id
            session['username'] = user.username

            # Remove OTP After Verification
            otp_storage.pop(email)

            return redirect(url_for('dashboard'))

        return "Invalid OTP"

    return render_template('otp.html')


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


# Logout
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# Run Flask App
if __name__ == '__main__':

    app.run(debug=True)