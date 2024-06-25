#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xml.dom.minidom import *
import json

# Inicializo un objeto de documento XML
class DTE:
    dte = ''
    doc = ''
    documento = ''

    def __init__(self):
        self.doc = Document()
        # Creo el nodo DTE
        self.dte = self.doc.createElement("DTE")
        self.dte.setAttribute("version", "1.0")

        self.documento = self.doc.createElement("Documento")
        self.documento.setAttribute("ID", "DOC33")

    def creaDTE(self, contenido):
        # Obtengo la información del JSON
        info = json.loads(contenido)
        infoiddoc = info['iddoc']

        # Identificación del documento
        encabezado = self.doc.createElement("Encabezado")
        iddoc = self.doc.createElement("IdDoc")
        tipodte = self.doc.createElement('TipoDTE')
        text = self.doc.createTextNode(infoiddoc['tipodte'])
        tipodte.appendChild(text)
        folio = self.doc.createElement('Folio')
        text = self.doc.createTextNode(infoiddoc['numdte'])
        folio.appendChild(text)
        fchemis = self.doc.createElement('FchEmis')
        text = self.doc.createTextNode(infoiddoc['fchemis'])
        fchemis.appendChild(text)
        iddoc.appendChild(tipodte)
        iddoc.appendChild(folio)
        iddoc.appendChild(fchemis)

        # Creo el nodo con los datos del emisor
        # Obtengo la información del emisor del JSON
        infoemisor = info['emisor']

        emisor = self.doc.createElement("Emisor")
        rutemisor = self.doc.createElement('RUTEmisor')
        text = self.doc.createTextNode(infoemisor['rutemisor'])
        rutemisor.appendChild(text)
        emisor.appendChild(rutemisor)

        rznsoc = self.doc.createElement('RznSoc')
        text = self.doc.createTextNode(infoemisor['rsemisor'])
        rznsoc.appendChild(text)
        emisor.appendChild(rznsoc)

        giroemis = self.doc.createElement('GiroEmis')
        text = self.doc.createTextNode(infoemisor['giroemisor'])
        giroemis.appendChild(text)
        emisor.appendChild(giroemis)

        acteco = self.doc.createElement('Acteco')
        text = self.doc.createTextNode(infoemisor['acteco'])
        acteco.appendChild(text)
        emisor.appendChild(acteco)

        cdgsiisucur = self.doc.createElement('CdgSIISucur')
        text = self.doc.createTextNode(infoemisor['cdgsiisucur'])
        cdgsiisucur.appendChild(text)
        emisor.appendChild(cdgsiisucur)

        dirorigen = self.doc.createElement('DirOrigen')
        text = self.doc.createTextNode(infoemisor['diremisor'])
        dirorigen.appendChild(text)
        emisor.appendChild(dirorigen)

        cmnaorigen = self.doc.createElement('CmnaOrigen')
        text = self.doc.createTextNode(infoemisor['cmnaemisor'])
        cmnaorigen.appendChild(text)
        emisor.appendChild(cmnaorigen)

        ciudadorigen = self.doc.createElement('CiudadOrigen')
        text = self.doc.createTextNode(infoemisor['ciuemisor'])
        ciudadorigen.appendChild(text)
        emisor.appendChild(ciudadorigen)

        # Obtengo la información del receptor del JSON
        inforeceptor = info['receptor']
        # Nodo con los datos del receptor
        receptor = self.doc.createElement("Receptor")

        rutrecep = self.doc.createElement('RUTRecep')
        text = self.doc.createTextNode(inforeceptor['rutreceptor'])
        rutrecep.appendChild(text)
        receptor.appendChild(rutrecep)

        rznsocrecep = self.doc.createElement('RznSocRecep')
        text = self.doc.createTextNode(inforeceptor['rsreceptor'])
        rznsocrecep.appendChild(text)
        receptor.appendChild(rznsocrecep)

        girorecep = self.doc.createElement('GiroRecep')
        text = self.doc.createTextNode(inforeceptor['giroreceptor'])
        girorecep.appendChild(text)
        receptor.appendChild(girorecep)

        dirrecep = self.doc.createElement('DirRecep')
        text = self.doc.createTextNode(inforeceptor['dirreceptor'])
        dirrecep.appendChild(text)
        receptor.appendChild(dirrecep)

        cmnarecep = self.doc.createElement('CmnaRecep')
        text = self.doc.createTextNode(inforeceptor['cmnareceptor'])
        cmnarecep.appendChild(text)
        receptor.appendChild(cmnarecep)

        ciudadrecep = self.doc.createElement('CiudadRecep')
        text = self.doc.createTextNode(inforeceptor['ciureceptor'])
        ciudadrecep.appendChild(text)
        receptor.appendChild(ciudadrecep)

        encabezado.appendChild(iddoc)
        encabezado.appendChild(emisor)
        encabezado.appendChild(receptor)
        self.documento.appendChild(encabezado)

        # Creo el nodo con los totales del documento
        # Obtengo la info del JSON de los totales del documento
        infototales = info['totales']

        totales = self.doc.createElement('Totales')
        mntneto = self.doc.createElement('MntNeto')
        text = self.doc.createTextNode(infototales['montoafecto'])
        mntneto.appendChild(text)
        totales.appendChild(mntneto)

        tasaiva = self.doc.createElement('TasaIVA')
        text = self.doc.createTextNode(infototales['tasaiva'])
        tasaiva.appendChild(text)
        totales.appendChild(tasaiva)

        iva = self.doc.createElement('IVA')
        text = self.doc.createTextNode(infototales['iva'])
        iva.appendChild(text)
        totales.appendChild(iva)

        mnttotal = self.doc.createElement('MntTotal')
        text = self.doc.createTextNode(infototales['montototal'])
        mnttotal.appendChild(text)
        totales.appendChild(mnttotal)
        encabezado.appendChild(totales)

        # Añado los detalles
        # Obtengo la info del JSON de los detalles del documento
        for infodetalle in info['detalle']:

            detalle = self.doc.createElement("Detalle")
            nrolindet = self.doc.createElement("NroLinDet")
            text = self.doc.createTextNode(infodetalle['nrolinea'])
            nrolindet.appendChild(text)
            detalle.appendChild(nrolindet)

            cdgitem = self.doc.createElement("CdgItem")
            tpocodigo = self.doc.createElement("TpoCodigo")
            text = self.doc.createTextNode(infodetalle['tpocodigo'])
            tpocodigo.appendChild(text)

            vlrcodigo = self.doc.createElement("VlrCodigo")
            text = self.doc.createTextNode(infodetalle['vlrcodigo'])
            vlrcodigo.appendChild(text)

            cdgitem.appendChild(tpocodigo)
            cdgitem.appendChild(vlrcodigo)
            detalle.appendChild(cdgitem)

            nmbitem = self.doc.createElement("NmbItem")
            text = self.doc.createTextNode(infodetalle['nmbitem'])
            nmbitem.appendChild(text)

            dscitem = self.doc.createElement("DscItem")
            text = self.doc.createTextNode(infodetalle['nmbitem'])
            dscitem.appendChild(text)

            qtyitem = self.doc.createElement("QtyItem")
            text = self.doc.createTextNode(infodetalle['qtyitem'])
            qtyitem.appendChild(text)

            prcitem = self.doc.createElement("PrcItem")
            text = self.doc.createTextNode(infodetalle['prcitem'])
            prcitem.appendChild(text)

            montoitem = self.doc.createElement("MontoItem")
            text = self.doc.createTextNode(infodetalle['montoitem'])
            montoitem.appendChild(text)

            detalle.appendChild(nmbitem)
            detalle.appendChild(dscitem)
            detalle.appendChild(qtyitem)
            detalle.appendChild(prcitem)
            detalle.appendChild(montoitem)
            self.documento.appendChild(detalle)

        self.dte.appendChild(self.documento)
        self.doc.appendChild(self.dte)

        # Aplico indentado antes de guardar
        contenido = self.doc.toprettyxml(indent="  ")
        return contenido
        # Guardo el XML del documento
        # f = open("dte.xml", "w")
        # f.write(contenido.encode('iso-8859-1'))
        # f.close()
