import random
import gspread
from google.oauth2.service_account import Credentials
from graphics.graphics import (hangman_title,
                               win_title,
                               lose_title,
                               draw_hangman,
                               Colors)


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


def get_random_word():
    """
    Retrieves a random word from the Google Sheets.

    Returns:
    str: A random word.

    Raises:
    gspread.exceptions.APIError: If an error occurs accessing
    Google Sheets API.

    Exception: For any other unexpected error.
    """

    try:
        hangman_sheet = GSPREAD_CLIENT.open('hangman_words').sheet1

        words = hangman_sheet.col_values(1)
        random_word = random.choice(words)

        return random_word

    except gspread.exceptions.APIError as e:
        print(f"Uh Oh! An error occurred accessing Google Sheets API: {e}")


def initialize_game(difficulty):
    """
    Initializes the Hangman game.

    Args:
    difficulty (str): The difficulty level (easy, medium, or hard).

    Returns:
    tuple: A tuple containing the random word, the initial guessed word,
    max attempts, and difficulty.
    """
    random_word = get_random_word()

    guessed_word = ['_'] * len(random_word)

    max_attempts = 0

    if difficulty == 'easy':
        max_attempts = 6
    elif difficulty == 'medium':
        max_attempts = 5
    elif difficulty == 'hard':
        max_attempts = 4

    return random_word, guessed_word, max_attempts, difficulty


def main_menu():
    """
    Displays the main menu options and returns the user's choice.

    Returns:
    str: The user's choice.
    """
    print(f"{Colors.CYAN}\nMenu:{Colors.NORMAL}")
    print(f"{Colors.GREEN}1. Play{Colors.NORMAL}")
    print(f"{Colors.ORANGE}2. Instructions{Colors.NORMAL}")
    print(f"{Colors.RED}3. Quit{Colors.NORMAL}")

    choice = input(f"{Colors.CYAN}Enter your choice ("
                   f"{Colors.GREEN}1{Colors.CYAN}/"
                   f"{Colors.ORANGE}2{Colors.CYAN}/"
                   f"{Colors.RED}3{Colors.CYAN}): {Colors.NORMAL}")
    return choice


def choose_difficulty():
    """
    Prompts the user to choose a difficulty level
    and returns the selected difficulty.

    Returns:
    str: The selected difficulty.
    """
    print(f"{Colors.CYAN}\nDifficulty Levels:")
    print(f"{Colors.GREEN}e - Easy{Colors.NORMAL}")
    print(f"{Colors.ORANGE}m - Medium{Colors.NORMAL}")
    print(f"{Colors.RED}h - Hard{Colors.NORMAL}")

    difficulty = input(f"{Colors.CYAN}Choose a difficulty ("
                       f"{Colors.GREEN}e{Colors.CYAN}/"
                       f"{Colors.ORANGE}m{Colors.CYAN}/"
                       f"{Colors.RED}h{Colors.CYAN}): {Colors.NORMAL}"
                       ).lower()

    if difficulty not in ['e', 'm', 'h']:
        print(f"{Colors.RED}Invalid difficulty level. "
              f"Please choose from e, m, or h{Colors.NORMAL}")
        return choose_difficulty()

    if difficulty == 'e':
        difficulty = 'easy'
    elif difficulty == 'm':
        difficulty = 'medium'
    else:
        difficulty = 'hard'

    return difficulty


def show_instructions():
    """
    Displays game instructions and waits for user to press Enter.
    """
    instructions = f"""{Colors.CYAN}
    **Hangman Game Instructions**

    Objective:
    Guess the hidden word before you run out of attempts.

    1. Difficulty Levels:
    - "e" for Easy (6 attempts).
    - "m" for Medium (5 attempts).
    - "h" for Hard (4 attempts).

    2. Guessing a Letter:
    - Enter a letter (a to z) and press Enter.
    - If the letter is in the word, it will be revealed.
    - If not, you lose a life.
    - If you guess the word before losing your lives, YOU WIN!
    - If you run out of lives, it's GAME OVER!

    3. Hints:
    - Type "hint" to get a hint; however, this costs a life.
    - A random unrevealed letter will be shown.
    - Use it wisely! You cannot use it on your last life!

    4. Enjoy the Game!{Colors.NORMAL}
    """

    print(instructions)
    input(f"{Colors.CYAN}Press {Colors.GREEN}Enter{Colors.CYAN} "
          f"to return to the main menu...{Colors.NORMAL}")


