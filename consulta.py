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
            
            dicta.append(listado[p],0])
        for c in farmase:
            for z in range(len(listado)):
                if c["CLIENTE"] == listado[z]:
                    precio = dicta[z][1]
                   # unidades = 1
                    #valor = 3
                    precio += valor * unidades
                    dicta[z][1] = precio
               
        return dicta

