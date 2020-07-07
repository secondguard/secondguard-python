from utils import BASE_URL
import requests
import json


def perform_asymmetric_decrypt_secondguard(todecrypt_b64, api_token='SG-XXXX'):
    assert type(todecrypt_b64) is bytes, todecrypt_b64
    
    r = requests.post(
            BASE_URL + "api/v1/decrypt",
            json={
                'api_token': api_token,
                'asymmetric_ciphertext_b64': todecrypt_b64.decode(),
            },
            headers = {"Content-Type": "application/json"},
        )

    response = r.json()

    # Will throw an error if these fields don't exist
    return {
        'decrypted': response['decrypted'],
        'ratelimit_limit': response['ratelimit_limit'],
        'ratelimit_remaining': response['ratelimit_remaining'],
        'ratelimit_reset': response['ratelimit_reset'],
    }
