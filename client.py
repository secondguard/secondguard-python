from secondguard import perform_asymmetric_decrypt_secondguard
from pyca import symmetric_encrypt, symmetric_decrypt, asymmetric_encrypt, asymmetric_decrypt
from utils import _assert_valid_api_token



def secondguard_encrypt(to_encrypt, pubkey, api_token, confirm=True):
    """
    Note that we DO NOT return the symmetric key generated as we do NOT want to save this locally!
    """
    assert type(to_encrypt) is bytes, to_encrypt
    assert type(pubkey) is bytes, pubkey
    _assert_valid_api_token(api_token)

    ciphertext, key = symmetric_encrypt(
        to_encrypt=to_encrypt,
        confirm=confirm,
    )
    asymm_ciphertext = asymmetric_encrypt(
        bytes_to_encrypt=key,
        pubkey_bytes=pubkey,
    )

    # To save locally in our DB:
    # We are returning the following format: (local_ciphertext, sg_recovery_instructions)
    return ciphertext, asymm_ciphertext


def secondguard_decrypt(local_ciphertext_to_decrypt, sg_recovery_instructions, api_token):
    assert type(local_ciphertext_to_decrypt) is bytes, local_ciphertext_to_decrypt

    # Recover symmetric key from SG HSM
    decrypted_recovery_instructions = perform_asymmetric_decrypt_secondguard(
        todecrypt_b64=sg_recovery_instructions,
        api_token=api_token,
    )

    # Grab the key to use for local decryption
    symmetric_key_used = decrypted_recovery_instructions.pop('decrypted')

    # Locally decrypt ciphertext using recovered key
    secret_recovered = symmetric_decrypt(
        ciphertext=local_ciphertext_to_decrypt,
        key=symmetric_key_used,
    )

    # Return the secret and the rate limit info (decrypted_recovery_instructions is now just rate limit info):
    return secret_recovered, decrypted_recovery_instructions
