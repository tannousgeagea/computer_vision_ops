class bcolors:
    """ ANSI color codes """
    colors = {
        "header": '\033[95m',
        "okblue": '\033[94m',
        "okcyan": '\033[96m',
        "okgreen": '\033[92m',
        "warning": '\033[93m',
        "fail": '\033[91m',
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "brown": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "lightgray": "\033[0;37m",
        "darkgray": "\033[1;30m",
        "lightred": "\033[1;31m",
        "lightgreen": "\033[1;32m",
        "yellow": "\033[1;33m",
        "lightblue": "\033[1;34m",
        "lightpurple": "\033[1;35m",
        "lightcyan": "\033[1;36m",
        "lightwhite": "\033[1;37m",
        "bold": "\033[1m",
        "faint": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "negative": "\033[7m",
        "crossed": "\033[9m",
        "end": "\033[0m"
    }

    def __call__(self, text, color):
        color_code = self.colors.get(color.lower(), self.colors['end'])
        return f"{color_code}{text}{self.colors['end']}"