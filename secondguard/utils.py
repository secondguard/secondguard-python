import requests

# Hack (make this somethign we can pass around?)
# BASE_URL = "http://localhost:1323/"
BASE_URL = "https://secondguard.uc.r.appspot.com/"

HEX_CHARS = set('0123456789abcdef')

# For testing only
# Limited to 1 INSECURE pubkey, rate-limiting shared across all users
TESTING_API_TOKEN = 'SG-XXXX'


with open('insecureprivkey.pem', 'r') as f:
    PRIVKEY_STR = f.read()
with open('insecurepubkey.crt', 'r') as f:
    PUBKEY_STR = f.read()


def _assert_hex(string):
    assert type(string) is str, string
    for char in string:
        assert char.lower() in HEX_CHARS, 'Char %s in %s NOT hex' % (char, string)

def _assert_valid_api_token(api_token):
    assert type(api_token) is str, api_token

    assert api_token.startswith('SG-'), api_token

def _assert_valid_pubkey(pubkey_str):
    assert type(pubkey_str) is str, pubkey_str
    assert pubkey_str.strip().startswith('-----BEGIN PUBLIC KEY-----'), pubkey_str
    assert pubkey_str.strip().endswith('-----END PUBLIC KEY-----'), pubkey_str

def _assert_valid_privkey(privkey_str):
    assert type(privkey_str) is str, privkey_str
    assert privkey_str.strip().startswith('-----BEGIN RSA PRIVATE KEY-----'), privkey_str
    assert privkey_str.strip().endswith('-----END RSA PRIVATE KEY-----'), privkey_str


def _fetch_testing_pubkey(url=BASE_URL + "static/pubkey.crt"):
    return requests.get(url).content.decode('utf-8')


def _write_bytes_to_file(some_bytes, filepath):
    print("Writing bytes to file %s ..." % filepath)
    with open(filepath, 'wb') as f:
        return f.write(some_bytes)
        
def _write_str_to_file(string, filepath):
    print("Writing string to file %s ..." % filepath)
    with open(filepath, 'w') as f:
        return f.write(string)
        

def assert_same(input1, input2):
    if input1 != input2:
        raise Exception("Have: %s\nWant: %s" % (input1, input2))
        