def hint(random_word, guessed_word, guessed_letters, hint_used,
         max_attempts, current_attempts):
    """
    Randomly selects an unguessed letter from the word to provide as a hint.
    If a hint is provided, the corresponding letter is revealed in the guessed
    word.

    A hint costs a life and can only be used if there is more than 1 letter
    remaining and if the hint hasn't been used before in the game.
    """
    if hint_used or max_attempts - current_attempts <= 1:
        print(f"{Colors.RED}Sorry, you can't use a hint right now."
              f"{Colors.NORMAL}")
        return False, max_attempts

    unguessed_letters = [i for i, letter in enumerate(guessed_word)
                         if letter == '_']
    hint_index = random.choice(unguessed_letters)
    hint_letter = random_word[hint_index]

    guessed_word[hint_index] = hint_letter
    guessed_letters.add(hint_letter)

    return guessed_word, max_attempts


def replay():
    """
    Asks the player if they want to play again, only allowing 'y' or 'n'.

    Returns True if the player wants to play again, False otherwise.
    """
    while True:
        replay_choice = input(f"{Colors.CYAN}Do you want to play again? "
                              f"({Colors.GREEN}y{Colors.CYAN}/"
                              f"{Colors.RED}n{Colors.CYAN}):{Colors.NORMAL} "
                              ).strip().lower()
        if replay_choice == 'y':
            return True
        elif replay_choice == 'n':
            return False
        else:
            print(f"{Colors.RED}Invalid choice. "
                  f"Please enter 'y' or 'n'.{Colors.NORMAL}")


def play_game(random_word, guessed_word, max_attempts, difficulty):
    """
    Plays a round of the game.

    Args:
    random_word (str): The word to guess.
    guessed_word (list): The word with guessed letters.
    max_attempts (int): The maximum number of attempts.
    difficulty (str): The difficulty level (easy, medium, or hard).

    Returns:
    bool: True if the game is won, otherwise False.

    """
    current_attempts = 0
    guessed_letters = set()
    hint_used = False

    while current_attempts < max_attempts:
        print(' '.join(guessed_word))
        print(f"{Colors.CYAN}Guessed Letters: "
              f"{' '.join(guessed_letters)}{Colors.NORMAL}")
        print(f"{Colors.CYAN}Lives Remaining:{Colors.RED} "
              f"{max_attempts - current_attempts}{Colors.NORMAL}")

        draw_hangman(current_attempts, difficulty)

        if max_attempts - current_attempts > 1:
            if not hint_used:
                guess = input(f"{Colors.CYAN}Enter a letter (or type 'hint' "
                              f"for a hint): {Colors.NORMAL}").lower()
            else:
                guess = input(f"{Colors.CYAN}Enter a letter: "
                              f"{Colors.NORMAL}").lower()
        else:
            guess = input(f"{Colors.CYAN}Enter a letter: "
                          f"{Colors.NORMAL}").lower()

        if guess == 'hint':
            hint_result, max_attempts = hint(random_word, guessed_word,
                                             guessed_letters, hint_used,
                                             max_attempts, current_attempts)
            if hint_result:
                hint_used = True
                current_attempts += 1
                guessed_word = hint_result

        else:
            if len(guess) != 1 or not guess.isalpha():
                print(f"{Colors.RED}Please enter a valid single letter."
                      f"{Colors.NORMAL}")
                continue

            if guess in guessed_letters:
                print(f"{Colors.RED}You already guessed that letter."
                      f"{Colors.NORMAL}")
                continue

            if guess in random_word:
                for i, letter in enumerate(random_word):
                    if letter == guess:
                        guessed_word[i] = guess
                print(f"{Colors.GREEN}Well done! You guessed a"
                      f" correct letter.{Colors.NORMAL}")
            else:
                current_attempts += 1
                print(Colors.RED + f"Incorrect guess! Attempts remaining: "
                      f"{max_attempts - current_attempts}" + Colors.NORMAL)

            guessed_letters.add(guess)

            if '_' not in guessed_word:
                win_title()
                print(Colors.GREEN + f"Congratulations! You guessed the word: "
                      f"{''.join(guessed_word)}" + Colors.NORMAL)
                replay_choice = replay()
                return replay_choice

    lose_title()
    print(Colors.RED + f"Sorry! The word was: {random_word}" + Colors.NORMAL)
    draw_hangman(current_attempts, difficulty)
    replay_choice = replay()
    return replay_choice


def main():
    """
    The main function that manages the execution of the Hangman game.
    """
    hangman_title()
    while True:
        choice = main_menu()

        if choice == '1':
            difficulty = choose_difficulty()
            play_again = True
            while play_again:
                (random_word,
                 guessed_word,
                 max_attempts,
                 difficulty) = initialize_game(difficulty)
                play_again = play_game(
                    random_word, guessed_word, max_attempts, difficulty)

        elif choice == '2':
            show_instructions()
        elif choice == '3':
            exit()
        else:
            print(f"{Colors.RED}Invalid choice. Please enter"
                  f" 1, 2, or 3.{Colors.NORMAL}")


if __name__ == "__main__":
    main()
