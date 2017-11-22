import csv
import os.path
from error import errorja

def orden2(archi):
    feo = False
    if os.path.isfile(archi):
        feo = True
    return feo
def orden3(arch):
    with open(arch,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        #farmase = []
        farmase = list(archivo_csv) 
        for zaraza in farmase:
            if len(zaraza) != 5:
                raise errorja
            if type(zaraza["CANTIDAD"]) != int:
                    raise errorja
            if type(float(zaraza["PRECIO"])) != float:
                    raise errorja
            for campete in zaraza:
                if campete is None or '':
                    raise errorja
        return farmase
                


def orden(archi):
    with open(archi,'r', encoding='latin-1') as archivo:
        archi_csv = csv.reader(archivo)
        orden = list(archi_csv)
        orden2 = 0
        
        for rs in orden:
            orden2 = rs
            break
        return orden2
       

def Todo(archicsv):
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        #farmase = []
        farmase = list(archivo_csv) 
        #for line in archivo_csv:
            # farmase.append("{CLIENTE} {CODIGO} {PRODUCTO} {CANTIDAD} {PRECIO}".format(**line))
        return farmase

def mayorganancia(archicsv):
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        farmase = list(archivo_csv)
        listado = []
        dicta = [] 
        
        for t in farmase:
            if t["CLIENTE"] not in listado: 
                listado.append(t["CLIENTE"])
                
        for p in range(len(listado)):
            dicta.append([listado[p],0])

        for c in farmase:
            for z in range(len(listado)):
                if c["CLIENTE"] == listado[z]:
                    precio = dicta[z][1]
                    unidades = float(c["CANTIDAD"]) 
                    valor = float(c["PRECIO"])
                    precio += valor * unidades
                    dicta[z][1] = precio

        dicta.sort(key=lambda x:x[1], reverse=True)
        return dicta

def mejorproducto(archicsv):
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        farmase = list(archivo_csv)
        listado = []
        dictado = []       
        lista3 = []
        
        for t in farmase:
            if t["PRODUCTO"] not in listado: 
                listado.append(t["PRODUCTO"])
                dictado.append(t["CODIGO"])

        for p in range(len(listado)):            
            lista3.append([listado[p],dictado[p],0])       
        
        for c in farmase:
            for z in range(len(listado)):
                if c["PRODUCTO"] == lista3[z][0]:
                    cantidad = lista3[z][2]
                    unidades = float(c["CANTIDAD"])                     
                    cantidad += unidades
                    lista3[z][2] = cantidad

        lista3.sort(key=lambda x:x[2], reverse=True)
        return lista3

def busqueda(archicsv,segmen):
     with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        farmase = list(archivo_csv)
        listado = []
        resultado = []
       
        for t in farmase:
            if t["PRODUCTO"] not in listado: 
                listado.append(t["PRODUCTO"])

        for p in range(len(listado)):
            if str(listado[p]).find(segmen) != -1:
                resultado.append(listado[p])

        return resultado

def busquedacliente(archicsv,segmen):
     with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        farmase = list(archivo_csv)
        listado = []
        resultado = []        
        
        for t in farmase:
            if t["CLIENTE"] not in listado: 
                listado.append(t["CLIENTE"])

        for p in range(len(listado)):
            if str(listado[p]).find(segmen) != -1:
                resultado.append(listado[p])

        return resultado
            
def Todoventa(archicsv):
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.reader(archivo)        
        farmase = list(archivo_csv) 
        
        return farmase        
    
