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

Update `requirements.txt`:
```bash
$ pip-compile requirements.in
```

Note that these INSECURE testing RSA keys were created with the following:
```bash
$ openssl genrsa -out localprivkey.pem 4096 && openssl rsa -in localprivkey.pem -pubout -out localpubkey.crt
```
