import os

class SIGNDTE:

    def signDTE(self, contenido):
        sig = """<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo>
        <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <Reference URI="#DOC33">
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

        # Insert the signature template before the closing </Documento> tag
        contenido = contenido.replace('</Documento>', '</Documento>' + '\n' + sig)
        
        with open("dte.xml", "w") as f:
            f.write(contenido)

        os.system("xmlsec1 --sign --pwd 'amulen1956' --privkey-pem key.pem,cert.pem --id-attr:ID Documento dte.xml > dtefirmado.xml")

        with open("dtefirmado.xml", "r") as f:
            contenido = f.read()

        return contenido

    def signDTE_xml(self, xml_content, key_path, cert_path, password, output_file="dtefirmado.xml"):
        sig_template = """<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo>
        <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <Reference URI="#DOC33">
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

        
        # Insert the signature template before the closing </Documento> tag
        modified_xml_content = xml_content.replace('</Documento>', '</Documento>' + '\n' + sig_template)

        # Write the modified XML content to a temporary file
        with open("dte.xml", "w") as temp_xml_file:
            temp_xml_file.write(modified_xml_content)

        # Sign the document using xmlsec1
        sign_command = (
            f"xmlsec1 --sign --pwd '{password}' "
            f"--privkey-pem {key_path},{cert_path} --id-attr:ID Documento dte.xml > {output_file}"
        )
        os.system(sign_command)

        # Read the signed document and return its content
        with open(output_file, "r") as signed_xml_file:
            signed_xml_content = signed_xml_file.read()

        return signed_xml_content
