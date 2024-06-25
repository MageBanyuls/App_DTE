import xml.etree.ElementTree as ET
import time
from lxml import etree
import xmlsec
import base64
import textwrap
from cryptography.hazmat.primitives import serialization


xml_file_path = r"C:\Users\USUARIO\Downloads\XML_nuestro\nuevo1-prueba.xml"
#xml_file_path = "./dte.xml"
# Configurar fecha de resolución
fecharesolucion = "2024-03-22"

# Ruta a cert.pem y key.pem
cert_pem_path = './cert.pem'
key_pem_path = './key.pem'

# Leer contenido del archivo XML con codificación ISO-8859-1
with open(xml_file_path, "r", encoding="ISO-8859-1") as f:
    xml_content = f.read()

# Eliminar el encabezado XML y encapsular los documentos DTE en un elemento raíz
xml_content = "<Root>" + xml_content.replace('<?xml version="1.0" encoding="ISO-8859-1"?>', '') + "</Root>"

try:
    root = ET.fromstring(xml_content)
except ET.ParseError as e:
    print(f"Error al parsear el XML: {e}")
    exit()

# Definir espacio de nombres
namespaces = {'sii': 'http://www.sii.cl/SiiDte'}

# Extraer todos los elementos DTE
dtes = root.findall('.//DTE', namespaces)
print(f"Se encontraron {len(dtes)} documentos DTE.")

# Obtener la información del primer DTE para construir la Caratula
if dtes:
    primer_dte = dtes[0]
    infoemisor = primer_dte.find('.//Emisor')
    infoiddoc = primer_dte.find('.//IdDoc')
    inforeceptor = primer_dte.find('.//Receptor')
    if infoemisor is not None and infoiddoc is not None:
        rutemisor = infoemisor.find('RUTEmisor').text
        rutenvia = "174619247"
        rutreceptor = inforeceptor.find('RUTRecep').text
    else:
        print("No se encontraron los elementos necesarios en el primer DTE.")
        exit()
else:
    print("No se encontraron documentos DTE.")
    exit()

