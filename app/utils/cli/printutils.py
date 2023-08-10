import colorama
from .styles import PRINT_STYLES


def reset_styles():
    """Resets console output style"""

    print(colorama.Style.RESET_ALL, sep='', end='')


def colorize(color=colorama.Fore.WHITE, bg_color=''):
    """Colorizes console output"""

    print(color, bg_color, sep='', end='')


def print_colored(*values, sep=' ', end='\n', color=colorama.Fore.WHITE, bg_color=''):
    """Prints colored output"""

    colorize(color=color, bg_color=bg_color)
    print(*values, sep=sep, end=end)
    reset_styles()


def print_prefixed(prefix, *values, sep=' ', end='\n'):
    """Prints prefix and values. Needed for print_pos, print_neg, ..."""

    print(f'{prefix} ', sep='', end='')
    print(*values, sep=sep, end=end)


def print_pos(*values, sep=' ', end='\n'):
    """Prints positive info with prefix [+]"""

    colorize(color=PRINT_STYLES['positive'])
    print_prefixed('[+]', *values, sep=sep, end=end)
    reset_styles()


def print_neg(*values, sep=' ', end='\n'):
    """Prints negative info with prefix [-]"""

    colorize(color=PRINT_STYLES['negative'])
    print_prefixed('[-]', *values, sep=sep, end=end)
    reset_styles()


def print_question(*values, sep=' ', end='\n'):
    """Prints question with prefix [?]"""

    colorize(color=PRINT_STYLES['question'])
    print_prefixed('[?]', *values, sep=sep, end=end)
    reset_styles()
