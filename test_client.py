from os import urandom
from utils import _fetch_testing_pubkey
from utils import assert_same

from client import secondguard_encrypt, secondguard_decrypt

TESTING_PUBKEY = _fetch_testing_pubkey()
API_TOKEN = 'SG-XXXX'


# TODO: add static decrypt test vectors

for cnt in range(5):
    pass


def perform_sg_hybrid_encryption(num_bytes=1000):
    # This represents the info you're trying to protect (could be of any length):
    secret = urandom(num_bytes)

    local_ciphertext, sg_recovery_instructions = secondguard_encrypt(
        to_encrypt=secret,
        pubkey=TESTING_PUBKEY,
        api_token=API_TOKEN,
    )

    secret_recovered, rate_limit_info = secondguard_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        sg_recovery_instructions=sg_recovery_instructions,
        api_token=API_TOKEN,
    )

    # Important test:
    assert secret == secret_recovered

    # TODO: test rate_limit_info content
    assert set(rate_limit_info.keys()) == set(('ratelimit_limit', 'ratelimit_remaining', 'ratelimit_reset'))


def test_sg_hybrid_encryption(cnt=5):
    for attempt in range(cnt):
        perform_sg_hybrid_encryption(num_bytes=attempt*1000)
