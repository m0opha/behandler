from colorama import Fore,Style, init

init(autoreset=True)

def pSuccess(text: str, no_salt=False):
    if no_salt:
        print(f"{Fore.GREEN}{Style.BRIGHT}{text}",end="")
        return
    
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}")

def pError(text: str, no_salt=False):
    if no_salt:
        print(f"{Fore.RED}{Style.BRIGHT}{text}",end="")
        return
    
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def pWarning(text: str, no_salt=False):
    
    if no_salt:
        print(f"{Fore.YELLOW}{Style.BRIGHT}{text}", end="")
        return
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}")