import requests

# Hack (make this somethign we can pass around?)
# BASE_URL = "http://localhost:1323/"
BASE_URL = "https://secondguard.uc.r.appspot.com/"

HEX_CHARS = set('0123456789abcdef')


def _assert_hex(string):
    assert type(string) is str, string
    for char in string:
        assert char.lower() in HEX_CHARS, 'Char %s in %s NOT hex' % (char, string)

def _assert_valid_api_token(api_token):
    assert type(api_token) is str, api_token

    assert api_token.startswith('SG-'), api_token


def _fetch_testing_pubkey(url=BASE_URL + "static/pubkey.crt"):
    return requests.get(url).content


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
        
