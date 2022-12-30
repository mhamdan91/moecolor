import typing

NOTE = """  Some attributes may not be supported on all terminals.  
            If a specific attribute does not work, that means the 
            terminal you are using does not support it.
       """

# Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
# https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences
CSI = '\033['
CLEAR_SCREEN = CSI + '2J'
RESET = '\033[0m'
ATTRIBUTES = {
                'BOLD': 1, 'DIM': 2, 'ITALIC': 3, 'UNDERLINE': 4,
                'BLINK': 5, 'INVERT': 7, 'HIDE': 8, 'STRIKE': 9,
                'DOUBLE-UNDERLINE': 21, 'FOREGROUND': 38, 'BACKGROUND': 48, 
                'OVERLINED': 53, 'UNDERLINE-COLOR': 58
            }

DEFAULT_COLORS = {
                    'BLACK': 30, 'RED': 31, 'GREEN': 32, 'YELLOW': 33, 'BLUE': 34,
                    'MAGENTA': 35, 'CYAN': 36, 'BRIGHT_GRAY': 37, 'DEFAULT': 39,
                    'DARK_GRAY': 90, 'BRIGHT_RED': 91, 'BRIGHT_GREEN': 92, 'BRIGHT_YELLOW': 93,
                    'BRIGHT_BLUE': 94,'BRIGHT_MAGENTA': 95, 'BRIGHT_CYAN': 96, 'WHITE': 97, 'RESET': 0
                }

class Print:

    def __init__(self, text, color: typing.Any, attr: typing.Iterable=[], **kwargs) -> None:
        self.attr = attr
        self.color = color
        self.sanitize_attr()

    def build_string(self):
            pass 

    
    def build_color(self) -> str:
        self.validate_color()
        offset = 0
        if {'invert', 'background'}.intersection(ATTRIBUTES):
            offset = 10
        if isinstance(list, self.color) or isinstance(tuple, self.color):
            rgb = ';'.join(self.color)
            return self.build_code('38;2;' + rgb)
        else:
            return self.build_code(self.color + offset)

    def build_code(self, code):
        return CSI + str(code) + 'm'

    def validate_color(self) -> None:
        if isinstance(str, self.color):
            color = DEFAULT_COLORS.get(self.color.upper(), -1)
            if color == -1:
                raise ValueError(f'Expecting a color from {list(DEFAULT_COLORS.keys())}, but received {self.color}.')
            else:
                self.color = color
        elif isinstance(list, self.color) or isinstance(tuple, self.color):
            if len(self.color) != 3:
                raise ValueError(f'Expecting a tuple/list of RGB colors (R,G,B)/[R,G,B], but received {self.color}.')
            else:
                try:
                    self.color = [int(c) for c in self.color]
                except ValueError:
                    raise ValueError(f'Expecting a tuple/list integers, but received {self.color}.')
                else:
                    for c in self.color:
                        if c > 255 or c < 0:
                           raise ValueError(f'Expecting a tuple/list integers between [0, 255], but received {c}.') 
        else:
            raise TypeError(f'Expecting a tuple/list of RGB colors (R,G,B)/[R,G,B], but received {self.color}.')

    def sanitize_attr(self) -> None:
        for t in self.attr:
            t = str(t).lower()
            t = t.replace(' ', '-')
            if t in ['b', 'bold']:
                t = 'BOLD'
            elif t in ['dim', 'dark', 'd']:
                t = 'DIM'
            elif t in ['i', 'italic']:
                t = 'ITALIC'
            elif t in ['u', 'underline']:
                t = 'UNDERLINE'
            elif t in ['blink', 'blinking', 'flash']:
                t = 'BLINK'
            elif t in ['reverse', 'invert', 'switch']:
                t = 'INVERT'
            elif t in ['conceal', 'hide']:
                t = 'HIDE'
            elif t in ['crossed-out', 'cross-out', 'crossed-out', 'strike']:
                t = 'STRIKE'
            elif t in ['double-underline', '2u', 'uu']:
                t = 'DOUBLE-UNDERLINE'
            elif t in ['foreground', 'fg', 'fore-ground']:
                t = 'FOREGROUND'
            elif t in ['background' ,'bg', 'back-ground']:
                t = 'BACKGROUND'
            elif t in ['overlined', 'o', 'over-lined']:
                t = 'OVERLINED'
            elif t in ['underline-color', 'ucolor', 'u-color']:
                t = 'UNDERLINE-COLOR'
            else:
                pass
