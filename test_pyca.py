from os import urandom
from pyca import (
    symmetric_encrypt,
    symmetric_decrypt,
    asymmetric_encrypt,
    asymmetric_decrypt,
)

from utils import _fetch_testing_pubkey


# TODO: move to a setup class?
from utils import PUBKEY_STR, PRIVKEY_STR

# TODO: come up with less HACKey way to test many times
# TODO: add static decrypt test vectors

def perform_symmetric_encryption_decryption(num_bytes=1000):
    secret = urandom(num_bytes)
    ciphertext, key = symmetric_encrypt(secret)
    recovered_secret = symmetric_decrypt(ciphertext=ciphertext, key=key)
    assert secret == recovered_secret

def test_symmetric(cnt=100):
    for attempt in range(cnt):
        print(attempt)
        perform_symmetric_encryption_decryption(num_bytes=attempt*100)


def perform_asymmetric_encryption_decryption(privkey_str, rsa_pubkey):
    bytes_to_encrypt = urandom(32)
    ciphertext_b64 = asymmetric_encrypt(bytes_to_encrypt=bytes_to_encrypt, rsa_pubkey=PUBKEY_STR)
    recovered_bytes = asymmetric_decrypt(ciphertext_b64=ciphertext_b64, rsa_privkey=PRIVKEY_STR)
    assert bytes_to_encrypt == recovered_bytes


def test_asymmetric(cnt=10):
    for attempt in range(cnt):
        perform_asymmetric_encryption_decryption(privkey_str=PRIVKEY_STR, rsa_pubkey=PUBKEY_STR)

