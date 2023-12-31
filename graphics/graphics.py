"""
Graphics for Hangman Game
"""


class Colors:
    """
    Provides ANSI escape codes for colored output.

    Attributes:
        CYAN (str): ANSI escape code for cyan color.
        RED (str): ANSI escape code for red color.
        GREEN (str): ANSI escape code for green color.
        ORANGE (str): ANSI escape code for orange color.
        NORMAL (str): ANSI escape code to reset color to default.
    """
    CYAN = '\033[96m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    ORANGE = '\033[1;33m'
    NORMAL = '\033[0m'


HANGMAN_GRAPHICS = [
        f"""{Colors.CYAN}
         ------
         |    |
              |
              |
              |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.CYAN}
         ------
         |    |
         O    |
              |
              |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.CYAN}
         ------
         |    |
         O    |
         |    |
              |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.CYAN}
         ------
         |    |
         O    |
        /|    |
              |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.CYAN}
         ------
         |    |
         O    |
        /|\\   |
              |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.ORANGE}
         ------
         |    |
         O    |
        /|\\   |
        /     |
              |
        {Colors.NORMAL}
        """,
        f"""{Colors.RED}
         ------
         |    |
         O    |
        /|\\   |
        / \\   |
              |
        {Colors.NORMAL}
        """
    ]


def hangman_title():
    """
    Title on main menu
    """
    print(f"""{Colors.ORANGE}
██   ██  █████  ███    ██  ██████  ███    ███  █████  ███    ██
██   ██ ██   ██ ████   ██ ██       ████  ████ ██   ██ ████   ██
███████ ███████ ██ ██  ██ ██   ███ ██ ████ ██ ███████ ██ ██  ██
██   ██ ██   ██ ██  ██ ██ ██    ██ ██  ██  ██ ██   ██ ██  ██ ██
██   ██ ██   ██ ██   ████  ██████  ██      ██ ██   ██ ██   ████
 {Colors.NORMAL}""")


def win_title():
    """
    Title on win screen
    """
    print(f"""{Colors.GREEN}
██     ██ ███████ ██      ██          ██████   ██████  ███    ██ ███████ ██
██     ██ ██      ██      ██          ██   ██ ██    ██ ████   ██ ██      ██
██  █  ██ █████   ██      ██          ██   ██ ██    ██ ██ ██  ██ █████   ██
██ ███ ██ ██      ██      ██          ██   ██ ██    ██ ██  ██ ██ ██
 ███ ███  ███████ ███████ ███████     ██████   ██████  ██   ████ ███████ ██

    ██    ██  ██████  ██    ██     ██████  ██ ██████      ██ ████████
     ██  ██  ██    ██ ██    ██     ██   ██ ██ ██   ██     ██    ██
      ████   ██    ██ ██    ██     ██   ██ ██ ██   ██     ██    ██
       ██    ██    ██ ██    ██     ██   ██ ██ ██   ██     ██    ██
       ██     ██████   ██████      ██████  ██ ██████      ██    ██
 {Colors.NORMAL}""")


def lose_title():
    """
    Title on lose screen
    """
    print(f"""{Colors.RED}
 ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████
██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██
██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████
██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██
 ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██
 {Colors.NORMAL}""")


def draw_hangman(attempts, difficulty):
    """
    Draws the hangman graphic based on the difficulty level.

    Args:
        attempts (int): The current number of attempts.
        difficulty (str): The difficulty level (easy, medium, or hard).
    """
    if difficulty == 'medium':
        print(HANGMAN_GRAPHICS[1 + attempts])
    elif difficulty == 'hard':
        print(HANGMAN_GRAPHICS[2 + attempts])
    else:
        print(HANGMAN_GRAPHICS[attempts])
