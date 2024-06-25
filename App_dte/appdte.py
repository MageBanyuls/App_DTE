#!/usr/bin/python
# -*- coding: utf-8 -*-
from dte import *
from timbre import *
from signdte import *
from enviodte import *
from authSII import *
from upload import *
import json

# Leer contenido del archivo DTEPRUEBA.json
with open("DTEPRUEBA.json", "r", encoding="utf-8") as f:
    contenido = f.read()

print(contenido)

info = json.loads(contenido)
infoemisor = info['emisor']
rutemisor = infoemisor['rutemisor']
rutenvia = infoemisor['rutenvia']

infoiddoc = info['iddoc']

# Crear objeto DTE y el archivo XML
objDTE = DTE()
documento = objDTE.creaDTE(contenido)

# Añadir la sección de timbre
objtimbre = TIMBRE()
documento = objtimbre.creaTimbre(documento)

# Añadir la sección de firma del DTE y firmar el documento
objfirma = SIGNDTE()
documento = objfirma.signDTE(documento)

# Crear el sobre electrónico del documento electrónico
# objEnvioDTE = ENVIODTE()
# enviodte = objEnvioDTE.make_envio(documento, infoemisor, infoiddoc)

# # Preparar la secuencia de autenticación
# objauthSII = AuthSII()
# objSeed = objauthSII.getSeed()
# valortoken = objauthSII.getToken(objSeed)

# # Con el token obtenido, iniciar la secuencia de carga del documento e iniciar el upload al SII
# objupLoad = UPLOADSII()
# respuesta = objupLoad.uploadDTE(valortoken, rutemisor, rutenvia, "enviodtefirmado")

# # Imprimir cadena XML que devuelve un track ID
# print(respuesta)
