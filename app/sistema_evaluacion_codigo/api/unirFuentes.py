
#Modulo para unir varios archivos simples de java en uno solo para facilitar compilacion y revision de plagio.

import re
import zipfile

def quitarSubCadenada(cadenaFuente, inicio, fin):
    if inicio != 0 and fin < (len(cadenaFuente) - 1):
        return cadenaFuente[:inicio] + cadenaFuente[fin+1:]
    elif inicio == 0 and fin < (len(cadenaFuente) - 1):
        return cadenaFuente[fin+1:]
    elif inicio != 0 and fin == (len(cadenaFuente) - 1):
        return cadenaFuente[:inicio]
    else:
        return ''  # toda la cadena hizo match
    

def quitarOcurrenciaUnica(cadenaFuente, pattern):
    compilado = re.compile(pattern, re.MULTILINE)
    match = compilado.search(cadenaFuente)
    if not match:
        return cadenaFuente  # no tiene ocurrencia
    inicio = match.start(1)
    fin = match.end(1)
    return quitarSubCadenada(cadenaFuente, inicio, fin)


def extraerSubcadenas(cadenaFuente, pattern):
    compilado = re.compile(pattern, re.MULTILINE)
    ocurr = compilado.search(cadenaFuente)
    res = []
    while ocurr:
        cadenaFuente = quitarSubCadenada(cadenaFuente,
                                         ocurr.start(), ocurr.end())
        res.append(ocurr.group().strip())
        ocurr = compilado.search(cadenaFuente)

    return res, cadenaFuente


# quita info de package y regresa cadena resultante
def quitarPackage(cadenaFuente):
    pattern = r'(^\s*package\s+[a-zA-Z]\w*;)'
    return quitarOcurrenciaUnica(cadenaFuente, pattern)


# para quitar el public de class
def quitarPublic(cadenaFuente):
    pattern = r'^\s*(public) class.*'
    return quitarOcurrenciaUnica(cadenaFuente, pattern)


# extrae imports y trunca cadena
def extraerImports(cadenaFuente):
    pattern = r'^\s*import\s+[a-zA-Z].*;'
    return extraerSubcadenas(cadenaFuente, pattern)


# El Main debe ser el primer fuente que se pasa
def unirFuentesJava(arSalida, *fuentes):
    
    contenido = fuentes[0]
    imports, programas = extraerImports(quitarPackage(contenido))

    for fuente in fuentes[1:]:
        contenido = fuente
        imps, pr = extraerImports(quitarPublic(quitarPackage(contenido)))
        programas += '\n' + pr
        imports += imps

    with open(arSalida, 'w') as salida:
        for imp in imports:
            salida.write(imp + '\n')
        salida.write(programas)
        

# regresa una lista de fuentes extraidos, primero para primer fuente
# se comprueba que se contenga archivo primero
def descomprimir(comprimido, primero='main'):
    res = []
    tieneMain = False
    try:
        with zipfile.ZipFile(comprimido) as myzip:
            for archivo in myzip.namelist():
                with myzip.open(archivo) as ar:
                    if primero.lower() in archivo.lower():
                        res.insert(0, ar.read().decode('utf-8'))
                        tieneMain = True
                    else:
                        res.append(ar.read().decode('utf-8'))

        if not tieneMain:
            return False, []
        return True, res

    except Exception:  # el zip tenia cosas que no eran texto
        return False, []


# genera fuente final pegado    
def generarFuenteJava(comprimido, destino):
    if not comprimido.lower().endswith('zip'):
        return False
    bandera, fuentes = descomprimir(comprimido, 'Main.java')
    if not bandera:
        return False
    unirFuentesJava(destino, *fuentes)
    return True
    

