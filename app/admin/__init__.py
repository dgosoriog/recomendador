from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from flask_login import current_user
from flask_security import utils
from flask import redirect,url_for

# def format_user(self,request,user,*args):
#     return user.email.upper()

class UserAdmin(ModelView):
    '''clase administrador'''
    #column_formatters = {'email': format_user}
    column_list = {'roles','email'}
    column_searchable_list = {'email'}
    column_filters = ['roles']
    form_excluded_columns = ['password','active']
    form_extra_fields = {
        'password2': PasswordField('Contraseña')
    }
    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):
        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.hash_password(model.password2)

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))




