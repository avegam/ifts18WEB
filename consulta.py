import csv
from datetime import datetime
from error import errorja

def leer_csv(archicsv):
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.reader(archivo)        
        leer_csv = list(archivo_csv)       
        return leer_csv        

def leer_csv_dict(archivocsv):
    with open(archivocsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        leido_lista_csvdict = list(archivo_csv) 
        return leido_lista_csvdict

def validar_csv(archivocsv):
    try:
        with open(archivocsv,'r', encoding='latin-1') as archivo:    
            archivo_csv = csv.DictReader(archivo)
            leer_csv_dict = list(archivo_csv)
    except FileNotFoundError as TT:
        raise errorja("archivo csv no encontrado") from TT 
        for linea in leer_csv_dict:
            if len(linea) != 5:
                raise errorja('cantidad de campos incorrecta')
            if not isinstance(int(float(linea["CANTIDAD"])),int):
                raise errorja('no es int')
            if not isinstance(float(linea["PRECIO"]),float):
                raise errorja('no es decimal')
            for campo in linea:
                if campo is None or '':
                    raise errorja
    return leer_csv_dict
                


def orden(archivoleido):    
        orden2 = 0
        
        for rs in archivoleido:
            orden2 = rs
            break
        return orden2



def mejoresclientes(listadict):   
        lista_clientes = []
        matriz_clientes_dinero = [] 
        
        for t in listadict:
            if t["CLIENTE"] not in lista_clientes: 
                lista_clientes.append(t["CLIENTE"])
                
        for p in range(len(lista_clientes)):
            matriz_clientes_dinero.append([lista_clientes[p],0])

        for c in listadict:
            for z in range(len(lista_clientes)):
                if c["CLIENTE"] == lista_clientes[z]:
                    precio = matriz_clientes_dinero[z][1]
                    unidades = float(c["CANTIDAD"]) 
                    valor = float(c["PRECIO"])
                    precio += valor * unidades
                    matriz_clientes_dinero[z][1] = precio

        matriz_clientes_dinero.sort(key=lambda x:x[1], reverse=True)
        return matriz_clientes_dinero

def exportardinero(resultado,sobre):
    nombre = datetime.now().strftime('resultado_%Y%m%d_%H%M%S')
    with open ('resultado/' + sobre + "/" + nombre + ".csv", 'a+') as nuevo_csv:
        nuevo_csv.write("Listado de clientes que gastaron mas dinero ordenados de mayor a menor" + '\n')
        exportar = csv.writer(nuevo_csv,delimiter=',')
        exportar.writerow(['Cliente','Dinero'])
        for j in range(len(resultado)):
            exportar.writerow([resultado[j][0],round(resultado[j][1],2)])
        return nombre

def mejorproducto(listadict):
        listado_productos = []
        listado_codigos = []       
        matriz_producto_codigo_cantidad = []
        
        for t in listadict:
            if t["PRODUCTO"] not in listado_productos: 
                listado_productos.append(t["PRODUCTO"])
                listado_codigos.append(t["CODIGO"])

        for p in range(len(listado_productos)):            
            matriz_producto_codigo_cantidad.append([listado_productos[p],listado_codigos[p],0])       
        
        for c in listadict:
            for z in range(len(listado_productos)):
                if c["PRODUCTO"] == matriz_producto_codigo_cantidad[z][0]:
                    cantidad = matriz_producto_codigo_cantidad[z][2]
                    unidades = float(c["CANTIDAD"])                     
                    cantidad += unidades
                    matriz_producto_codigo_cantidad[z][2] = cantidad

        matriz_producto_codigo_cantidad.sort(key=lambda x:x[2], reverse=True)
        return matriz_producto_codigo_cantidad

def exportarmejor(resultado,sobre):
    nombre = datetime.now().strftime('resultado_%Y%m%d_%H%M%S')
    with open ('resultado/' + sobre + "/" + nombre + ".csv", 'a+') as nuevo_csv:
        nuevo_csv.write("Listado de productos que mas cantidades compraron ordenados de mayor a menor" + '\n')
        exportar = csv.writer(nuevo_csv,delimiter=',')
        exportar.writerow(['Producto','Codigo',"Cantidad"])
        for j in range(len(resultado)):
            exportar.writerow([resultado[j][0],resultado[j][1],resultado[j][2]])
        return nombre

def busqueda(listadict,segmento):
        listado_productos = []
        resultado_busqueda = []
       
        for t in listadict:
            if t["PRODUCTO"] not in listado_productos: 
                listado_productos.append(t["PRODUCTO"])
        if segmento not in listado_productos:

            for p in range(len(listado_productos)):
                if str(listado_productos[p]).find(segmento) != -1:
                    resultado_busqueda.append(listado_productos[p])
        else:
            for p in range(len(listado_productos)):
                if str(listado_productos[p]) == segmento:
                    resultado_busqueda.append(listado_productos[p])

        return resultado_busqueda

def busquedacliente(listadict,segmento):     
        listado_cliente = []
        resultado_busqueda = []        
        
        for t in listadict:
            if t["CLIENTE"] not in listado_cliente: 
                listado_cliente.append(t["CLIENTE"])
        if segmento not in listado_cliente:
            for p in range(len(listado_cliente)):
                if str(listado_cliente[p]).find(segmento) != -1:
                    resultado_busqueda.append(listado_cliente[p])
        else:
            for p in range(len(listado_cliente)):
                if str(listado_cliente[p]) == segmento:
                    resultado_busqueda.append(listado_cliente[p])
        return resultado_busqueda

def exportar(resultados,orden,busqueda,sobre):
    nombre = datetime.now().strftime('resultado_%Y%m%d_%H%M%S')
    with open ('resultado/' + sobre + "/" + nombre + ".csv", 'a+') as nuevo_csv:
        nuevo_csv.write("resultado de la busqueda de todos movientos del " + sobre + " " + busqueda + '\n')
        fieldnames = orden
        csv_resultado = csv.DictWriter(nuevo_csv,fieldnames=fieldnames,delimiter=',') 
        csv_resultado.writeheader()        
        for h in resultados:
            if busqueda == h[sobre]:
                csv_resultado.writerow(h)
        return nombre

#def exportar(resultados,orden,busqueda,sobre):
#    nombre = datetime.now().strftime('resultado_%Y%m%d_%H%M%S')
#    with open ('resultado/' + sobre + "/" + nombre + ".csv", 'w')
#        columnTitleRow = 'CLIENTE, CODIGO, PRODUCTO, CANTIDAD, PRECIO\n'
#        csv.write(columnTitleRow)              
#        for key in resultados.key:
#            CLIENTE =
#            CODIGO =
#            PRODUCTO =
#            CANTIDAD =
#            PRECIO =

#def exportar(resultados,orden,busqueda,sobre):
#    nombre = datetime.now().strftime('resultado_%Y%m%d_%H%M%S')
#    with open ('resultado/' + sobre + "/" + nombre + ".csv", 'w') as nuevo_csv:
#        fieldnames = orden
#        csv_resultado = csv.DictWriter(nuevo_csv,fieldnames=fieldnames) 
#        csv_resultado.writeheader()        
#        for h in resultados:
#            if busqueda == h[sobre]:
#                csv_resultado.writerow(h)
#        return nombre
            
       
    
