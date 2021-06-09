from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_security import SQLAlchemyUserDatastore, Security, utils

from app import app, db, admin
from app.forms import LoginForm
from app.admin import UserAdmin
from app.models import Usuario, Rol

#main = Blueprint('main', __name__)

@app.route('/')
def index():
 return render_template('index.html')

@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Usuario.query.filter_by(email=form.email.data).first()
            if user and utils.verify_password(form.password.data,user.password):
                login_user(user, remember=form.remember.data)
                #next_page = request.args.get('next')
                if user.has_role('admin'):
                    return redirect(url_for('admin.home_admin'))
                elif user.has_role('tecnico'):
                    return redirect(url_for('home'))
                #return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Error al acceder. Por favor verifique su email y/o contraseña', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

admin.add_view(UserAdmin(Usuario, db.session))
@app.route("/recomendacion")
def recomendacion():
    return render_template('recomendacion.html')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Usuario, Rol)
security = Security(app, user_datastore)
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for
    )

@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', descripcion='Administrador')
    user_datastore.find_or_create_role(name='tecnico', descripcion='Tecnico Agricola')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password_admin = utils.hash_password('admin')
    encrypted_password_tecnico = utils.hash_password('tecnico')
    if not user_datastore.get_user('tecnico@example.com'):
        user_datastore.create_user(email='tecnico@example.com', password=encrypted_password_tecnico)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password_admin)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('tecnico@example.com', 'tecnico')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()
# db.create_all()
# db.session.commit()
# admin=Tipous(tipo_us='admin')
# tecnico=Tipous(tipo_us='tecnico')
# db.session.add(admin)
# db.session.add(tecnico)
# db.session.commit()
# user1 = Usuario(usuario='admin', email='admin@example.com',_password='admin',tipo_id=1)
# user2 = Usuario(usuario='tecnico', email='tecnico@demo.com',_password='tecnico',tipo_id=2)
# db.session.add(user1)
# db.session.add(user2)
# db.session.commit()