class ENVIODTE:
    def make_envio(self, documentos_dte, infoemisor, infoiddoc):
        NSMAP = {
            None: "http://www.sii.cl/SiiDte",
            "envio": "http://www.sii.cl/SiiDte",
            "dsig": "http://www.w3.org/2000/09/xmldsig#",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

        enviodte = etree.Element("{http://www.sii.cl/SiiDte}EnvioDTE", nsmap=NSMAP, attrib={
            "version": "1.0",
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.sii.cl/SiiDte EnvioDTE_v10.xsd"
        })

        setdte = etree.SubElement(enviodte, "SetDTE", ID="SetDoc")

        caratula = etree.SubElement(setdte, "Caratula", version="1.0")

        rutemisor_elem = etree.SubElement(caratula, "RutEmisor")
        rutemisor_elem.text = infoemisor.find('RUTEmisor').text

        rutenvia_elem = etree.SubElement(caratula, "RutEnvia")
        rutenvia_elem.text = "17461924-7"

        rutreceptor_elem = etree.SubElement(caratula, "RutReceptor")
        rutreceptor_elem.text = rutreceptor

        fchresol_elem = etree.SubElement(caratula, "FchResol")
        fchresol_elem.text = fecharesolucion

        nroresol_elem = etree.SubElement(caratula, "NroResol")
        nroresol_elem.text = "0"

        fecha = time.strftime("%Y-%m-%d")
        hora = time.strftime("%X")

        tmstfirmaenv_elem = etree.SubElement(caratula, "TmstFirmaEnv")
        tmstfirmaenv_elem.text = fecha + "T" + hora

        subtotdte = etree.SubElement(caratula, "SubTotDTE")
        tpodte = etree.SubElement(subtotdte, "TpoDTE")
        tpodte.text = infoiddoc.find('TipoDTE').text

        nrodte = etree.SubElement(subtotdte, "NroDTE")
        nrodte.text = str(len(documentos_dte))

        for elemento_dte in documentos_dte:
            documento_xml = ET.tostring(elemento_dte, encoding="ISO-8859-1")
            dte_node = etree.fromstring(documento_xml)
            setdte.append(dte_node)

        contenido = etree.tostring(enviodte, pretty_print=True, xml_declaration=True, encoding="ISO-8859-1")
        with open("enviodte.xml", "wb") as f:
            f.write(contenido)

        # Leer el contenido XML guardado
        with open("enviodte.xml", "rb") as f:
            contenidoenvio = f.read()

        # Ahora vamos a firmar el XML usando xmlsec
        tree = etree.fromstring(contenidoenvio)

        # Crear la firma usando xmlsec
        signature_node = xmlsec.template.create(tree, xmlsec.constants.TransformInclC14N, xmlsec.constants.TransformRsaSha1, ns="ds")
        key_info = xmlsec.template.ensure_key_info(signature_node)

        # Agregar KeyValue manualmente
        key_value = etree.SubElement(key_info, "{http://www.w3.org/2000/09/xmldsig#}KeyValue")
        rsa_key_value = etree.SubElement(key_value, "{http://www.w3.org/2000/09/xmldsig#}RSAKeyValue")
        modulus = etree.SubElement(rsa_key_value, "{http://www.w3.org/2000/09/xmldsig#}Modulus")
        exponent = etree.SubElement(rsa_key_value, "{http://www.w3.org/2000/09/xmldsig#}Exponent")

        # Leer clave privada para obtener el modulus y el exponent
        with open(key_pem_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        print(private_key.public_key())

        modulus_text = base64.b64encode(
            private_key.public_key().public_numbers().n.to_bytes(
                (private_key.public_key().public_numbers().n.bit_length() + 7) // 8, 'big'
            )
        ).decode('ISO-8859-1')
        modulus.text = '\n'.join(textwrap.wrap(modulus_text, 76))

        exponent_text = base64.b64encode(
            private_key.public_key().public_numbers().e.to_bytes(
                (private_key.public_key().public_numbers().e.bit_length() + 7) // 8, 'big'
            )
        ).decode('ISO-8859-1')
        exponent.text = '\n'.join(textwrap.wrap(exponent_text, 76))

        # Agregar X509Data
        x509_data = xmlsec.template.add_x509_data(key_info)
        x509_certificate_node = xmlsec.template.x509_data_add_certificate(x509_data)
        with open(cert_pem_path, "r", encoding="ISO-8859-1") as cert_file:
            cert_pem = cert_file.read()
        x509_certificate_node_text = base64.b64encode(cert_pem.encode('ISO-8859-1')).decode('ISO-8859-1')
        x509_certificate_node.text = '\n'.join(textwrap.wrap(x509_certificate_node_text, 76))
        # Encontrar el nodo de SetDTE e insertar la firma
        namespaces = {'sii': 'http://www.sii.cl/SiiDte'}
        setdte_node = tree.find('.//sii:SetDTE', namespaces)
        if setdte_node is None:
            raise ValueError("No se encontró el nodo SetDTE en el documento XML.")
        setdte_node.addnext(signature_node)

        # Agregar el objeto de referencia
        setdte_id = setdte_node.get('ID')
        if setdte_id is None:
            raise ValueError("El nodo SetDTE no tiene un atributo ID.")
        
        ref = xmlsec.template.add_reference(signature_node, xmlsec.constants.TransformSha1, uri="#" + setdte_id)

        ctx = xmlsec.SignatureContext()
        key = xmlsec.Key.from_file(key_pem_path, xmlsec.constants.KeyDataFormatPem)
        key.load_cert_from_file(cert_pem_path, xmlsec.constants.KeyDataFormatPem)
        ctx.key = key

        # Registrar el nodo y el atributo ID
        ctx.register_id(setdte_node, "ID")

        # Intentar firmar el documento
        try:
            ctx.sign(signature_node)
            print("Firma realizada con éxito.")
        except xmlsec.Error as e:
            print(f"Error al firmar el documento: {e}")
            return None
        
        

        # Guardar el documento firmado
        signed_xml = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='ISO-8859-1')

        # Convertir los bytes a una cadena para realizar el reemplazo
        signed_xml_str = signed_xml.decode('ISO-8859-1')

        # Reemplazar las comillas en la declaración XML
        signed_xml_str = signed_xml_str.replace("<?xml version='1.0' encoding='ISO-8859-1'?>", '<?xml version="1.0" encoding="ISO-8859-1"?>')

        # Escribir el resultado en el archivo
        with open("DTEPRUEBA_DEVELOPERS_comillas.xml", "wb") as f:
            f.write(signed_xml_str.encode('ISO-8859-1'))

        return signed_xml

# Crear objeto DTE y el archivo XML
objDTE = ENVIODTE()
documento = objDTE.make_envio(dtes, infoemisor, infoiddoc)

