from base64 import b64decode
from os import urandom
from secondguard.pyca import (
    symmetric_encrypt,
    symmetric_decrypt,
    asymmetric_encrypt,
    asymmetric_decrypt,
)

# TODO: move to a setup class?
from tests.utils import PUBKEY_STR, PRIVKEY_STR, _fetch_testing_pubkey

# TODO: come up with less HACKey way to test many times
# TODO: add static decrypt test vectors


def perform_symmetric_encryption_decryption(num_bytes=1000):
    secret = urandom(num_bytes)
    ciphertext, key = symmetric_encrypt(secret)
    recovered_secret = symmetric_decrypt(ciphertext=ciphertext, key=key)
    assert secret == recovered_secret


def test_symmetric(cnt=100):
    for attempt in range(cnt):
        perform_symmetric_encryption_decryption(num_bytes=attempt * 100)


def perform_asymmetric_encryption_decryption(rsa_privkey, rsa_pubkey, secret):
    ciphertext_b64 = asymmetric_encrypt(bytes_to_encrypt=secret, rsa_pubkey=PUBKEY_STR)
    assert len(b64decode(ciphertext_b64)) == 512
    recovered_secret = asymmetric_decrypt(
        ciphertext_b64=ciphertext_b64, rsa_privkey=PRIVKEY_STR
    )
    assert secret == recovered_secret


def test_asymmetric(cnt=10):
    for _ in range(cnt):
        # This represents the info you're trying to protect:
        secret = urandom(64)
        perform_asymmetric_encryption_decryption(
            rsa_privkey=PRIVKEY_STR, rsa_pubkey=PUBKEY_STR, secret=secret
        )
