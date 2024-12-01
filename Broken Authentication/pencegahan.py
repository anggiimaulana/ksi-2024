from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inisialisasi Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # Maksimal 5 permintaan per menit
)

# Konfigurasi login
MAX_ATTEMPTS = 5  # Maksimal percobaan gagal
LOCKOUT_DURATION = timedelta(minutes=1)  # Blokir selama 1 menit

# Model database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)  # Jumlah gagal login
    lockout_time = db.Column(db.DateTime, nullable=True)  # Waktu pemblokiran

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", override_defaults=False)  # Terapkan rate limiting
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            if user.lockout_time and datetime.now() < user.lockout_time:
                flash('Account is temporarily locked. Try again later.', 'danger')
                return render_template('login.html')

            if check_password_hash(user.password, password):
                user.failed_attempts = 0
                user.lockout_time = None
                db.session.commit()
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                user.failed_attempts += 1
                if user.failed_attempts >= MAX_ATTEMPTS:
                    user.lockout_time = datetime.now() + LOCKOUT_DURATION
                db.session.commit()
                flash('Invalid credentials.', 'danger')
        else:
            flash('User not found.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/initdb')
def initdb():
    db.create_all()
    return "Database initialized successfully!"

if __name__ == '__main__':
    app.run(debug=True)
