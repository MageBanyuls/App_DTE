#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parseString, Node
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
import base64

class TIMBRE:

    def creaTimbre(self, contenido):
        xmlTree = parseString(contenido)

        # Get all departments
        nrolinea = 0
        item1 = ""
        for node1 in xmlTree.getElementsByTagName("DscItem"):
            for node2 in node1.childNodes:
                if node2.nodeType == Node.TEXT_NODE:
                    if nrolinea == 0:
                        item1 = node2.data
                        nrolinea += 1

        documento = xmlTree.getElementsByTagName("Documento")[0]
        ted = xmlTree.createElement("TED")

        ted.setAttribute("version", "1.0")
        dd = xmlTree.createElement("DD")
        re = xmlTree.createElement("RE")

        rutemisor = ""
        for element in xmlTree.getElementsByTagName("RUTEmisor"):
            rutemisor = element.firstChild.nodeValue

        text = xmlTree.createTextNode(rutemisor)
        re.appendChild(text)
        dd.appendChild(re)

        tipodte = ""
        for element in xmlTree.getElementsByTagName("TipoDTE"):
            tipodte = element.firstChild.nodeValue

        td = xmlTree.createElement("TD")
        text = xmlTree.createTextNode(tipodte)
        td.appendChild(text)
        dd.appendChild(td)

        folio = ""
        for element in xmlTree.getElementsByTagName("Folio"):
            folio = element.firstChild.nodeValue

        f = xmlTree.createElement("F")
        text = xmlTree.createTextNode(folio)
        f.appendChild(text)
        dd.appendChild(f)

        fchemis = ""
        for element in xmlTree.getElementsByTagName("FchEmis"):
            fchemis = element.firstChild.nodeValue

        text = xmlTree.createTextNode(fchemis)
        fe = xmlTree.createElement("FE")
        fe.appendChild(text)
        dd.appendChild(fe)

        rutrecep = ""
        for element in xmlTree.getElementsByTagName("RUTRecep"):
            rutrecep = element.firstChild.nodeValue

        text = xmlTree.createTextNode(rutrecep)
        rr = xmlTree.createElement("RR")
        rr.appendChild(text)
        dd.appendChild(rr)

        rznsocrecep = ""
        for element in xmlTree.getElementsByTagName("RznSocRecep"):
            rznsocrecep = element.firstChild.nodeValue

        text = xmlTree.createTextNode(rznsocrecep)
        rsr = xmlTree.createElement("RSR")
        rsr.appendChild(text)
        dd.appendChild(rsr)

        mntotal = ""
        for element in xmlTree.getElementsByTagName("MntTotal"):
            mntotal = element.firstChild.nodeValue

        text = xmlTree.createTextNode(mntotal)
        mnt = xmlTree.createElement("MNT")
        mnt.appendChild(text)
        dd.appendChild(mnt)

        it1 = xmlTree.createElement("IT1")
        text = xmlTree.createTextNode(item1)
        it1.appendChild(text)
        dd.appendChild(it1)

        # Procedo a cargar el nodo caf
        caf = parseString(open('/home/esteban/appdte/caf/F76040308T33.xml').read())
        nodecaf = caf.getElementsByTagName("CAF")[0]
        dd.appendChild(nodecaf)

        tsted = xmlTree.createElement("TSTED")

        import time
        fecha = time.strftime("%Y-%m-%d")
        hora = time.strftime("%X")
        text = xmlTree.createTextNode(fecha + "T" + hora)
        tsted.appendChild(text)
        dd.appendChild(tsted)

        ted.appendChild(dd)

        auxdd = dd.toxml()
        auxdd = auxdd.replace("\n", "")

        # Obtengo la clave rsa del caf y la guardo en una variable
        clave = ""
        rsask = caf.getElementsByTagName("RSASK")

        for node1 in rsask:
            for node2 in node1.childNodes:
                if node2.nodeType == Node.TEXT_NODE:
                    clave = node2.data

        key = RSA.importKey(clave)
        message = auxdd.encode('iso-8859-1')

        h = SHA1.new(message)
        signature = pkcs1_15.new(key).sign(h)

        firma = base64.b64encode(signature).decode('utf-8')

        frmt = xmlTree.createElement("FRMT")
        frmt.setAttribute("algoritmo", "SHA1withRSA")
        text = xmlTree.createTextNode(firma)
        frmt.appendChild(text)
        ted.appendChild(frmt)
        documento.appendChild(ted)

        tmstfirma = xmlTree.createElement("TmstFirma")
        text = xmlTree.createTextNode(fecha + "T" + hora)
        tmstfirma.appendChild(text)
        documento.appendChild(tmstfirma)

        contenido = xmlTree.toxml()
        return contenido
