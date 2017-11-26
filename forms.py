from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class ListarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('buscar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')

class CambioPassForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    passwordvieja = PasswordField('Vieja Contraseña', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Cambiar contrasena')
