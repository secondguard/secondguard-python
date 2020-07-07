from os import urandom

from secondguard.utils import _fetch_testing_pubkey, assert_same, PUBKEY_STR, TESTING_API_TOKEN
from secondguard.main import sg_hybrid_encrypt, sg_hybrid_decrypt


# TODO: add static decrypt test vectors

TESTING_RSA_PUBKEY = _fetch_testing_pubkey()

for cnt in range(5):
    pass


def perform_sg_hybrid_encryption_and_decryption(num_bytes=1000):
    # This represents the info you're trying to protect (could be of any length):
    secret = urandom(num_bytes)

    local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
        to_encrypt=secret,
        rsa_pubkey=TESTING_RSA_PUBKEY,
        api_token=TESTING_API_TOKEN,
    )

    secret_recovered, rate_limit_info = sg_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        sg_recovery_instructions=sg_recovery_instructions,
        api_token=TESTING_API_TOKEN,
    )

    # Important test:
    assert secret == secret_recovered

    # TODO: test rate_limit_info content
    assert set(rate_limit_info.keys()) == set(('ratelimit_limit', 'ratelimit_remaining', 'ratelimit_reset'))


def test_sg_hybrid_encryption_and_decryption(cnt=5):
    for attempt in range(cnt):
        perform_sg_hybrid_encryption_and_decryption(num_bytes=attempt*1000)
