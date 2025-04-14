from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.hazmat.backends import default_backend

def extract_pem_from_p7b(p7b_file, output_pem_file):
    with open(p7b_file, 'rb') as f:
        p7b_data = f.read()

    # Load PKCS7 data
    certs = pkcs7.load_pem_pkcs7_certificates(p7b_data, default_backend())
    # If that fails, try DER instead:
    # certs = pkcs7.load_der_pkcs7_certificates(p7b_data, default_backend())

    with open(output_pem_file, 'wb') as f:
        for cert in certs:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Extracted {len(certs)} cert(s) to {output_pem_file}")

# Example usage
extract_pem_from_p7b("certificate.p7b", "output.pem")
