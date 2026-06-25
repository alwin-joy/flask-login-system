from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask App
app = Flask(__name__)

# Secret Key for Sessions
app.config['SECRET_KEY'] = 'secret123'

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize Database
db = SQLAlchemy(app)

# User Table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    # Automatically verified
    verified = db.Column(db.Boolean, default=True)


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

        # Check if email already exists
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
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # Find User
        user = User.query.filter_by(email=email).first()

        # Check Password
        if user and check_password_hash(user.password, password):

            # Create Session
            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('dashboard'))

        return "Invalid Email or Password"

    return render_template('login.html')


# Dashboard Page
@app.route('/dashboard')
def dashboard():

    # Check if logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return f'''
    <h1>Welcome {session["username"]}!</h1>

    <br>

    <a href="/logout">Logout</a>
    '''


# Logout Route
@app.route('/logout')
def logout():

    # Clear Session
    session.clear()

    return redirect(url_for('login'))


# Run Flask App
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)