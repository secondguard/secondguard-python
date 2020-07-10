from base64 import b64encode, b64decode, urlsafe_b64decode

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from secondguard.utils import assert_same, _assert_valid_privkey, _assert_valid_pubkey


def symmetric_encrypt(to_encrypt, confirm=True):
    assert type(to_encrypt) is bytes, to_encrypt

    key = Fernet.generate_key()
    f = Fernet(key)
    ciphertext = f.encrypt(to_encrypt)

    if confirm:
        # Can be set to false for better performance
        assert_same(f.decrypt(ciphertext), to_encrypt)

    # Once asymmetrically encrypted, we'll want to throw away the key
    return ciphertext, key


def symmetric_decrypt(ciphertext, key):
    assert len(urlsafe_b64decode(key)) == 32, key

    f = Fernet(key)
    return f.decrypt(ciphertext)


def asymmetric_encrypt(bytes_to_encrypt, rsa_pubkey):
    assert type(bytes_to_encrypt) is bytes, bytes_to_encrypt
    _assert_valid_pubkey(rsa_pubkey)

    # Extract and parse the public key as a PEM-encoded RSA key.
    pubkey_bytes = rsa_pubkey.encode()
    rsa_key = serialization.load_pem_public_key(pubkey_bytes, backend=default_backend())

    # Construct the padding. Note that the padding differs based on key choice.
    sha256 = hashes.SHA256()
    mgf = padding.MGF1(algorithm=sha256)
    pad = padding.OAEP(mgf=mgf, algorithm=sha256, label=None)

    # Encrypt the data using the public key.
    ciphertext = rsa_key.encrypt(bytes_to_encrypt, pad)

    return b64encode(ciphertext)


def asymmetric_decrypt(ciphertext_b64, rsa_privkey, password=None):
    """
    Do NOT use this method and instead use the SecondGuard HSM for better security.
    """

    assert type(ciphertext_b64) is bytes, ciphertext_b64
    _assert_valid_privkey(rsa_privkey)

    ciphertext_bytes = b64decode(ciphertext_b64)

    privkey_bytes = rsa_privkey.encode()
    rsa_key = serialization.load_pem_private_key(
        privkey_bytes, password=password, backend=default_backend()
    )

    # Construct the padding. Note that the padding differs based on key choice.
    sha256 = hashes.SHA256()
    mgf = padding.MGF1(algorithm=sha256)
    pad = padding.OAEP(mgf=mgf, algorithm=sha256, label=None)

    # Decrypt the data using the private key.
    return rsa_key.decrypt(ciphertext_bytes, pad)
