import sys

def test(_TOTEST):
    for _index, _testfun in enumerate(_TOTEST):
        fun, test_status, args = _testfun

        if test_status or test_status == 1:
            print(f"[!] Testing function: '{fun.__name__}'")

            if not args:
                fun()
            else:
                fun(*args)