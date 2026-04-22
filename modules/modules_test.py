import io
import contextlib
import sys

from vars.test_vars import _TEST, _TEST_SPACE

from modules.utils import execute, datatodict, printSuccess, printError
from modules.verify_bluetoothctl import verify_bluetoothctl, data_bluetoothctl


#execute strings
from vars.test_vars import execute_test_string

#datatodict strings
from vars.test_vars import datatodict_test_string

#printSuccess
from vars.test_vars import printSuccess_test_string


def test(_TOTEST):
    print("[!] Testing functions")

    results = {}

    for _index, _testfun in enumerate(_TOTEST):
        
        fun, test_status, print_return, args = _testfun
        
        if test_status or test_status == 1:
            print(f"{_TEST_SPACE[:4]}[{_index}] -> '{fun.__name__}'")

            buffer = io.StringIO()

            try:
                # 👇 silenciar prints
                with contextlib.redirect_stdout(buffer):
                    if isinstance(args, dict):
                        result = fun(**args)
                    elif isinstance(args, tuple):
                        result = fun(*args)
                    else:
                        result = fun()

                # 👇 si quieres ver el retorno
                if print_return:
                    print(_TEST_SPACE, result)

                printSuccess(f"{_TEST_SPACE} [+] PASS")

                results[fun.__name__] = {
                    "status": True,
                    "result": result,
                    "output": buffer.getvalue()  # 👈 lo que imprimió la función
                }

            except Exception as e:
                output = buffer.getvalue()

                printError(f"{_TEST_SPACE} [-] FAIL")
                print(_TEST_SPACE, f"[!] {type(e).__name__}: {e}")

                # opcional: mostrar lo que imprimió antes de fallar
                if output:
                    print(_TEST_SPACE, "[DEBUG OUTPUT]:")
                    print(output)

                results[fun.__name__] = {
                    "status": False,
                    "error": str(e),
                    "output": output
                }

        else:
            results[fun.__name__] = None

    return results

_TOTEST = [
    # fun                 test_status       print_return        args
    [execute,             1,                True,               {"cmd":execute_test_string, "return_output" : True}],
    [datatodict,          1,                False,              {"data" : datatodict_test_string}], 
    [verify_bluetoothctl, 1,                False,               {}],
    [data_bluetoothctl,   1,                False,               {}],
    [printSuccess,        1,                False,              {"text":printSuccess_test_string}],
]


if __name__ == "__main__":
    if _TEST:
        print("###########################################")
        print("#           TESTING.........")
        print("###########################################")

        status_funs = test(_TOTEST)