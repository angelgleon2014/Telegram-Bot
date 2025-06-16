import os 
  
path = "/home/angel/Documentos/botscalping/symbols/botdmirsi/"
  
os.chdir(path) 
  
suma        = 0
suma1       = 0
suma2       = 0
sumaperdido = 0  
cant        = 0
sumap       = 0
sumag       = 0 
listoftradeopen, lstwin, lstlost = [], [], []
canttradeopen = 0 
def read_text_file(file_path): 
    global suma, cant, suma2, suma1, sumaperdido
    with open(file_path, 'r') as f: 
        # print(file_path)
        # print(f.read())
        valor = (f.read())
        # print(f"valor {valor}")
        primercaracter = valor[0]
        # print(f"primercaracter  {primercaracter}")

        # if int(primercaracter) == 1:
        if float(valor) >=10:
            # print(f"valor {valor}")
            nuevovalor = valor[1:] 
            # print(f"ganado {nuevovalor}")
            suma1 = suma1 + float(nuevovalor)
        else:
        # if int(primercaracter) == 9:
            # nuevovalor = valor[1:]
            # print(f"nuevovalor2 {nuevovalor}")
            # cero = "0" 
            # nuevovalor = cero + valor[1:] 
            # print(f"nuevovalor3 {nuevovalor}")
            perdido = 10 - float(valor)
            # print(f"perdido {perdido}")
            sumaperdido = sumaperdido + perdido
            # suma2 = suma2 + float(nuevovalor)
            pass
        name = os.path.split(file_path)
        # print(name[1])
        # print("el valor es: ", name[1],"--",valor )
        suma = suma1 - suma2
        cant +=1
        # print("la suma es: ", suma)

def read_text_files(file_path): 
    # global suma, cant
    global listoftradeopen, canttradeopen
    with open(file_path, 'r') as f: 
        # print(f.read())
        valor = (f.read())
        name = os.path.split(file_path)
        if valor == 'tradeopen':
            listoftradeopen.append(name[1])
        canttradeopen = len(listoftradeopen)

def read_text_filep(file_path): 
    global sumap
    with open(file_path, 'r') as f: 
        # print(f.read())
        valor = (f.read()) 
        name = os.path.split(file_path)
        valorlista = str(valor) + " - " + str(name[1][:-4])
        # print(name[1])
        lstlost.append(valorlista)
        # print("el valor es: ", name[1],"--",valor )
        sumap = sumap + int(valor)
        # cant +=1
        # print("Perdidas: ", sumap)

def read_text_fileg(file_path): 
    global sumag
    with open(file_path, 'r') as f: 
        # print(f.read())
        valor = (f.read()) 
        name = os.path.split(file_path)
        valorlista = str(valor) + " - " + str(name[1][:-4])
        # print(name[1])
        lstwin.append(valorlista)
        # print("el valor es: ", name[1],"--",valor )
        sumag = sumag + int(valor)
        # cant +=1
        # print("Ganadas: ", sumag)
  
  
for file in os.listdir(): 
    
    if file.endswith("T.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_file(file_path)
    if file.endswith("S.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_files(file_path)
    if file.endswith("p.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_filep(file_path)
    if file.endswith("g.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_fileg(file_path)

""" for file in os.listdir(): 
    
    if file.endswith("p.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_filep(file_path)

for file in os.listdir(): 
    
    if file.endswith("g.txt"): 
        file_path = f"{path}/{file}"
        valor = read_text_fileg(file_path) """
    
    # print("\n") 
print("                                                           ")
print("------------------GANADORAS--------------------------------")
lstwin.sort(key=lambda lstwin: lstwin.split("-")[0], reverse=True)
print(lstwin)
print("                                                           ")
print("------------------PERDEDORAS-------------------------------")
lstlost.sort(key=lambda lstlost: lstlost.split("-")[0], reverse=True)
print(lstlost)
print("                                                           ")
print("------------------RESULTADOS-------------------------------")
print("Profit      : ", suma)
print("Loss        : ", sumaperdido)
print("Balence     : ", suma - sumaperdido)
print("la catidad es :", cant)
print("Trades Abiertos : ", listoftradeopen)
print("Cantidad de Trades Abiertos : ", canttradeopen)
print("Ganadas : ", sumag)
print("Perdidas : ", sumap)
