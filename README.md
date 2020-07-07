##

#### This is a rough proof-of-concept, do not use this with real data!
### Client and server API subject to breaking changes

Create a virtualenv, activate and install `requirements.txt`
```bash
$ python3 -m virtualenv .venv3 && source .venv3/bin/activate && pip3 install -r requirements.txt
```

Run tests:
```bash
$ py.test -v
=============================== test session starts ===============================
platform darwin -- Python 3.7.7, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/mflaxman/workspace/secondguard/.venv3/bin/python
cachedir: .pytest_cache
rootdir: /Users/mflaxman/workspace/secondguard
collected 3 items                                                                 

test_client.py::test_sg_hybrid_encryption PASSED                            [ 33%]
test_pyca.py::test_symmetric PASSED                                         [ 66%]
test_pyca.py::test_asymmetric PASSED                                        [100%]

================================ 3 passed in 0.94s ================================

```

Encrypt some data using test API key:
```python
from client import secondguard_encrypt, secondguard_decrypt

# Testing credentials:
your_secret = b"attack at dawn!"
API_TOKEN = 'SG-XXXX'
YOUR_PUBKEY = b'-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxY9sgHqrHRkfppnOJACr\nhwYxHP4d/OUUzbTiNFfcFoCyCUCL6dnLql1WPfaUyYWeLEQ4NTFI9Nfdy9tka6ZO\n75V3LCW5l2TMkbb0BvWnAcIK3lMY19kfFyImAoLvcZcAevi0ogkOn20zDrxVhlpv\nQAu3OMCQmc1aMgv6pp1FO4v3OjiXNp1AQQw8CIHnQzlLmGSMeUK1hdCcSGXq5qLA\nXrKwdkA8K6gDi67A43ZcWzew1KF8OwtA2WyLRfbzGaXqqq2pLNcrt90v64azkk+Q\nn8JTJym7k30Jv7zbhsGR08dvk6zn7TrNMn1TsIwflDFGSpzSCAQcz1gR+0GiwGvk\nqQkKeNhTAUHOdf7IONEpmZ+46O4uUmtAXu5lI0D5dPtl2M5ZtAjxRMvXX65QeNd7\nMwcoXy5LaUMnDVl8Sq8OL8dj8PMKiqO7m/yMuMfXgEd9EcdzFt80rRUCH3/H3+MT\nQMZdlbNASA5d//MOxERsb1ildEyfTQpSWvyeGIpCCtPmq3yJbKat95RTUX4uJPLi\nKFCifkVhirl+XxdDK6L0gly0kZEW41qyKZL+++5M6NalsBsMr5AFAUF0Ws4E+aWf\n6Zm8FDi6G4ZpAmVpP6bmqY+GoTFBQKXezICAwsJ6Dhy8UUHxDRQIiNTSLVnO5wgR\ncRfaU/jG6gorIFQvw8mw2hcCAwEAAQ==\n-----END PUBLIC KEY-----\n'

# Save this in your DB (only local encryption happens here):
local_ciphertext, sg_recovery_instructions = secondguard_encrypt(
    to_encrypt=your_secret,
    pubkey=YOUR_PUBKEY, 
    api_token=API_TOKEN,
)

# recover from SecondGuard (asymmetric decryption takes place via API and then symmetric decryption takes place locally):
secret_recovered, rate_limit_info = secondguard_decrypt( 
    local_ciphertext_to_decrypt=local_ciphertext, 
    sg_recovery_instructions=sg_recovery_instructions,
    api_token=API_TOKEN,
)

assert your_secret == secret_recovered
```

Update `requirements.txt`:
```bash
$ pip-compile requirements.in
```

Note that these INSECURE testing RSA keys were created with the following:
```bash
$ openssl genrsa -out localprivkey.pem 4096 && openssl rsa -in localprivkey.pem -pubout -out localpubkey.crt
```
