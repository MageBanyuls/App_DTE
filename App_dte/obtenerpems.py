from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.backends import default_backend

pfx_path=r"C:\Users\USUARIO\Desktop\validate_dte\docs\17461924-7 (Seba0404).pfx"
with open(pfx_path, 'rb') as f:
        pfx_data = f.read()

# Datos del PFX y contraseña
pfx_password = b'Seba0404'  # Reemplaza con la contraseña de tu archivo PFX

# Cargar el PFX
p12 = load_key_and_certificates(pfx_data, pfx_password, backend=default_backend())
private_key = p12[0]
cert = p12[1]

# Convertir la clave privada al formato PEM
private_key_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode('ISO-8859-1')

# Convertir el certificado al formato PEM
cert_pem = cert.public_bytes(Encoding.PEM).decode('ISO-8859-1')

# Guardar la clave privada en un archivo key.pem
with open('key.pem', 'w', encoding='ISO-8859-1') as key_file:
    key_file.write(private_key_pem)

# Guardar el certificado en un archivo cert.pem
with open('cert.pem', 'w', encoding='ISO-8859-1') as cert_file:
    cert_file.write(cert_pem)

print("Archivos key.pem y cert.pem han sido creados.")
