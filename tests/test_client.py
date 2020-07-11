from base64 import b64decode
from hashlib import sha256
from os import urandom

from secondguard.utils import assert_same
from secondguard.main import sg_hybrid_encrypt, sg_hybrid_decrypt

from tests.testing_utils import PUBKEY_STR, TESTING_API_TOKEN, _fetch_testing_pubkey


# TODO: add static decrypt test vectors

TESTING_RSA_PUBKEY = _fetch_testing_pubkey()


def perform_sg_hybrid_encryption_and_decryption(num_bytes=1000):
    # This represents the info you're trying to protect (could be of any length):
    secret = urandom(num_bytes)

    local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
        to_encrypt=secret, rsa_pubkey=TESTING_RSA_PUBKEY, api_token=TESTING_API_TOKEN
    )

    secret_recovered, recovery_info = sg_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        sg_recovery_instructions=sg_recovery_instructions,
        api_token=TESTING_API_TOKEN,
    )

    # Important test:
    assert secret == secret_recovered

    # sha256(sg_recovery_instructions) matches returned 
    assert sha256(b64decode(sg_recovery_instructions)).hexdigest() == recovery_info["asymmetric_ciphertext_dsha256"]

    # TODO: test actual rate limit behavior in recovery_info
    assert set(recovery_info.keys()) == set(
        ("ratelimit_limit", "ratelimit_remaining", "ratelimit_reset", "asymmetric_ciphertext_dsha256")
    )


def test_sg_hybrid_encryption_and_decryption(cnt=5):
    for attempt in range(cnt):
        perform_sg_hybrid_encryption_and_decryption(num_bytes=attempt * 1000)
