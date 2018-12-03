from colorama import Fore, Style

def color_str(s, color):
    return '{}{}{}'.format(
        Fore.__dict__[color.upper()],
        s,
        Style.RESET_ALL,
    )


plus=color_str('[+]', 'green')
star=color_str('[*]', 'yellow')
minus=color_str('[-]','red')
