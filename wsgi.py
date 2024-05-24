from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blockchain')
def blockchain():
    return render_template('blockchain.html')

@app.route('/transaction')
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