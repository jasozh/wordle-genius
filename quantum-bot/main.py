from wordle.quantum import GameState, Feedback
import random
import itertools
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

        # add number of turns
        self.total_turns_won = 0

        # possible_words is a set of words the bot is willing to guess
        self.possible_words = self.all_words()

        # half letters
        self.half_green = set()
        self.half_yellow = set()

        # combo of half letters that can be tried
        self.cantry = []

        self.tried = []

        self.full_found = False

        self.testing = []

        self.changed = False

    def play_game(self) -> GameState:
        """
        Non-interactively plays a game of Wordle and returns the finished game state
        """
        game = GameState()
        while (not game.is_finished()):
            guess = self.generate_word(game)
            game.attempt_guess(guess)

        # Add to games, update win rate, and reset possible words
        self.games.append(game)
        self.possible_words = self.all_words()
        self.half_green = set()
        self.half_yellow = set()
        self.cantry = []
        self.tried = []
        self.full_found = False
        self.testing.append("break")
        self.changed = False
        if game.win:
            
            self.win_rate += 1
            self.total_turns_won += game.turn
        return game

    def play_games(self, n: int) -> None:
        """
        Non-interactively plays n games of Wordle
        """
        for _ in range(n):
            self.play_game()

    def __repr__(self) -> str:
        """
        Returns a string representation of Bot
        """
        return (
            f"games: {self.games}\n"
            f"win rate: {self.win_rate}\n"
            f"number of possible words: {len(self.possible_words)}"
        )

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

    # def play_game(self) -> GameState:
    #     """
    #     Non-interactively plays a game of Wordle and returns the finished game state
    #     """
    #     game = GameState()
    #     while not game.is_finished():
    #         guess = self.generate_word(game)
    #         game.attempt_guess(guess)

    #     # Add to games, update win rate, and reset possible words
    #     self.games.append(game)
    #     self.possible_words = self.all_words()
    #     if game.win:
    #         self.win_rate += 1

    #     return game

    # def play_games(self, n: int) -> None:
    #     """
    #     Non-interactively plays n games of Wordle
    #     """
    #     for _ in range(n):
    #         self.play_game()
    #         self.testing.append("hello1")


    def __repr__(self) -> str:
        """
        Returns a string representation of Bot
        """
        return (
            f'games: {self.games}\n'
            f'win rate: {self.win_rate}\n'
            f'number of possible words: {len(self.possible_words)}'
        )

    # HELPER FUNCTIONS

    def all_words(self) -> set[str]:
        """
        All possible legal words to guess from
        """
        # word list found here: https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt
        # La words that can be guessed and which can be the word of the day
        # Ta words that can be guessed but are never selected as the word of the day

        # opening the file in read mode
        valid_word_list_file = open("public/wordle-La.txt", "r")
        invalid_word_list_file = open("public/wordle-Ta.txt", "r")

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
        super().__init__()

    def generate_word(self, game: GameState) -> str:
        # Randomly selects a possible word
        self.filter(game)
        self.half(game)
        return random.choice(list(self.possible_words))

    def filter(self, game: GameState) -> None:
        # Filters out the last guess since we can't guess it again
        if len(game.guesses) > 0:
            last_guess = "".join(game.guesses[-1])
            self.possible_words.remove(last_guess)

    def half(self, game: GameState) -> None:
        self.feedback


class QuantumBot(BotInterface):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        """
        Returns a string representation of Bot
        """
        if self.win_rate == 0:
            avg_turns = 0
        else:
            avg_turns = round(self.total_turns_won / self.win_rate, 2)
        return (
            # f"games: {self.games}\n"
            f'games: {self.games}\n'
            f"number of games: {len(self.games)}\n"
            f"win rate: {self.win_rate/len(self.games)}\n"
            # f"number of possible words: {len(self.possible_words)}\n"
            f"avg turns to win: {avg_turns}\n"
            f"testing: {self.testing}\n"
        )

    def generate_word(self, game: GameState) -> str:
        """
        This bot makes a random first guess, then it tries combinations of letters from 
        the information given, also filtering out the gray letters. If the combination is 
        completely colored, then we continue. Otherwise, we try a new combination.
        The algorithm is as follows:
        1.  Choose a random word for the first guess.
        2.  Filter out gray letters from the guess.
        3.  If the letters are completely filled, then continue with said letters (using 
        middle bot's strategy).
        4.  Else, then choose a combination of two letters to continue guessing with.
        4.  If there's no new information but it's still half, then try different 
        combination. Otherwise, try new word with same information.
        """
        # Randomly selects a possible word
        self.filter(game)
        if self.full_found or (len(self.half_green) == 0 and len(self.half_yellow) == 0):
            return random.choice(list(self.possible_words))
        else:
            if (self.changed == True and len(self.tried) > 0):
                self.cantry.append(self.tried[-1])
                self.tried.remove(self.tried[-1])
            permutations = list(itertools.combinations(self.half_green, 2))
            self.cantry.extend(permutations)
            # tempset = self.half_green.union(self.half_yellow)
            # permutations = list(itertools.combinations(tempset, 2))
            permutations = list(itertools.product(self.half_green,self.half_yellow))
            self.cantry.extend(permutations)
            permutations = list(itertools.combinations(self.half_yellow, 2))
            self.cantry.extend(permutations)
            # self.cantry = [i for n, i in enumerate(
            #     self.cantry) if i not in self.cantry[:n]]
            self.cantry = list(dict.fromkeys(self.cantry))
