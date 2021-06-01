#from datetime import datetime
from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm

#main = Blueprint('main', __name__)

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/login')
def login():
 return render_template('login.html')