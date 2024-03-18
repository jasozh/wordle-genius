from wordle.main import GameState, Feedback
import random
from abc import ABC, abstractmethod


class BotInterface(ABC):
    def __init__(self) -> None:
        """
        Initializes a friendly AI bot to play Wordle!
        """
        # games is the list of all games that were played by the bot
        self.games = []

        # win_rate is the number of games out of all games that the bot won
        self.win_rate = 0

        # possible_words is a set of words the bot is willing to guess
        self.possible_words = self.all_words()

    def play_game(self) -> GameState:
        """
        Non-interactively plays a game of Wordle and returns the finished game state
        """
        game = GameState()
        while not game.is_finished():
            guess = self.generate_word(game)
            game.attempt_guess(guess)
        return game

    @abstractmethod
    def generate_word(self, game: GameState) -> str:
        """
        Generates the next guess based on the current game state. This is an
        abstract class that should be overridden.
        """
        pass

    @abstractmethod
    def filter(self, game: GameState) -> None:
        """
        Filters self.possible_words to become smaller based on the game state
        and the most recent guess (not any earlier guesses)
        """
        pass

    # HELPER FUNCTIONS

    def all_words(self) -> set[str]:
        """
        All possible legal words to guess from
        """
        # word list found here: https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt
        # La words that can be guessed and which can be the word of the day
        # Ta words that can be guessed but are never selected as the word of the day

        # opening the file in read mode
        valid_word_list_file = open("../public/wordle-La.txt", "r")
        invalid_word_list_file = open("../public/wordle-Ta.txt", "r")

        # reading the file
        valid_data = valid_word_list_file.read()
        invalid_data = invalid_word_list_file.read()

        # replacing end splitting the text
        # when newline ('\n') is seen.
        data_into_list = valid_data.split("\n") + invalid_data.split("\n")

        valid_word_list_file.close()
        invalid_word_list_file.close()
        return set(data_into_list)


class DummyBot(BotInterface):
    def __init__(self) -> None:
        super.__init__()

    def generate_word(self, game: GameState) -> str:
        # Randomly selects a possible word
        return random.choice(self.possible_words)

    def filter(self, game: GameState) -> None:
        # Filters out the last guess since we can't guess it again
        last_guess = str(game.guesses[game.turn])
        self.possible_words.remove(last_guess)


class SimpleBot(BotInterface):
    def __init__(self) -> None:
        super.__init__()

    def generate_word(self, game: GameState) -> str:
        """
        Our simplest bot would always guess words with letters it hadn't tried
        before until the last guess, or it cannot guess any more totally
        unique-lettered words. Then, it would piece together the information it
        had received to make a final guess.

        The algorithm is as follows:
        1.  Choose a random word for the first guess.
        2.  Filter out all remaining words that contain letters used in guess 1.
        3.  Guess with the remaining options. Repeat until we have to stop.
        4.  Make a guess where green letters stay, and we mix around yellow letters.
        """
        # Randomly selects a possible word
        while self.possible_words != [] and game.turn != 5:
            return random.choice(self.possible_words)

        # last turn or self.possible_words is empty
        possible_correct_words = self.potential_final_guesses(game)
        return random.choice(possible_correct_words)

    def filter(self, game: GameState) -> None:
        # Filter out all remaining words that contain letters used in previous guess
        guess = game.guesses[game.turn]  # list of letters
        feedback = game.feedback[game.turn]  # list of enums
        for letter in guess:
            for word in self.possible_words:
                if letter in word:
                    self.possible_words.remove(word)

    def potential_final_guesses(self, game):
        """
        Makes guesses of words based on feedback from previous turns
        """
        full_list = self.all_words()
        feedback = game.feedback
        guess_format = {}

        for word in range(len(game.guesses)):
            for letter in range(len(word)):
                if guess_format[letter] in guess_format.keys():
                    # already have a green letter there
                    continue
                else:
                    if feedback[word][letter] == Feedback.GREEN:
                        guess_format[letter] = game.guesses[word][
                            letter
                        ]  # set position of guess format to that letter
                    elif feedback[word][letter] == Feedback.YELLOW:
                        # guess is yellow
                        pass


class MiddleBot(BotInterface):
    def __init__(self) -> None:
        super.__init__()

    def generate_word(self, game: GameState) -> str:
        """
        Our middle bot would filter out impossible words based off of the game's
        feedback.

        The algorithm is as follows:
        1.  Choose a random word for the first guess. Suppose we guess "stare"
            and "r" and "e" are both yellow.
        2.  For the next word, guess a word that has to have "r" and "e" and that
            are not in the positions they were in guess 1. Each guess, we use the
            information we know to make the best possible guess on what the word
            could be.
        3.  Repeat this until we win or lose.
        """
        # Randomly selects a possible word
        return random.choice(self.possible_words)

    def filter(self, game: GameState) -> None:
        # Filter out all words that cannot possibly be the final word
        pass
