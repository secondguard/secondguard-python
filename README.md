## This is not production-ready code, do not use this with real data!
### Client and server API subject to breaking changes


## Setup

Create a virtualenv, activate, install `requirements.txt` (including this repo) and run tests:
```bash
$ python3 -m virtualenv .venv3 && source .venv3/bin/activate && pip3 install -r requirements.txt && pip3 install --editable . && py.test -v
```

## Use

Encrypt some data using test API key:
```python
from secondguard import sg_hybrid_encrypt, sg_hybrid_decrypt

your_secret = b"attack at dawn!"

# Testing credentials (normally saved in your app's config):
API_TOKEN = 'SG-XXXX'
YOUR_PUBKEY = '''-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxY9sgHqrHRkfppnOJACr\nhwYxHP4d/OUUzbTiNFfcFoCyCUCL6dnLql1WPfaUyYWeLEQ4NTFI9Nfdy9tka6ZO\n75V3LCW5l2TMkbb0BvWnAcIK3lMY19kfFyImAoLvcZcAevi0ogkOn20zDrxVhlpv\nQAu3OMCQmc1aMgv6pp1FO4v3OjiXNp1AQQw8CIHnQzlLmGSMeUK1hdCcSGXq5qLA\nXrKwdkA8K6gDi67A43ZcWzew1KF8OwtA2WyLRfbzGaXqqq2pLNcrt90v64azkk+Q\nn8JTJym7k30Jv7zbhsGR08dvk6zn7TrNMn1TsIwflDFGSpzSCAQcz1gR+0GiwGvk\nqQkKeNhTAUHOdf7IONEpmZ+46O4uUmtAXu5lI0D5dPtl2M5ZtAjxRMvXX65QeNd7\nMwcoXy5LaUMnDVl8Sq8OL8dj8PMKiqO7m/yMuMfXgEd9EcdzFt80rRUCH3/H3+MT\nQMZdlbNASA5d//MOxERsb1ildEyfTQpSWvyeGIpCCtPmq3yJbKat95RTUX4uJPLi\nKFCifkVhirl+XxdDK6L0gly0kZEW41qyKZL+++5M6NalsBsMr5AFAUF0Ws4E+aWf\n6Zm8FDi6G4ZpAmVpP6bmqY+GoTFBQKXezICAwsJ6Dhy8UUHxDRQIiNTSLVnO5wgR\ncRfaU/jG6gorIFQvw8mw2hcCAwEAAQ==\n-----END PUBLIC KEY-----\n'''

# Save this in your DB (only local encryption happens here):
local_ciphertext, sg_recovery_instructions = sg_hybrid_encrypt(
    to_encrypt=your_secret,
    rsa_pubkey=YOUR_PUBKEY, 
    api_token=API_TOKEN,
)

# Recover using SecondGuard (asymmetric decryption takes place via API and then symmetric decryption takes place locally):
secret_recovered, rate_limit_info = sg_hybrid_decrypt( 
    local_ciphertext_to_decrypt=local_ciphertext, 
    sg_recovery_instructions=sg_recovery_instructions,
    api_token=API_TOKEN,
)

assert your_secret == secret_recovered
```

---

### Further Reading

Run tests to confim it's working (add a `-v` flag for more output):
```bash
$ py.test
=============================== test session starts ===============================
...
================================ 3 passed in 0.94s ================================

```

Update `requirements.txt`:
```bash
$ pip-compile requirements.in
```

Note that these INSECURE testing RSA keys were created with the following:
```bash
$ openssl genrsa -out insecureprivkey.pem 4096 && openssl rsa -in insecureprivkey.pem -pubout -out insecurepubkey.crt
```
