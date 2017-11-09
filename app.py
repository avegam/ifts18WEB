#!/usr/bin/env python
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, ListarForm, RegistrarForm
import consulta 

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())



@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    farmas = consulta.Todo("farmacia",)
          
    return render_template('ventas.html',farma = farmas)

@app.route('/listadocliexpro', methods=['GET', 'POST'])
def listar():
    formulario = ListarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('clientesxproducto', usuario=formulario.usuario.data))
    return render_template('listadocliexpro.html', form=formulario)

@app.route('/clientesxproducto/<cliente>')
def clientesxproducto(cliente):
    farmas = consulta.Todo("farmacia",)
    return render_template('clientesxproducto.html', cliente=cliente, farma=farmas)

@app.route('/listadocliexpro', methods=['GET', 'POST'])
def listarotro():
    formulario = ListarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('clientesxproducto', usuario=formulario.usuario.data))
    return render_template('listadocliexpro.html', form=formulario)

@app.route('/productoxclientes/<producto>')
def productoxclientes(producto):
    farmas = consulta.Todo("farmacia",)
    return render_template('productoxclientes.html', producto=producto, farma=farmas)

@app.route('/mayorpostor')
def mayorpostor():
    farmas = consulta.mayorganancia("farmacia",)
    return render_template('mayorpostor.html', farma=farmas)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    manager.run()
