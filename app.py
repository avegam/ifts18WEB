#!/usr/bin/env python
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, ListarForm, RegistrarForm,CambioPassForm
import consulta 
from error import errorja

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

@app.route('/')
def index():
    
    return render_template('index.html', fecha_actual=datetime.utcnow(),)


@app.route('/error')
def errores():
    
        orden = consulta.orden3('farmacia')
        '''if orden:
            raise errorja('si archivo')
            
        else:
            raise errorja('no archivo')
    except errorja as e:'''
        return render_template('error.html',error = orden)

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        formulario = LoginForm()
        if formulario.validate_on_submit():
            with open('usuarios') as archivo:
                archivo_csv = csv.reader(archivo)
                registro = next(archivo_csv)
                while registro:
                    if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                        flash('Bienvenido')
                        session['username'] = formulario.usuario.data
                        return redirect(url_for('ventas'))
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
            with open ('usuarios', 'r+') as archi:
                archileer = csv.reader(archi)
                leerusuarios = list(archileer)
                for z in range(len(leerusuarios)):
                    if leerusuarios[z][0] == formulario.usuario.data:
                        flash('nombre de usuario ya estea usado')
                        return render_template('registrar.html', form=formulario)
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)

@app.route('/cambiocontras', methods=['GET', 'POST'])
def cambiocon():
    formulario = CambioPassForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open ('usuarios', 'r+') as archi:
                archileer = csv.reader(archi)
                leerusuarios = list(archileer)
                for z in range(len(leerusuarios)):
                    if leerusuarios[z][0] == formulario.usuario.data and leerusuarios[z][1] == formulario.passwordvieja.data:
                        leerusuarios[z][1] = formulario.password.data
                        with open ('usuarios', 'w') as csvcorregido:
                            nuevousuarios = csv.writer(csvcorregido)
                            nuevousuarios.writerows(leerusuarios)
                        flash('su contrasena se cambio correctamente')
                        return redirect(url_for('ingresar'))
                flash('Revisá nombre de usuario y contraseña')
        flash('las contraseñas no coinciden')
    return render_template('cambiopass.html', form=formulario)

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
    if 'username' in session:
        orden = consulta.orden('farmacia')
        farmas = consulta.Todoventa("farmacia",)
        listainversa = []
        for z in farmas[-5:]:
            listainversa.append(z)
        return render_template('ventas.html',farma = listainversa,orden = orden)
    else:
        return render_template('sin_permiso.html')



@app.route('/clientesxproducto/<cliente>')
def clientesxproducto(cliente):
    if 'username' in session:
        orden = consulta.orden('farmacia')
        farmas = consulta.Todo("farmacia",)
        sobre = "CLIENTE"
        consulta.exportar(farmas,orden,cliente,sobre)
        return render_template('clientesxproducto.html', cliente=cliente, farma=farmas,orden=orden)
    else:
        return render_template('sin_permiso.html')


@app.route('/productoxclientes/<producto>')
def productoxclientes(producto):
    if 'username' in session:
        orden = consulta.orden('farmacia')
        farmas = consulta.Todo("farmacia",)
        sobre = "PRODUCTO"
        consulta.exportar(farmas,orden,producto,sobre)
        return render_template('productoxclientes.html', producto=producto, farma=farmas,orden=orden)
    else:
        return render_template('sin_permiso.html')

@app.route('/mayorpostor')
def mayorpostor():
    if 'username' in session:
        farmas = consulta.mayorganancia("farmacia",)
        sobre = "MEJORESCLIENTES"
        consulta.exportardinero(farmas,sobre)
        return render_template('mayorpostor.html', farma=farmas)
    else:
        return render_template('sin_permiso.html')

@app.route('/mejorproducto')
def mejorproducto():
    if 'username' in session:
        farmas = consulta.mejorproducto("farmacia",)
        sobre = "MEJORESPRODUCTOS"
        consulta.exportarmejor(farmas,sobre)
        return render_template('mejorproducto.html', farma=farmas)
    else:
        return render_template('sin_permiso.html')

@app.route('/busqueda/<segmen>')
def busqueda(segmen):
    if 'username' in session:
        farmas = consulta.busqueda("farmacia",segmen,)
        return render_template('busqueda.html', farma=farmas)
    else:
        return render_template('sin_permiso.html')

@app.route('/busqueda', methods=['GET', 'POST'])
def saludar():
    if 'username' in session:
        formulario = ListarForm()
        if formulario.validate_on_submit():
            print(formulario.usuario.name)
            return redirect(url_for('busqueda', segmen=formulario.usuario.data))
        return render_template('usuarios.html', form=formulario)
    else:
        return render_template('sin_permiso.html')

@app.route('/busquedacliente/<segmen>')
def busquedacliente(segmen):
    if 'username' in session:
        farmas = consulta.busquedacliente("farmacia",segmen,)
        return render_template('busquedacliente.html', farma=farmas)
    else:
        return render_template('sin_permiso.html')

@app.route('/busquedacliente', methods=['GET', 'POST'])
def saludart():
    if 'username' in session:
        formulario = ListarForm()
        if formulario.validate_on_submit():
            print(formulario.usuario.name)
            return redirect(url_for('busquedacliente', segmen=formulario.usuario.data))
        return render_template('usuarios.html', form=formulario)
    else:
        return render_template('sin_permiso.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    manager.run()
