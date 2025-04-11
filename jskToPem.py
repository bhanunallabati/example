import jks
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load JKS keystore
keystore = jks.KeyStore.load("keystore.jks", "keystore_password")

# Loop through all private keys
for alias, pk_entry in keystore.private_keys.items():
    print(f"Processing entry: {alias}")

    # Extract private key (in PKCS8 DER format)
    pkey = serialization.load_der_private_key(
        pk_entry.pkey, password=None, backend=default_backend()
    )

    # Save private key as PEM
    with open(f"{alias}_key.pem", "wb") as key_file:
        key_file.write(pkey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save certificate chain as PEM
    with open(f"{alias}_cert.pem", "wb") as cert_file:
        for cert in pk_entry.cert_chain:
            cert_file.write(cert[1])  # cert[1] is the DER-encoded cert
