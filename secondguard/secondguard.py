from .utils import BASE_URL
import requests
import json


class RateLimitError(Exception):
    pass


class BadRequestError(Exception):
    pass


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

    if r.status_code == 400:
        print(response)
        raise BadRequestError("Bad Request: %s" % response)

    if r.status_code == 429:
        print(response)
        raise RateLimitError("SecondGuard Rate Limit Exceeded: %s" % response)

    # Will throw an error if these fields don't exist
    return {
        "key_recovered": response["key_recovered"],
        "request_sha256": response["request_sha256"],
        "ratelimit_limit": response["ratelimit_limit"],
        "ratelimit_remaining": response["ratelimit_remaining"],
        "ratelimit_resets_in": response["ratelimit_resets_in"],
    }
