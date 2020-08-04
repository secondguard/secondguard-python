from base64 import b64decode
from datetime import datetime, timedelta
from hashlib import sha256
from os import urandom

from secondguard import (
    sg_hybrid_encrypt,
    sg_hybrid_encrypt_with_auditlog,
    sg_hybrid_decrypt,
    BadRequestError,
)

from tests.utils import PUBKEY_STR, TESTING_API_TOKEN, _fetch_testing_pubkey


# TODO: add static decrypt test vectors

TESTING_RSA_PUBKEY = _fetch_testing_pubkey()


def _assert_valid_recovery_info(recovery_info_dict):
    # TODO: test actual rate limit behavior in recovery_info
    for k in ("ratelimit_limit", "ratelimit_remaining", "ratelimit_resets_in"):
        assert type(recovery_info_dict[k]) is int, recovery_info_dict[k]

    # Confirm no other fields returned
    assert set(recovery_info_dict.keys()) == set(
        (
            "ratelimit_limit",
            "ratelimit_remaining",
            "ratelimit_resets_in",
            "request_sha256",
        )
    )


def perform_sg_hybrid_encryption_and_decryption_with_auditlog(
    secret, deprecate_at=None
):
    local_ciphertext, sg_recovery_instructions, sg_recovery_instructions_digest = sg_hybrid_encrypt_with_auditlog(
        to_encrypt=secret,
        rsa_pubkey=TESTING_RSA_PUBKEY,
        deprecate_at=deprecate_at,
    )

    secret_recovered, recovery_info = sg_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        sg_recovery_instructions=sg_recovery_instructions,
        api_token=TESTING_API_TOKEN,
    )

    assert secret == secret_recovered
    assert (
        sg_recovery_instructions_digest == recovery_info["request_sha256"]
    )
    _assert_valid_recovery_info(recovery_info)


def perform_sg_hybrid_encryption_and_decryption(secret, deprecate_at=None):
    local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
        to_encrypt=secret,
        rsa_pubkey=TESTING_RSA_PUBKEY,
        deprecate_at=deprecate_at,
    )

    secret_recovered, recovery_info = sg_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        sg_recovery_instructions=sg_recovery_instructions,
        api_token=TESTING_API_TOKEN,
    )

    assert secret == secret_recovered
    # sha256(sg_recovery_instructions) matches returned:
    assert (
        sha256(b64decode(sg_recovery_instructions)).hexdigest()
        == recovery_info["request_sha256"]
    )
    _assert_valid_recovery_info(recovery_info)


def test_sg_hybrid_encryption_and_decryption():
    secret = urandom(1000)
    future_expiry = datetime.now() + timedelta(days=100)
    past_expiry = datetime.now() - timedelta(days=100)

    for deprecate_at in (None, future_expiry):
        perform_sg_hybrid_encryption_and_decryption(
            secret=secret, deprecate_at=deprecate_at
        )
        perform_sg_hybrid_encryption_and_decryption_with_auditlog(
            secret=secret, deprecate_at=deprecate_at
        )

    # Confirm that an expired key throws an error:
    try:
        perform_sg_hybrid_encryption_and_decryption(
            secret=secret, deprecate_at=past_expiry
        )
        assert False
    except BadRequestError:
        assert True

    try:
        perform_sg_hybrid_encryption_and_decryption_with_auditlog(
            secret=secret, deprecate_at=past_expiry
        )
        assert False
    except BadRequestError:
        assert True
