#!/usr/bin/python
#-*- coding: UTF-8 -*-
from xml.dom.minidom import *
import time

class ENVIODTE:

	def make_envio(self,documento,infoemisor,infoiddoc):							
		doc = Document()
		#creo el nodo DTE
		enviodte = doc.createElement("envio:EnvioDTE")
		enviodte.setAttribute("xmlns","http://www.sii.cl/SiiDte")
		enviodte.setAttribute("xmlns:envio","http://www.sii.cl/SiiDte")
		enviodte.setAttribute("xmlns:dsig","http://www.w3.org/2000/09/xmldsig#")
		enviodte.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
		enviodte.setAttribute("xsi:schemaLocation","http://www.sii.cl/SiiDte EnvioDTE_v10.xsd")
		enviodte.setAttribute("version","1.0")

		setdte = doc.createElement('SetDTE')
		setdte.setAttribute("ID","SetDoc")
		caratula = doc.createElement('Caratula')
		caratula.setAttribute("version","1.0")
		rutemisor = doc.createElement("RutEmisor")
		text = doc.createTextNode(infoemisor['rutemisor'])
		rutemisor.appendChild(text)

		caratula.appendChild(rutemisor)
		rutenvia = doc.createElement("RutEnvia")
		text = doc.createTextNode(infoemisor['rutenvia'])
		rutenvia.appendChild(text)



		caratula.appendChild(rutenvia)
		rutreceptor = doc.createElement("RutReceptor")
		text = doc.createTextNode('60803000-K')
		rutreceptor.appendChild(text)

		caratula.appendChild(rutreceptor)
		fchresol  = doc.createElement("FchResol")
		text = doc.createTextNode(infoemisor['fecharesol'])
		fchresol.appendChild(text)

		caratula.appendChild(fchresol)
		nroresol = doc.createElement("NroResol")
		text = doc.createTextNode(infoemisor['numresol'])
		nroresol.appendChild(text)
		caratula.appendChild(nroresol)

		fecha = time.strftime("%Y-%m-%d")
		hora = time.strftime("%X")


		tmstfirmaenv = doc.createElement("TmstFirmaEnv")
		text = doc.createTextNode(fecha+"T"+hora)
		tmstfirmaenv.appendChild(text)

		caratula.appendChild(tmstfirmaenv)


		subtotdte = doc.createElement("SubTotDTE")
		tpodte = doc.createElement("TpoDTE")
		text = doc.createTextNode(infoiddoc['tipodte'])
		tpodte.appendChild(text)

		subtotdte.appendChild(tpodte)
		nrodte = doc.createElement("NroDTE")
		text = doc.createTextNode('1')
		nrodte.appendChild(text)


		subtotdte.appendChild(nrodte)

		caratula.appendChild(subtotdte)
		setdte.appendChild(caratula)


		enviodte.appendChild(setdte)
		doc.appendChild(enviodte)
		#aplico indentado antes de guardar
		contenido = doc.toprettyxml(indent="  ")
		f = open("enviodte.xml", "w", encoding='iso-8859-1')
		f.write(contenido)
		f.close()





		#ahora abro el dte firmado y lo inserto en el sobre electrónico

		contenidodte = documento.replace('<?xml version="1.0"?>','')


		f = open("enviodte.xml", "r",encoding='iso-8859-1')
		contenidoenvio = f.read()
		f.close()

		#agrego el dte
		contenidoenvio = contenidoenvio.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="ISO-8859-1"?>')
		contenidoenvio = contenidoenvio.replace('</Caratula>','</Caratula>'+contenidodte)

		#añado las secciones de firma
		dsig = """ <dsig:Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
		<dsig:SignedInfo>
		<dsig:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
		<dsig:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
		<dsig:Reference URI="#SetDoc">
		<dsig:Transforms>
		<dsig:Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
		</dsig:Transforms>
		<dsig:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
		<dsig:DigestValue/>
		</dsig:Reference>
		</dsig:SignedInfo>
		<dsig:SignatureValue/>
		<dsig:KeyInfo>
		<dsig:KeyValue/>
		<dsig:X509Data>
		<dsig:X509Certificate/>
		</dsig:X509Data>
		</dsig:KeyInfo>
		</dsig:Signature> """
		contenidoenvio = contenidoenvio.replace('</SetDTE>','</SetDTE>'+'\n'+dsig)




		f = open("enviodte.xml", "w",encoding='iso-8859-1')
		f.write(contenidoenvio)
		f.close()



		import os
		os.system("xmlsec1 --sign --pwd 'Seba0404' --privkey-pem key.pem,cert.pem --id-attr:ID SetDTE --node-xpath /envio:EnvioDTE/dsig:Signature enviodte.xml > enviodtefirmado.xml")

		f = open("enviodtefirmado.xml", "r",encoding='iso-8859-1')
		contenidoenvio = f.read()
		f.close()
		return contenidoenvio