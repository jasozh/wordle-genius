from enum import Enum
import random
from termcolor import cprint, colored


class Feedback(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2


class GameState:
    def __init__(self) -> None:
        """
        Initializes a new empty game state
        """
        # word is a list of chars for each letter in the actual word
        #
        # Example: [s, p, a, i, n]
        self.word = self.generate_word()

        # guesses has 6 rows, one for each guess. Each row is a list of chars
        # representing the letters in the guess.
        #
        # Example: [
        #     [s, t, a, i, r],
        #     [t, o, w, e, l],
        #     [p, l, a, c, e],
        #     [w, h, i, n, y]
        # ]
        self.guesses = []

        # feedback has 6 rows, one for each guess. Each row is a list of enums
        # representing the feedback for each letter in the guess. For example,
        #
        # Example: [
        #     [1, 0, 2, 0, 0]
        #     [0, 0, 2, 1, 0]
        #     [0, 0, 0, 0, 0]
        #     [1, 0, 2, 0, 1]
        # ]
        self.feedback = []

        # turn is what the current player turn is, from 0 to 5 (6 guesses)
        self.turn = 0

        # win is a boolean that describes whether the player has won the game
        self.win = False

    def generate_word(self) -> str:
        """
        Returns a new valid 5-letter Wordle word
        """
        # word list found here: https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt
        # La words that can be guessed and which can be the word of the day
        # Ta words that can be guessed but are never selected as the word of the day

        # opening the file in read mode
        word_list_file = open("../public/wordle-La.txt", "r")

        # reading the file
        data = word_list_file.read()

        # replacing end splitting the text
        # when newline ('\n') is seen.
        data_into_list = data.split("\n")

        word_list_file.close()
        return random.choice(data_into_list)

    def print_game_state(self) -> None:
        """
        Prints out the current state of the board, using ANSI terminals for
        feedback
        """
        for turn in range(len(self.guesses)):
            feedback = self.feedback[turn]
            guess = self.guesses[turn]
            for letter in range(len(guess)):
                if feedback[letter] == Feedback.YELLOW:
                    cprint(guess[letter], "yellow", end=" ")
                elif feedback[letter] == Feedback.GREEN:
                    cprint(guess[letter], "green", end=" ")
                else:
                    cprint(guess[letter], "white", end=" ")
            # for the new line
            print()

    def attempt_guess(self, guess: str) -> None:
        """
        Takes in a guess from the player, increments the turn, updates the game
        state, and updates the feedback
        """
        pass

    def is_finished(self) -> bool:
        """
        Returns whether the game is over or not
        """
        return self.turn > 5 or self.win

    def __repr__(self) -> str:
        """
        Returns a string representation of GameState
        """
        return (
            f'word: {self.word}\n'
            f'guesses: {self.guesses}\n'
            f'feedback: {self.feedback}\n'
            f'turn: {self.turn}\n'
            f'win: {self.win}'
        )


class Bot:
    def __init__(self) -> None:
        """
        Initializes a friendly AI bot to play Wordle!
        """
        pass

    def generate_word(self, game: GameState) -> str:
        """
        Generates the next guess based on the current game state
        """
        pass


def play_game(bot: Bot) -> GameState:
    """
    Non-interactively plays a game of Wordle and returns the finished game state
    """
    game = GameState()
    while not game.is_finished():
        guess = bot.generate_word(game)
        game.attempt_guess(guess)
    return game


def play():
    """
    Plays an interactive game of Wordle.
    """
    # Intro
    print("Welcome to Wordle!\n")
    game = GameState()

    # Play game
    while not game.is_finished():
        guess = input("What is your guess?\n")
        game.attempt_guess(guess)
        game.print_game_state()

    # End game
    print("Thanks for playing wordle!")
    if game.won:
        print("Congratulations! You won Wordle!")
    else:
        print("You lost. Better luck next time! Sad.")