# Convert the permutations iterator to a list for easier printing
            # for i in range(len(self.half_green)):
            #     for j in range(i, len(self.half_green)):
            #         if (i != j):
            #             self.cantry.add((list(self.half_green)[i], list(self.half_green)[j]))
            # permut = itertools.permutations(
            #     self.half_green, len(self.half_yellow))
            # for comb in permut:
            #     zipped = zip(comb, self.half_yellow)
            #     self.cantry.add(zipped)
            # for i in range(len(self.half_yellow)):
            #     for j in range(i, len(self.half_yellow)):
            #         if (i != j):
            #             self.cantry.add((list(self.half_yellow)[
            #                             i], list(self.half_yellow)[j]))
            self.cantry = [a for a in self.cantry if a not in self.tried]
            # self.cantry = self.cantry - list(self.tried)
            if (len(self.cantry) == 0):
                return random.choice(list(self.possible_words))
            else:
                trying1, trying2 = self.cantry[-1]
                self.testing.append((trying1, trying2))
                self.tried.append((trying1, trying2))
                tempgreen = set()
                tempyellow_ind = set()
                tempyellow_let = set()

                if (trying1[0] == Feedback.HALFGREEN):
                    tempgreen.add((trying1[1], trying1[2]))
                else:
                    tempyellow_ind.add((trying1[1], trying1[2]))
                    tempyellow_let.add(trying1[2])
                if (trying2[0] == Feedback.HALFGREEN):
                    tempgreen.add((trying2[1], trying2[2]))
                else:
                    tempyellow_ind.add((trying2[1], trying2[2]))
                    tempyellow_let.add(trying2[2])

                # Check each word to see if it matches criteria
                words_to_remove = set()

                for word in self.possible_words:
                    letters = {x for x in list(word)}  # { 'a', 'b', ... }
                    letters_indices = {x for x in enumerate(
                        list(word))}  # { (index, letter), ... }

                    # Check to see that every green exists in letters
                    if not tempgreen.issubset(letters_indices):
                        words_to_remove.add(word)

                    # # Check that every yellow letter exists but not at the same index
                    # If any yellow letter not in word, remove word
                    if not tempyellow_let.issubset(letters):
                        words_to_remove.add(word)
                    if len(tempyellow_ind & letters_indices) > 0:
                        words_to_remove.add(word)


                # Remove all words to be removed
                temp = self.possible_words - words_to_remove

                if (len(temp) > 0):
                    return random.choice(list(temp))
                else:
                    return random.choice(list(self.possible_words))

    def filter(self, game: GameState) -> None:
        # Filter out all words that cannot possibly be the final word
        if len(game.guesses) > 0:
            guess, feedback = game.guesses[-1], game.feedback[-1]

            # Filter guess letters into green, yellow, gray
            green_indices = set()  # { (index, letter), ... }
            halfgreen_indices = set()  # { (index, letter), ... }

            yellow_letters = set()  # { 'a', 'b', ... }
            yellow_indices = set()  # { (index, letter), ... }
            halfyellow_letters = set()  # { 'a', 'b', ... }
            halfyellow_indices = set()  # { (index, letter), ... }

            gray_letters = set()  # { 'a', 'b', ... }

            length = len(halfyellow_indices) + len(halfgreen_indices)

            for i in range(len(guess)):
                letter = guess[i]
                if feedback[i] == Feedback.GREEN:
                    green_indices.add((i, letter))
                    self.full_found = True
                elif feedback[i] == Feedback.YELLOW:
                    yellow_letters.add(letter)
                    yellow_indices.add((i, letter))
                    self.full_found = True
                elif feedback[i] == Feedback.HALFGREEN:
                    halfgreen_indices.add((i, letter))
                    self.half_green.add((Feedback.HALFGREEN, i, letter))
                elif feedback[i] == Feedback.HALFYELLOW:
                    halfyellow_letters.add(letter)
                    halfyellow_indices.add((i, letter))
                    self.half_yellow.add((Feedback.HALFYELLOW, i, letter))
                else:
                    gray_letters.add(letter)

            if length == len(halfyellow_indices) + len(halfgreen_indices):
                self.changed = False
            else:
                self.changed = True
            # Check each word to see if it matches criteria
            words_to_remove = set()

            for word in self.possible_words:
                letters = {x for x in list(word)}  # { 'a', 'b', ... }
                letters_indices = {x for x in enumerate(
                    list(word))}  # { (index, letter), ... }

                # Check to see that every green exists in letters
                if not green_indices.issubset(letters_indices):
                    words_to_remove.add(word)

                # # Check that every yellow letter exists but not at the same index
                # If any yellow letter not in word, remove word
                if not yellow_letters.issubset(letters):
                    words_to_remove.add(word)
                # If any yellow letter is in the same index, remove word
                if len(yellow_indices & letters_indices) > 0:
                    words_to_remove.add(word)
                # If any yellow letter is in the same index, remove word
                if len(halfyellow_indices & letters_indices) > 0:
                    words_to_remove.add(word)

                # Check that none of the gray letters exist in the word
                if len(gray_letters & letters) > 0:  # If any gray letter is in word, remove word
                    words_to_remove.add(word)

            # Remove all words to be removed
            self.possible_words = self.possible_words - words_to_remove


if __name__ == "__main__":
    b = QuantumBot()
    b.play_games(10)
    print(b)
