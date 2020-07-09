import requests
from secondguard.utils import BASE_URL
from pathlib import Path
import os

# For testing only
# Limited to 1 INSECURE pubkey, rate-limiting shared across all users
TESTING_API_TOKEN = 'SG-XXXX'


# TODO: move test to own directory?
key_dir = Path(__file__).absolute().parent.parent

with open(os.path.join(key_dir, 'insecureprivkey.pem'), 'r') as f:
    PRIVKEY_STR = f.read()
with open(os.path.join(key_dir, 'insecurepubkey.crt'), 'r') as f:
    PUBKEY_STR = f.read()

def _fetch_testing_pubkey(url=BASE_URL + "static/pubkey.crt"):
    return requests.get(url).content.decode('utf-8')
