#!/usr/bin/env python
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session,send_file
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



@app.route('/descarga/<sobre>/<archivo>')
def return_files(sobre,archivo):
    direccion = 'resultado/' + sobre + '/' + archivo      
    return send_file(direccion,as_attachment=True)


@app.route('/error')
def errores():
    
        orden = consulta.validar_csv('farmacia')        
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
            with open ('usuarios', 'r+') as archivo:
                archileer = csv.reader(archivo)
                leerusuarios = list(archileer)
                for z in range(len(leerusuarios)):
                    if leerusuarios[z][0] == formulario.usuario.data:
                        flash('nombre de usuario ya esta usado')
                        return render_template('registrar.html', form=formulario)
            with open('usuarios', 'a+') as archivo2:
                archivo_csv = csv.writer(archivo2)
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
            with open ('usuarios', 'r+') as archivo:
                archileer = csv.reader(archivo)
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
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

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
        leer_csv = consulta.leer_csv('farmacia')
        orden = consulta.orden(leer_csv)
        listainversa = []
        for z in leer_csv[-5:]:
            listainversa.append(z)
        return render_template('ventas.html',ultimas_ventas = listainversa,orden = orden)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))








@app.route('/mejorcliente')
def mejoresclientes():
    if 'username' in session:
        listadict = consulta.leer_csv_dict("farmacia")
        matriz_clientes_dinero = consulta.mejoresclientes(listadict)
        sobre = "MEJORESCLIENTES"
        nombre = consulta.exportardinero(matriz_clientes_dinero,sobre)
        return render_template('mejoresclientes.html', matriz=matriz_clientes_dinero,nombre=nombre)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/mejorproducto')
def mejorproducto():
    if 'username' in session:
        listadict = consulta.leer_csv_dict("farmacia")
        matriz_producto_codigo_cantidad = consulta.mejorproducto(listadict)
        sobre = "MEJORESPRODUCTOS"
        nombre = consulta.exportarmejor(matriz_producto_codigo_cantidad,sobre)
        return render_template('mejorproducto.html', matriz=matriz_producto_codigo_cantidad,nombre=nombre)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/productoxclientes/<producto>', methods=['GET', 'POST'])
def productoxclientes(producto):
    if 'username' in session:        
        formulario = ListarForm()
        if formulario.validate_on_submit():
            return redirect(url_for('busqueda', segmen=formulario.usuario.data))       
        leer_csv = consulta.leer_csv('farmacia')
        orden = consulta.orden(leer_csv)
        listadict = consulta.leer_csv_dict("farmacia")
        sobre = "PRODUCTO"
        nombre = consulta.exportar(listadict,orden,producto,sobre)
        return render_template('productoxclientes.html', producto=producto, listadict=listadict,orden=orden,form=formulario,nombre=nombre)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/busqueda/<segmen>')
def busqueda(segmen):
    if 'username' in session:
        parte_buscadora = segmen.upper()
        leer_csv_dict = consulta.leer_csv_dict("farmacia")
        lista_resultado = consulta.busqueda(leer_csv_dict,parte_buscadora)
        if len(lista_resultado) == 1:
            return redirect(url_for('productoxclientes', producto = lista_resultado[0]))
        if not lista_resultado:
            flash('no se encontro ' + parte_buscadora)
        return render_template('busqueda.html', resultado=lista_resultado)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/clientesxproducto/<cliente>',methods=['GET', 'POST'])
def clientesxproducto(cliente):
    if 'username' in session:
        formulario = ListarForm()
        if formulario.validate_on_submit():
            return redirect(url_for('busquedacliente', segmen=formulario.usuario.data))
        leer_csv = consulta.leer_csv('farmacia')
        orden = consulta.orden(leer_csv)
        listadict = consulta.leer_csv_dict("farmacia",)
        sobre = "CLIENTE"
        nombre = consulta.exportar(listadict,orden,cliente,sobre)
        return render_template('clientesxproducto.html', cliente=cliente, listadict=listadict,orden=orden ,form=formulario, nombre=nombre)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/busqueda', methods=['GET', 'POST'])
def saludar():
    if 'username' in session:
        formulario = ListarForm()
        if formulario.validate_on_submit():
            print(formulario.usuario.name)
            return redirect(url_for('busqueda', segmen=formulario.usuario.data))
        return render_template('usuarios.html', form=formulario)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/busquedacliente/<segmen>')
def busquedacliente(segmen):
    if 'username' in session:
        parte_buscadora = segmen.upper()
        leer_csv_dict = consulta.leer_csv_dict("farmacia")
        lista_resultado = consulta.busquedacliente(leer_csv_dict,parte_buscadora)
        if len(lista_resultado) == 1:
            return redirect(url_for('clientesxproducto', cliente = lista_resultado[0]))
        if not lista_resultado:
            flash('no se encontro ' + parte_buscadora)
        return render_template('busquedacliente.html', resultado=lista_resultado)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

@app.route('/busquedacliente', methods=['GET', 'POST'])
def saludart():
    if 'username' in session:
        formulario = ListarForm()
        if formulario.validate_on_submit():
            print(formulario.usuario.name)
            return redirect(url_for('busquedacliente', segmen=formulario.usuario.data))
        return render_template('usuarios.html', form=formulario)
    else:
        flash('no tenes permisos')
        return redirect(url_for('ingresar'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    manager.run()
