from enum import Enum
import random
from termcolor import cprint, colored
import numpy as np


class Feedback(Enum):
    GRAY = 0
    HALFYELLOW = 1
    YELLOW = 2
    HALFGREEN = 3
    GREEN = 4


class GameState:
    def __init__(self) -> None:
        """
        Initializes a new empty game state
        """
        # word is a string, generated from a list
        self.word1 = self.generate_word()
        self.word2 = self.generate_second_word()

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
        word_list_file = open("public/wordle-La.txt", "r")

        # reading the file
        data = word_list_file.read()

        # replacing end splitting the text
        # when newline ('\n') is seen.
        data_into_list = data.split("\n")

        word_list_file.close()
        return random.choice(data_into_list)

    def generate_second_word(self) -> str:
        """
        Returns a new valid 5-letter Wordle word, without letters used in the first generated word
        """
        # word list found here: https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt
        # La words that can be guessed and which can be the word of the day
        # Ta words that can be guessed but are never selected as the word of the day

        # opening the file in read mode
        word_list_file = open("public/wordle-La.txt", "r")

        # reading the file
        data = word_list_file.read()

        # replacing end splitting the text
        # when newline ('\n') is seen.
        data_into_list = data.split("\n")

        word_list_file.close()
        chosen_word = ""
        not_found = True
        while (not_found):
            chosen_word = random.choice(data_into_list)
            not_found = not set(self.word1).isdisjoint(chosen_word)
        return chosen_word

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
                elif feedback[letter] == Feedback.HALFYELLOW:
                    cprint(guess[letter], "black", "on_yellow", end=" ")
                elif feedback[letter] == Feedback.GREEN:
                    cprint(guess[letter], "green", end=" ")
                elif feedback[letter] == Feedback.HALFGREEN:
                    cprint(guess[letter], "black", "on_green", end=" ")
                else:
                    cprint(guess[letter], "white", end=" ")
            # for the new line
            print()

    def attempt_guess(self, guess: str) -> None:
        """
        Takes in a guess from the player, increments the turn, updates the game
        state, and updates the feedback
        """

        guesses_temp = [0 for i in range(5)]
        feedback_temp = [Feedback.GRAY] * 5

        index = 0
        foundinone = False
        foundintwo = False
        for l in guess:
            guesses_temp[index] = l
            if l in self.word1:
                if l == self.word1[index]:
                    feedback_temp[index] = Feedback.GREEN
                    foundinone = True
                else:
                    feedback_temp[index] = Feedback.YELLOW
                    foundinone = True
            if l in self.word2:
                if l == self.word2[index]:
                    feedback_temp[index] = Feedback.GREEN
                    foundintwo = True
                else:
                    feedback_temp[index] = Feedback.YELLOW
                    foundintwo = True
            index += 1
        if foundinone and foundintwo:
            for l in range(len(feedback_temp)):
                if feedback_temp[l] == Feedback.GREEN:
                    feedback_temp[l] = Feedback.HALFGREEN
                elif feedback_temp[l] == Feedback.YELLOW:
                    feedback_temp[l] = Feedback.HALFYELLOW
        self.guesses.append(guesses_temp)
        self.feedback.append(feedback_temp)
        self.turn += 1
        if guess == self.word1 or guess == self.word2:
            self.win = True

    def is_finished(self) -> bool:
        """
        Returns whether the game is over or not
        """
        return self.win

    def __repr__(self) -> str:
        """
        Returns a string representation of GameState
        """
        return (
            f'word1: {self.word1}\n'
            f'word2: {self.word2}\n'
            f'guesses: {self.guesses}\n'
            f'feedback: {self.feedback}\n'
            f'turn: {self.turn}\n'
            f'win: {self.win}'
        )


def play(helper_bot=None):
    """
    Plays an interactive game of Wordle.
    """
    # Intro
    print("Welcome to Quantum Wordle!\n")
    game = GameState()

    # Play game
    while not game.is_finished():
        if helper_bot:
            suggestion = helper_bot.generate_word(game)
            print(f"Your helper bot thinks you should guess {suggestion}!")
        guess = input("What is your guess?\n> ")
        game.attempt_guess(guess)
        game.print_game_state()

    # End game
    print("Thanks for playing wordle!")
    if game.win:
        print("Congratulations! You won Wordle!")
    else:
        print("You lost. Better luck next time! Sad.")
