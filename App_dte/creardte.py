#!/usr/bin/python
# -*- coding: utf-8 -*-
from dte import *
from timbre import *
from signdte import *
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


with open('DTEDEVELOPER1.xml', 'w', encoding='ISO-8859-1') as doc:
    doc.write(documento)