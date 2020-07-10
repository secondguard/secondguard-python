## SecondGuard Python Client Library


## Setup

Install
```bash
$ pip3 install --upgrade secondguard
```

## Use

Encrypt some data using the testing API token and RSA pubkey (no account needed):
```python
from secondguard import sg_hybrid_encrypt, sg_hybrid_decrypt

your_secret = b"attack at dawn!"

# Testing credentials (normally saved in your app's config):
API_TOKEN = 'SG-XXXX'
YOUR_PUBKEY = '''-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxY9sgHqrHRkfppnOJACr\nhwYxHP4d/OUUzbTiNFfcFoCyCUCL6dnLql1WPfaUyYWeLEQ4NTFI9Nfdy9tka6ZO\n75V3LCW5l2TMkbb0BvWnAcIK3lMY19kfFyImAoLvcZcAevi0ogkOn20zDrxVhlpv\nQAu3OMCQmc1aMgv6pp1FO4v3OjiXNp1AQQw8CIHnQzlLmGSMeUK1hdCcSGXq5qLA\nXrKwdkA8K6gDi67A43ZcWzew1KF8OwtA2WyLRfbzGaXqqq2pLNcrt90v64azkk+Q\nn8JTJym7k30Jv7zbhsGR08dvk6zn7TrNMn1TsIwflDFGSpzSCAQcz1gR+0GiwGvk\nqQkKeNhTAUHOdf7IONEpmZ+46O4uUmtAXu5lI0D5dPtl2M5ZtAjxRMvXX65QeNd7\nMwcoXy5LaUMnDVl8Sq8OL8dj8PMKiqO7m/yMuMfXgEd9EcdzFt80rRUCH3/H3+MT\nQMZdlbNASA5d//MOxERsb1ildEyfTQpSWvyeGIpCCtPmq3yJbKat95RTUX4uJPLi\nKFCifkVhirl+XxdDK6L0gly0kZEW41qyKZL+++5M6NalsBsMr5AFAUF0Ws4E+aWf\n6Zm8FDi6G4ZpAmVpP6bmqY+GoTFBQKXezICAwsJ6Dhy8UUHxDRQIiNTSLVnO5wgR\ncRfaU/jG6gorIFQvw8mw2hcCAwEAAQ==\n-----END PUBLIC KEY-----\n'''

# Encrypt locally (symmetrically and asymmetrically) and save the results to your DB:
local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
    to_encrypt=your_secret,
    rsa_pubkey=YOUR_PUBKEY, 
    api_token=API_TOKEN,
)

# Asymmetrically decrypt sg_recovery_instructions (via SecondGuard API) and use it to symmetrically decrypt local_ciphertext: 
secret_recovered, rate_limit_info = sg_hybrid_decrypt( 
    local_ciphertext_to_decrypt=local_ciphertext, 
    sg_recovery_instructions=sg_recovery_instructions,
    api_token=API_TOKEN,
)

assert your_secret == secret_recovered
```

See [test_client.py](https://github.com/secondguard/secondguard-python/blob/master/tests/test_client.py) to see how the protocol works.

---

### Development

Pull requests welcome!

Check out the code:
```bash
$ git checkout git@github.com:secondguard/secondguard-python.git && cd secondguard-python.git
```

Create & activate a virtual environment, install dependencies & this library, then run tests:
```bash
$ python3 -m virtualenv .venv3 && source .venv3/bin/activate && pip3 install -r requirements.txt && pip3 install --editable . && pytest -v
```
(unfortunately, running tests requires intalling a `--editable` local version of this repo)

To update `requirements.txt` change `requirements.in` and then run:
```bash
$ pip-compile requirements.in
```

How these INSECURE testing RSA keys were created:
```bash
$ openssl genrsa -out insecureprivkey.pem 4096 && openssl rsa -in insecureprivkey.pem -pubout -out insecurepubkey.crt
```

Package and upload to [PyPI](https://pypi.org/project/secondguard/):
```bash
$ python3 setup.py sdist bdist_wheel
$ python3 -m pip install --upgrade twine
$ python3 -m twine upload dist/*
```
