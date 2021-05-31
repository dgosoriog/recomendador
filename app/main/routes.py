#from datetime import datetime
from flask import render_template, session, redirect, url_for,Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
 #return redirect(url_for('.index'))
 #si utilizo este return en otra ruta, añadir 'main' asi: url_for('main.index')
 return render_template('index.html')
 #form=form, name=session.get('name'),
 #known=session.get('known', False),
 #current_time=datetime.utcnow())
@main.route('/login')
def login():
 #return redirect(url_for('.index'))
 #si utilizo este return en otra ruta, añadir 'main' asi: url_for('main.index')
 return render_template('login.html')