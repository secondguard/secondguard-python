from base64 import b64decode
from datetime import datetime
from hashlib import sha256
from json import dumps

from secondguard.secondguard import perform_asymmetric_decrypt_secondguard
from secondguard.pyca import (
    symmetric_encrypt,
    symmetric_decrypt,
    asymmetric_encrypt,
    asymmetric_decrypt,
)
from secondguard.utils import _assert_valid_api_token, _assert_valid_pubkey


def sg_hybrid_encrypt(
    to_encrypt, rsa_pubkey, deprecate_at=None, confirm=True
):
    """
    What's happening under the hood:
      1. Symmetrically encrypt your information with a locally generated symmetric key (`key`) -> ciphertext
      2. Asymmetrically encrypt your `key` (and other decryption instructions) with your RSA pubkey (kept in an HSM) -> sg_recovery_instructions
      3. Return your local ciphertext

    Note that we DO NOT return the symmetric key (`key`) generated as we do NOT want to save this locally!
    """
    assert type(to_encrypt) is bytes, to_encrypt
    _assert_valid_pubkey(rsa_pubkey)
    assert type(deprecate_at) is datetime or deprecate_at is None, deprecate_at

    # Encrypt locally, generate a unique symmetric key
    local_ciphertext, localkey = symmetric_encrypt(
        to_encrypt=to_encrypt, confirm=confirm
    )

    # Create instructions to decrypt
    decryption_instructions_dict = {
        "key": localkey.decode()  # bytes not json serializable
    }
    if deprecate_at:
        # Round and add timezone
        decryption_instructions_dict["deprecate_at"] = (
            deprecate_at.replace(microsecond=0).astimezone().isoformat()
        )

    decryption_instructions_bytes = dumps(decryption_instructions_dict).encode()

    # Asymmetrically encrypt decryption instructions (locally)
    sg_recovery_instructions = asymmetric_encrypt(
        bytes_to_encrypt=decryption_instructions_bytes, rsa_pubkey=rsa_pubkey
    )

    # Save this locally in our DB:
    return local_ciphertext, sg_recovery_instructions


def sg_hybrid_decrypt(local_ciphertext_to_decrypt, sg_recovery_instructions, api_token):
    """
    Recover the symmetric key from SecondGuard (`symmetric_key_recovered`) and then use it to (locally) decrypt the data in your DB (`secret_recovered`).
    """
    assert type(local_ciphertext_to_decrypt) is bytes, local_ciphertext_to_decrypt

    # Recover symmetric key from SG HSM
    recovery_info = perform_asymmetric_decrypt_secondguard(
        todecrypt_b64=sg_recovery_instructions, api_token=api_token
    )

    # Grab the key to use for local decryption
    symmetric_key_recovered = recovery_info.pop("key_recovered")

    # Locally decrypt ciphertext using recovered key
    secret_recovered = symmetric_decrypt(
        ciphertext=local_ciphertext_to_decrypt, key=symmetric_key_recovered
    )

    # Return the recovered secret, and recovery_info (rate limit info & sha256(base64_decode(sg_recovery_instructions))):
    return secret_recovered, recovery_info


def sg_hybrid_encrypt_with_auditlog(
    to_encrypt, rsa_pubkey, deprecate_at=None, confirm=True
):
    """
    Convenience wrapper for sg_hybrid_encrypt method that also calculates the sha 256 hash digest of the asymetrically-encrypted symmetric key.
    This should be saved in your database with an index for easy querying.
    """
    local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
        to_encrypt, rsa_pubkey, deprecate_at=deprecate_at, confirm=confirm
    )
    return (
        local_ciphertext,
        sg_recovery_instructions,
        sha256(b64decode(sg_recovery_instructions)).hexdigest(),
    )
