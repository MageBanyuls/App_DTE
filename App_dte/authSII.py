#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree
import requests
import os

class AuthSII:

    def getSeed(self):
        url = "https://palena.sii.cl/DTEWS/CrSeed.jws?WSDL"
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'Access-Control-Allow-Credentials': 'true',
            'SOAPAction': 'getSeed'
        }

        body = """ 
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header/>
                <soapenv:Body>
                    <getSeed></getSeed>
                </soapenv:Body>
            </soapenv:Envelope> """

        response = requests.post(url, data=body, headers=headers, verify=False)
        contenido = response.content.decode('utf-8')
        print(contenido)

        salida = contenido.replace("&lt;", "<").replace("&quot;", "\"").replace("&gt;", ">")
        original = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        reemplazo = ""
        salida = salida.replace(original, reemplazo)

        return salida

    def getToken(self, objseed):
        xmlTree = etree.fromstring(objseed.encode('utf-8'))
        valorsemilla = xmlTree.find('.//SEMILLA').text.strip('+-0')

        gettoken = etree.Element("getToken")
        item = etree.SubElement(gettoken, "item")
        semilla = etree.SubElement(item, "Semilla")
        semilla.text = valorsemilla

        contenido = etree.tostring(gettoken, pretty_print=True, encoding='unicode')

        sig = """<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
            <SignedInfo>
                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                <Reference URI="">
                    <Transforms>
                        <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                    </Transforms>
                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                    <DigestValue/>
                </Reference>
            </SignedInfo>
            <SignatureValue/>
            <KeyInfo>
                <KeyValue/>
                <X509Data>
                    <X509Certificate/>
                </X509Data>
            </KeyInfo>
        </Signature>"""

        contenido = contenido.replace('</getToken>', sig + '</getToken>')
        
        # Guardar el XML del documento
        with open("gettoken.xml", "w", encoding='utf-8') as f:
            f.write(contenido)

        os.system("xmlsec1 --sign --privkey-pem key.pem,cert.pem --pwd 'amulen1956' gettoken.xml > gettokensigned.xml")

        with open("gettokensigned.xml", "r", encoding='utf-8') as f:
            contenido = f.read()

        contenidoa = contenido.replace('<?xml version="1.0"?>', '')

        url = "https://palena.sii.cl/DTEWS/GetTokenFromSeed.jws?WSDL"
        headers = {
            'content-type': 'text/xml; charset=utf-8',
            'Access-Control-Allow-Credentials': 'true',
            'SOAPAction': 'getToken'
        }

        body = """ 
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header/>
                <soapenv:Body>
                    <getToken>
                        <pszXml><![CDATA[
        """ + contenidoa + """]]></pszXml></getToken></soapenv:Body></soapenv:Envelope>"""

        response = requests.post(url, data=body, headers=headers, verify=False)
        respuesta = response.content.decode('utf-8')

        salida = respuesta.replace("&lt;", "<").replace("&quot;", "\"").replace("&gt;", ">")
        original = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        reemplazo = ""
        salida = salida.replace(original, reemplazo)

        xmlTree = etree.fromstring(salida.encode('utf-8'))
        valortoken = xmlTree.find('.//TOKEN').text

        return valortoken
