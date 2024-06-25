import requests
import os

class UPLOADSII:

    def uploadDTE(self,token,rutemisor,rutenvia,archivo):		
		
        arrayrutemisor = rutemisor.split("-")
        rutCompany = arrayrutemisor[0]
        dvCompany = arrayrutemisor[1]
        arrayrutenvia = rutenvia.split("-")
        rutSender = arrayrutenvia[0]
        dvSender = arrayrutenvia[1]

        cabecera = {
            'Accept':'*/*',
            #'Referer':'http://www.egga.cl',
            'Accept-Language':'es-cl',
            #'Content-Type':'multipart/form-data: boundary=7d23e2a11301c4',
            'Accept-Encoding':'gzip, deflate',
            'User-Agent':'Mozilla/4.0 (compatible; PROG 1.0; Windows NT 5.0; YComp 5.0.2.4)',
            #'Content-Length':'8653',
            'Connection':'Keep-Alive',
            'Cache-Control':'no-cache'

            }

        archivo={'archivo': os.open(archivo+'.xml','rb')}

            
        datos = {'rutCompany':rutCompany,'dvCompany':dvCompany,'rutSender':rutSender,'dvSender':dvSender}
            

        cookie = {'TOKEN':token}
        conexion = requests.post('https://maullin.sii.cl/cgi_dte/UPL/DTEUpload',headers=cabecera,cookies=cookie,files=archivo,data=datos)	

        respuesta = conexion.content
        return respuesta