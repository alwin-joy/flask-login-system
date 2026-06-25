from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pyotp
import random

# Create Flask App
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = 'secret123'

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize Database
db = SQLAlchemy(app)

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


# Home Page
@app.route('/')
def home():

    return redirect(url_for('register'))


# Register Page
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check Existing User
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        # Hash Password
        hashed_password = generate_password_hash(password)

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

        # Verify Password
        if user and check_password_hash(user.password, password):

            # Generate 6-digit OTP
            otp = random.randint(100000, 999999)

            # Store OTP
            otp_storage[email] = otp

            print(f"OTP for {email}: {otp}")

            # Store Temporary Session
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

        if real_otp and str(real_otp) == entered_otp:

            user = User.query.filter_by(email=email).first()

            # Create Real Session
            session['user_id'] = user.id
            session['username'] = user.username

            # Remove OTP
            otp_storage.pop(email)

            return redirect(url_for('dashboard'))

        return "Invalid OTP"

    return render_template('otp.html')


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return f'''
    <h1>Welcome {session["username"]}!</h1>

    <br>

    <a href="/logout">Logout</a>
    '''


# Logout
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# Run Flask App
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)