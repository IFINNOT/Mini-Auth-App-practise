from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入才能訪問此頁面'

#------------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') == 'on'
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
#------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)