from .utils import BASE_URL
import requests
import json


def perform_asymmetric_decrypt_secondguard(todecrypt_b64, api_token="SG-XXXX"):
    assert type(todecrypt_b64) is bytes, todecrypt_b64

    url = BASE_URL + "api/v1/decrypt"
    payload = {
        "api_token": api_token,
        "asymmetric_ciphertext_b64": todecrypt_b64.decode(),
    }

    # TODO: change protocol to not need this?
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)

    response = r.json()

    # Will throw an error if these fields don't exist
    return {
        "decrypted": response["decrypted"],
        "asymmetric_ciphertext_dsha256": response["asymmetric_ciphertext_dsha256"],
        "ratelimit_limit": response["ratelimit_limit"],
        "ratelimit_remaining": response["ratelimit_remaining"],
        "ratelimit_reset": response["ratelimit_reset"],
    }
