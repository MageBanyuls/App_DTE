from signdte import *
from timbre import *

# Instancia de la clase TIMBRE

timbre = TIMBRE()

# Instancia de la clase SIGNDTE
signer = SIGNDTE()

# XML de ejemplo que quieres firmar
xml_content = """<Documento ID="DOC33">
<Contenido>Ejemplo</Contenido>
</Documento>"""

# Rutas a los archivos key.pem y cert.pem
key_path = "key.pem"
cert_path = "cert.pem"
password = "amulen1956"

# Firmar el XML
signed_xml = signer.signDTE(xml_content, key_path, cert_path, password)

# Guardar el resultado firmado en un archivo
with open("resultado_firmado.xml", "w") as result_file:
    result_file.write(signed_xml)

print("El documento XML ha sido firmado y guardado como 'resultado_firmado.xml'.")