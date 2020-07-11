from secondguard.utils import dsha256


def test_dsha256():
    assert dsha256("5e20d2c1e3495a01ca909ba228c171430819f88b764f6f93e0155e8dff79b135".encode()) == '249e5217c427f30994085779c8f2ed370e8d374edfc9e54407e215b7a8107303'
    assert dsha256("hello".encode()) == 'd7914fe546b684688bb95f4f888a92dfc680603a75f23eb823658031fff766d9'
    
