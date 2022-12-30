class Colors:
    # https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit
    ESC = "\033["
    RESET = f"{ESC}0m"
    RED   = f"{ESC}1m{ESC}38;2;255;0;0m"
    GREEN = f"{ESC}1m{ESC}38;2;0;255;0m"
    BLUE  = f"{ESC}1m{ESC}38;2;0;0;255m"
    START_RGB = f"{ESC}1m{ESC}38;2;"

print(f'{Colors.ESC}3mMoving{Colors.RESET}')