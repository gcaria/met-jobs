bcolors = {
    "header": "\033[95m",
    "blue": "\033[34m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "warning": "\033[93m",
    "fail": "\033[91m",
    "endc": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}


def printc(string, color):
    print(f"{bcolors[color]}{string}{bcolors['endc']}")
