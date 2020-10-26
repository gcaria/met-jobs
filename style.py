from colorama import init
from colorama import Fore as f
init(autoreset=True)

dict_color = {
    'red': f.RED,
    'blue': f.BLUE,
    'green': f.GREEN,
    'yellow': f.YELLOW,
    'magenta': f.MAGENTA,
    'cyan': f.CYAN
}


def printc(text, color='red', end='\n'):
    print(dict_color[color] + str(text), end=end)

