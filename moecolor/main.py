import typing
# NOT USING F STRING TO MAKE THIS COMPATIBLE WITH MOST PYTHON VERSIONS...


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
                    'BRIGHT_BLUE': 94,'BRIGHT_MAGENTA': 95, 'BRIGHT_CYAN': 96, 'WHITE': 97, 'RESET': 0, 
                }

EXTRA_COLORS = {
                    'PURPLE': (160, 32, 240),
                    'VOILET': (127, 0, 255),
                    'LIME': (50, 205, 50),
                    'ORANGE': (255, 165, 0)
                }

class MoeColorError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

class InvalidColor(MoeColorError):
    """
    Raised when the color passed is invalid
    """

class FormatText:
    def __init__(self, text, color: typing.Any='DEFAULT', attr: typing.Iterable=[]) -> None:
        self.attr = attr
        self.color = color
        self.text = text
        self.format_text()

    def __str__(self) -> str:
        return self.text

    def format_text(self):
        self.sanitize_attr()
        self.build_string()

    def build_string(self):
        formatted_attrs = ''
        for t in self.attr:
            if t not in ATTRIBUTES:
                continue
            formatted_attrs += self.build_code(ATTRIBUTES[t])
        self.text = formatted_attrs + self.build_color() + self.text + RESET

    def build_color(self) -> str:
        self.validate_color()
        offset = 0
        if {'INVERT', 'BACKGROUND'}.intersection(set(self.attr)):
            offset = 10
        if isinstance(self.color, list) or isinstance(self.color, tuple):
            code = '5' if len(self.color) == 1 else '2'
            self.color = [str(c) for c in self.color]
            color = ';'.join(self.color)
            color_code = '58' if 'UNDERLINE-COLOR' in self.attr else str(38 + offset)
            self.color = color_code + ';' + code + ';' + color
        else:
            self.color = '58'  if 'UNDERLINE-COLOR' in self.attr else str(self.color + offset)
        for t in ['INVERT', 'BACKGROUND', 'UNDERLINE-COLOR']:
            try:
                self.attr.remove(t)
            except:
                pass
        return self.build_code(self.color)

    def build_code(self, code):
        return CSI + str(code) + 'm'

    def validate_color(self) -> None:
        if isinstance(self.color, str):
            color = DEFAULT_COLORS.get(self.color.upper(), -1)
            if color == -1:
                color = EXTRA_COLORS.get(self.color.upper(), -1)
                if color == -1:
                    raise InvalidColor('Expecting a color from ' + str(list(DEFAULT_COLORS.keys())) +
                                    ', but received [' + str(self.color) + ']. You can alternatively '+
                                    'provide RGB (R,G,B) value for a specific color.')
                else:
                    pass
            else:
                self.color = color
        elif isinstance(self.color, list) or isinstance(self.color, tuple):
            if len(self.color) != 3 and len(self.color) != 1:
                raise InvalidColor('Expecting a tuple/list of RGB colors (R,G,B)/[R,G,B] ' +
                                   'or an integer COLOR/[COLOR], but received ' + str(self.color) + '.')
            else:
                try:
                    self.color = [int(c) for c in self.color]
                except ValueError:
                    raise ValueError('Expecting a tuple/list integers, but received ' + str(self.color) + '.')
                else:
                    for c in self.color:
                        if c > 255 or c < 0:
                           raise InvalidColor('Expecting a tuple/list integers between [0, 255], but received [' + str(c) +'].')
        elif isinstance(self.color, int):
            if self.color > 255 or self.color < 0:
                raise InvalidColor('Expecting a tuple/list integers between [0, 255], but received [' + str(c) +'].')
            else:
                self.color = [self.color]
        else:
            raise InvalidColor('Expecting a color from ' + str(list(DEFAULT_COLORS.keys())) +
                               ' or a tuple/list of RGB colors (R,G,B)/[R,G,B] or an integer ' +
                               'COLOR/[COLOR], but received [' + str(self.color) + '].')

    def sanitize_attr(self) -> None:
        for i, t in enumerate(self.attr):
            attribute = str(t).lower()
            attribute = attribute.replace(' ', '-')
            if attribute in ['b', 'bold']:
                self.attr[i] = 'BOLD'
            elif attribute in ['dim', 'dark', 'd']:
                self.attr[i] = 'DIM'
            elif attribute in ['i', 'italic']:
                self.attr[i] = 'ITALIC'
            elif attribute in ['u', 'underline']:
                self.attr[i] = 'UNDERLINE'
            elif attribute in ['blink', 'blinking', 'flash']:
                self.attr[i] = 'BLINK'
            elif attribute in ['reverse', 'invert', 'switch']:
                self.attr[i] = 'INVERT'
            elif attribute in ['conceal', 'hide']:
                self.attr[i] = 'HIDE'
            elif attribute in ['crossed-out', 'cross-out', 'crossed-out', 'strike', 's']:
                self.attr[i] = 'STRIKE'
            elif attribute in ['double-underline', '2u', 'uu', 'du']:
                self.attr[i] = 'DOUBLE-UNDERLINE'
            elif attribute in ['foreground', 'fg', 'fore-ground']:
                self.attr[i] = 'FOREGROUND'
            elif attribute in ['background' ,'bg', 'back-ground']:
                self.attr[i] = 'BACKGROUND'
            elif attribute in ['overlined', 'o', 'over-lined']:
                self.attr[i] = 'OVERLINED'
            elif attribute in ['underline-color', 'ucolor', 'u-color', 'uc']:
                self.attr[i] = 'UNDERLINE-COLOR'
            else:
                pass

def Print(text, color: typing.Any='DEFAULT', attr: typing.Iterable=[], **kwargs):
    formatted_text = FormatText(text, color, attr=attr)
    print(formatted_text, **kwargs)

Print('my formatted text', color='orange', attr=[])
print('my base text', end='\n\n')

#''sada