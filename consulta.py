import csv
def Todo(archicsv):
    
    with open(archicsv,'r', encoding='latin-1') as archivo:
        archivo_csv = csv.DictReader(archivo)
        #farmase = []
        farmase = list(archivo_csv) 
        #for line in archivo_csv:
            # farmase.append("{CLIENTE} {CODIGO} {PRODUCTO} {CANTIDAD} {PRECIO}".format(**line))
  
        return farmase
'''
def clientesxproducto(cliente):
    with open(archivo3,'r', encoding='latin-1') as archivo:
       archivo_csv = csv.DictReader(archivo)
       carmen = list(archivo_csv)
       
       return car'''

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
