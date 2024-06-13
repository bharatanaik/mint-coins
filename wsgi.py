import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, flash, url_for
import pyrebase
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firebase_uid = db.Column(db.String(120), unique=True, nullable=False)

    @staticmethod
    def get_by_firebase_uid(firebase_uid):
        return User.query.filter_by(firebase_uid=firebase_uid).first()

    @staticmethod
    def create_user(username, email, firebase_uid):
        new_user = User(username=username, email=email, firebase_uid=firebase_uid)
        db.session.add(new_user)
        db.session.commit()
        return new_user

with app.app_context():
    db.create_all()

load_dotenv()
config = {
    "apiKey": os.getenv('APIKEY'),
    "authDomain": os.getenv('AUTHDOMAIN'),
    "storageBucket": os.getenv('STORAGEBUCKET'),
    "projectId": os.getenv('PROJECTID'),
    "messagingSenderId": os.getenv('MESSAGINGSENDERID'),
    "appId": os.getenv('APPID'),
    "measurementId": os.getenv('MEASUREMENTID'),
    "databaseURL": ""
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            new_user = User(username=username, email=email, firebase_uid=user['localId'])
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
        return redirect(url_for('register'))
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            firebase_uid = user['localId']
            existing_user = User.get_by_firebase_uid(firebase_uid)
            if not existing_user:
                existing_user = User.create_user(username='default', email=email, firebase_uid=firebase_uid)
            login_user(existing_user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return redirect(url_for('login'))
    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/blockchain')
@login_required
def blockchain():
    return render_template('blockchain.html')


@app.route('/transaction')
@login_required
def transaction():
    return render_template('transaction.html')


@app.route('/block/<hash>')
def block(hash):
    return render_template('block.html')


@app.route('/mining')
def mining():
    return render_template('mining.html')


@app.route('/register-node')
def register_node():
    return render_template('register-node.html')

if __name__ == "__main__":
    app.run(debug=True)
