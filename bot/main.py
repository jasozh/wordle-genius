from wordle.main import GameState, Feedback
import random
import string
from abc import ABC, abstractmethod


class BotInterface(ABC):
    def __init__(self) -> None:
        """
        Initializes a friendly AI bot to play Wordle!
        """
        # games is the list of all games that were played by the bot
        self.games = []

        # games_won is the number of games out of all games that the bot won
        self.games_won = 0

        # possible_words is a set of words the bot is willing to guess
        self.possible_words = self.all_words()

        # total_turns_won is the total number of turns played for games that the
        # bot won
        self.total_turns_won = 0

    def play_game(self, max_turns=6, word=None) -> GameState:
        """
        Non-interactively plays a game of Wordle and returns the finished game state
        """
        game = GameState(word=word)
        while not game.is_finished(max_turns):
            guess = self.generate_word(game)
            game.attempt_guess(guess)

        # Add to games, update win rate, and reset possible words
        self.games.append(game)

        # Accumulate average number of turns and recompute average
        if game.win:
            self.total_turns_won += game.turn + 1

        self.possible_words = self.all_words()

        if game.win:
            self.games_won += 1

        return game

    def play_games(self, n: int, max_turns=6, words=None) -> None:
        """
        Non-interactively plays n games of Wordle

        words: a list of words that will be the answers of each game
        """
        if words is not None:
            for i in range(n):
                # print("playing game with answer:", words[i])
                self.play_game(max_turns, word=words[i])
        else:
            for _ in range(n):
                self.play_game(max_turns)

    def __repr__(self) -> str:
        """
        Returns a string representation of Bot
        """
        return (
            # f"games: {self.games}\n"
            f"number of games: {len(self.games)}\n"
            f"win rate: {self.games_won/len(self.games)}\n"
            # f"number of possible words: {len(self.possible_words)}\n"
            f"avg turns to win: {round(self.total_turns_won / self.games_won, 2)}\n"
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

    def possible_words_tf(self) -> dict[str, int]:
        """
        Given current possible Wordle guesses, returns a tuple of (key, value) where
        key = letter and value = number of words with that letter. The list is
        sorted in order, with the most common letter appearing first.

        Example: tf = { "a": 5, "b": 3, ... }
        """
        alphabet = list(string.ascii_lowercase)
        result = {}
        for letter in alphabet:
            words_with_letter = {word for word in self.possible_words if letter in word}
            result[letter] = len(words_with_letter)

        return result

    def generate_word_with_tf(self) -> set[str]:
        """
        Looks at all words in self.possible_guesses and selects the next word
        to guess based on letter frequency. A word is chosen if it contains the
        most common letters.

        Letter frequency is calculated as follows. Suppose we have the word "stair"
        and the tf dictionary has the following:

        tf = {
            "s": 53,
            "t": 49,
            "a": 17,
            "i": 19,
            "r": 2
        }

        For all unique letters in the word, we sum up all the values, so "stair"
        has score 140. Higher scores are better.

        We make scores for every possible word and choose the word with the highest
        score.
        """
        possible_tf = self.possible_words_tf()
        scores = []  # ex: [ ("stair": 140), ... ]
        for word in self.possible_words:
            unique_letters = set(word)
            score = 0
            for letter in unique_letters:
                score += possible_tf[letter]
            scores.append((word, score))

        scores_sorted = sorted(scores, reverse=True, key=lambda x: x[1])
        # print(scores_sorted[:10])
        # print(scores_sorted[-10:])
        # print(scores_sorted[0])

        # Return word with top score
        return scores_sorted[0][0]


class DummyBot(BotInterface):
    def __init__(self) -> None:
        super().__init__()

    def generate_word(self, game: GameState) -> str:
        # Randomly selects a possible word
        self.filter(game)
        return random.choice(list(self.possible_words))

    def filter(self, game: GameState) -> None:
        # Filters out the last guess since we can't guess it again
        if len(game.guesses) > 0:
            last_guess = "".join(game.guesses[-1])
            self.possible_words.remove(last_guess)


class SimpleBot(BotInterface):
    def __init__(self) -> None:
        super().__init__()

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
        if len(self.possible_words) != 0 and game.turn != 5:
            # print(
            #     "length of possible words:",
            #     len(self.possible_words),
            #     "turn:",
            #     game.turn,
            # )
            next_guess = random.choice(list(self.possible_words))
            self.filter(next_guess)  # filter out the next guess
        else:
            # last turn or self.possible_words is empty
            possible_correct_words = self.potential_final_guesses(game)
            next_guess = random.choice(list(possible_correct_words))
        return next_guess

    def filter(self, next_guess: str) -> None:
        # Filter out all remaining words that contain letters used in previous guess
        words_to_remove = set()
        for letter in next_guess:
            for word in self.possible_words:
                # print(letter, word)
                if letter in word:
                    words_to_remove.add(word)

        self.possible_words -= words_to_remove

    def potential_final_guesses(self, game):
        """
        Makes guesses of words based on feedback from previous turns
        """
        full_set = self.all_words()
        feedback = game.feedback
        green_format = {}  # keys are letter positions & values are letter positions
        bad_letters = set()
        yellow_format = {}  # keys are letter pos & yellow letters that don't fit there
        yellow_letters = set()

        for word in range(len(game.guesses)):  # words that have been guessed
            # letter position in that word
            for idx in range(len(game.guesses[word])):
                letter = game.guesses[word][idx]
                if feedback[word][idx] == Feedback.GREEN:
                    green_format[idx] = letter  # add to green_format dict
                elif feedback[word][idx] == Feedback.GRAY:
                    # guess can't have letter in final guess
                    bad_letters.add(letter)
                else:  # letter is yellow
                    yellow_letters.add(letter)
                    if idx not in yellow_format.keys():
                        yellow_format[idx] = set(letter)
                    else:
                        yellow_format[idx].add(letter)

        words_to_remove = set()
        for word in full_set:
            letters_in_word = set(list(word))
            if len(letters_in_word & yellow_letters) != len(yellow_letters):
                # does not contain any of the yellow letters and yellow letters were foun
                words_to_remove.add(word)
            elif len(letters_in_word & bad_letters) != 0:
                # contains at least one bad letter
                words_to_remove.add(word)
            else:
                for idx in range(len(word)):
                    letter = word[idx]
                    # print(idx in green_format.keys() ^ idx in yellow_format.keys())
                    if letter in bad_letters:
                        break
                    if (
                        idx not in green_format.keys()
                        and idx not in yellow_format.keys()
                    ):
                        continue  # don't remove the word based on this
                    else:
                        if idx in green_format.keys():
                            # print("must be in green format dict")
                            if green_format[idx] != letter:
                                words_to_remove.add(word)
                                break
                        else:
                            # print("must be in yellow format dict")
                            if letter in yellow_format[idx]:
                                # print("in yellow")
                                words_to_remove.add(word)
                                break

        return full_set - words_to_remove


class MiddleBot(BotInterface):
    def __init__(self) -> None:
        super().__init__()

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
        self.filter(game)

        # print(
        #     "length of possible words:",
        #     len(self.possible_words),
        #     "turn:",
        #     game.turn,
        # )

        # return random.choice(list(self.possible_words))
        return self.generate_word_with_tf()

    def filter(self, game: GameState) -> None:
        # Filter out all words that cannot possibly be the final word
        if len(game.guesses) > 0:
            guess, feedback = game.guesses[-1], game.feedback[-1]

            # Filter guess letters into green, yellow, gray
            green_indices = set()  # { (index, letter), ... }

            yellow_letters = set()  # { 'a', 'b', ... }
            yellow_indices = set()  # { (index, letter), ... }

            gray_letters = set()  # { 'a', 'b', ... }

            for i in range(len(guess)):
                letter = guess[i]
                if feedback[i] == Feedback.GREEN:
                    green_indices.add((i, letter))
                elif feedback[i] == Feedback.YELLOW:
                    yellow_letters.add(letter)
                    yellow_indices.add((i, letter))
                else:
                    gray_letters.add(letter)

            # Check each word to see if it matches criteria
            words_to_remove = set()

            for word in self.possible_words:
                letters = {x for x in list(word)}  # { 'a', 'b', ... }
                letters_indices = {
                    x for x in enumerate(list(word))
                }  # { (index, letter), ... }

                # Check to see that every green exists in letters
                if not green_indices.issubset(letters_indices):
                    words_to_remove.add(word)

                # Check that every yellow letter exists but not at the same index
                # If any yellow letter not in word, remove word
                if not yellow_letters.issubset(letters):
                    words_to_remove.add(word)
                # If any yellow letter is in the same index, remove word
                elif len(yellow_indices & letters_indices) > 0:
                    words_to_remove.add(word)

                # Check that none of the gray letters exist in the word
                if (
                    len(gray_letters & letters) > 0
                ):  # If any gray letter is in word, remove word
                    words_to_remove.add(word)

            # Remove all words to be removed
            self.possible_words = self.possible_words - words_to_remove


class HardBot(BotInterface):
    # type: refers to 'aggregate' (green + yellow), 'pool', 'green'
    # metric: number related to the type
    # Ex 1: HardBot(type='aggregate', metric=3)
    #       this bot will switch to trying to Middle Bot's strategy as soon as
    #       3 yellow or green squares are revealed
    # Ex 2: HardBot(type='green', metric=2)
    #       this bot will switch to Middle bot's strategy as soon as 2 green
    #       green squares are revealed
    # Ex 3: HardBot(type='pool', metric=10):
    #       The bot will switch to Middle bot's strategy when, if applying
    #       middle bot's strategy, there are 10 or less possible final guesses
    def __init__(self, type: str, metric: int) -> None:
        super().__init__()
        self.type = type
        self.metric = metric
        self.num_green = 0
        self.num_yellow = 0
        self.metric_met = False

    def play_game(self, max_turns=6, word=None):
        # reset things
        self.metric_met = False
        self.num_green = 0
        self.num_yellow = 0
        # play the game
        super().play_game(max_turns, word)

    def generate_word(self, game: GameState) -> str:
        """
        Generates the next word based on the metric.
        """
        if game.turn == 0:  # first turn: pick a random word, then filter list
            next_guess = random.choice(list(self.possible_words))
            self.filter(next_guess)
            return next_guess

        if len(self.possible_words) == 0:  # no more possible words; use Middle's strat
            self.metric_met = True

        if not self.metric_met:
            # first count number of green and yellow
            # there are no overlaps since this only happens when employing
            # SimpleBot's strategy which only guesses words with disjoint sets of letters
            # don't need to loop through the entire feedback matrix every time
            prev_turn = game.turn - 1
            for j in range(len(game.feedback[prev_turn])):
                if game.feedback[prev_turn][j] == Feedback.GREEN:
                    self.num_green += 1
                elif game.feedback[prev_turn][j] == Feedback.YELLOW:
                    self.num_yellow += 1

            if self.type == "aggregate":
                if self.num_green + self.num_yellow >= self.metric:
                    self.metric_met = True
            elif self.type == "green":
                if self.num_green >= self.metric:
                    self.metric_met = True
            elif self.type == "yellow":
                if self.num_yellow >= self.metric:
                    self.metric_met = True
            else:
                possible_correct_words = self.potential_final_guesses(game)
                if len(possible_correct_words) <= self.metric:
                    self.metric_met = True

        if self.metric_met:
            possible_correct_words = self.potential_final_guesses(game)
            return random.choice(list(possible_correct_words))
        else:
            # already been filtered
            next_guess = random.choice(list(self.possible_words))
            self.filter(next_guess)
            return next_guess

    def potential_final_guesses(self, game):
        """
        Makes guesses of words based on feedback from previous turns
        """
        full_set = self.all_words()
        feedback = game.feedback
        green_format = {}  # keys are letter positions & values are letter positions
        bad_letters = set()
        yellow_format = {}  # keys are letter pos & yellow letters that don't fit there
        yellow_letters = set()

        for word in range(len(game.guesses)):  # words that have been guessed
            # letter position in that word
            for idx in range(len(game.guesses[word])):
                letter = game.guesses[word][idx]
                if feedback[word][idx] == Feedback.GREEN:
                    green_format[idx] = letter  # add to green_format dict
                elif feedback[word][idx] == Feedback.GRAY:
                    # guess can't have letter in final guess
                    bad_letters.add(letter)
                else:  # letter is yellow
                    yellow_letters.add(letter)
                    if idx not in yellow_format.keys():
                        yellow_format[idx] = set(letter)
                    else:
                        yellow_format[idx].add(letter)

        words_to_remove = set()
        for word in full_set:
            letters_in_word = set(list(word))
            if len(letters_in_word & yellow_letters) != len(yellow_letters):
                # does not contain any of the yellow letters and yellow letters were foun
                words_to_remove.add(word)
            elif len(letters_in_word & bad_letters) != 0:
                # contains at least one bad letter
                words_to_remove.add(word)
            else:
                for idx in range(len(word)):
                    letter = word[idx]
                    if letter in bad_letters:
                        break
                    if (
                        idx not in green_format.keys()
                        and idx not in yellow_format.keys()
                    ):
                        continue  # don't remove the word based on this
                    else:
                        if idx in green_format.keys():
                            if green_format[idx] != letter:
                                words_to_remove.add(word)
                                break
                        else:
                            if letter in yellow_format[idx]:
                                words_to_remove.add(word)
                                break

        return full_set - words_to_remove

    def filter(self, next_guess: str) -> None:
        """
        Filter out all remaining words that contain letters used in
        previous guess
        """
        # next_guess = str(game.guesses[game.turn - 1])
        words_to_remove = set()
        for letter in next_guess:
            for word in self.possible_words:
                if letter in word:
                    words_to_remove.add(word)

        self.possible_words -= words_to_remove


def generate_word(num_words) -> str:
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
    return random.choices(data_into_list, k=num_words)


if __name__ == "__main__":
    num_games = 10

    words = generate_word(num_games)
    hb = HardBot(type="green", metric=3)
    sb = SimpleBot()
    mb = MiddleBot()

    sb.play_games(num_games, words=words)
    mb.play_games(num_games, words=words)
    hb.play_games(num_games, words=words)

    print(sb)
    print(mb)
    print(hb)
