from wordle.main import GameState, Feedback
import random
from wordle.multi_wordle import Multi_Wordle
from abc import ABC, abstractmethod


class BotInterface(ABC):
    def __init__(self) -> None:
        """
        Initializes a friendly AI bot to play Multi-Wordle!
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

        # keeps track of which game to attempt to solve
        self.to_solve = 0  # start by trying to solve 0th game

    def play_game(self, max_turns=8, num_games=2) -> Multi_Wordle:
        """
        Non-interactively plays a game of Wordle and returns the finished game state
        """
        game = Multi_Wordle(num_games=num_games)
        while not game.is_finished(max_turns=max_turns):
            guess = self.generate_word(game)
            if guess is None:
                break
            game.attempt_guess(guess, max_turns)

        # Add to games, update win rate, and reset possible words
        self.games.append(game)

        # Accumulate average number of turns and recompute average
        if game.win:
            self.total_turns_won += game.xturn

        self.possible_words = self.all_words()
        self.to_solve = 0

        if game.win:
            self.games_won += 1
        return game

    def play_games(self, n: int, max_turns=8, num_games=2) -> None:
        """
        Non-interactively plays n games of Wordle
        """
        for i in range(n):
            print(f"Playing Multi_Wordle game number {i+1}")
            game = self.play_game(max_turns=max_turns, num_games=num_games)
            print(f"Turns: {game.xturn}")
            game.print_game_state()

    def __repr__(self) -> str:
        """
        Returns a string representation of Bot
        """
        if self.games_won == 0:
            avg_turns = 0
        else:
            avg_turns = round(self.total_turns_won / self.games_won, 2)
        return (
            # f"games: {self.games}\n"
            f"number of games: {len(self.games)}\n"
            f"win rate: {self.games_won/len(self.games)}\n"
            # f"number of possible words: {len(self.possible_words)}\n"
            f"avg turns to win: {avg_turns}\n"
        )

    @abstractmethod
    def generate_word(self, game: GameState) -> str:
        """
        Generates the next guess based on the current game state. This is an
        abstract class that should be overridden.
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

    def filter(self, game: Multi_Wordle) -> None:
        """
        Filters self.possible_words to become smaller based on the game state

        """
        # if no guesses have been made; do nothing
        if len(game.guesses) == 0:
            return None

        # get the guesses
        to_solve_guesses = game.guesses[self.to_solve]
        # get the feedback of the game you're trying to solve
        to_solve_feedback = game.feedback[self.to_solve]

        # start with a full set of words
        full_set = self.all_words()

        green_format = {}  # keys are letter positions & values are letter positions
        bad_letters = set()
        yellow_format = {}  # keys are letter pos & yellow letters that don't fit there
        yellow_letters = set()  # set of yellow letters

        for word in range(len(to_solve_guesses)):  # words that have been guessed
            # letter position in that word
            for idx in range(len(to_solve_guesses[word])):
                letter = to_solve_guesses[word][idx]
                # if the letter is green, add to green_format
                if to_solve_feedback[word][idx] == Feedback.GREEN:
                    green_format[idx] = letter  # add to green_format dict
                elif to_solve_feedback[word][idx] == Feedback.GRAY:
                    # guess can't have letter in final guess
                    bad_letters.add(letter)
                else:  # letter is yellow
                    yellow_letters.add(letter)  # add the yellow_letters
                    if idx not in yellow_format.keys():
                        yellow_format[idx] = set(letter)
                    else:
                        yellow_format[idx].add(letter)

        words_to_remove = set()
        for word in full_set:
            letters_in_word = set(list(word))
            if len(letters_in_word & yellow_letters) == 0 and len(yellow_letters) != 0:
                # does not contain any of the yellow letters and yellow letters were found
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
                        # print(idx in green_format.keys() ^ idx in yellow_format.keys())
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

        self.possible_words = full_set - words_to_remove


class NaiveBot(BotInterface):

    def __init__(self):
        """
        NaiveBot specifically targets one game at a time in order; it does not care about
        the other games occuring and does not attempt to solve them until they've solved
        all previous games.
        In other words, NaiveBot does not aim to solve the 'closest to finished' game;
        instead always goes in order
        """
        super().__init__()

    def generate_word(self, game: Multi_Wordle) -> str:
        if game.wins != self.to_solve:
            self.to_solve += 1
            self.possible_words = self.all_words()
            if game.wins == game.num_games:
                return None
        self.filter(game)
        return random.choice(list(self.possible_words))


class GreedyBot(BotInterface):

    def __init__(self):
        """
        GreedyBot scores each wordle game within Multi_Wordle, and greedily solves.
        Scores are based on the feedback (according to Enum values)
        """
        super().__init__()
        self.scores = []

    def play_game(self, max_turns=8, num_games=2) -> Multi_Wordle:
        """
        Non-interactively plays a game of Wordle and returns the finished game state
        """
        game = Multi_Wordle(num_games=num_games)
        self.scores = [0] * num_games
        while not game.is_finished(max_turns=max_turns):
            guess = self.generate_word(game)
            if guess is None:
                break
            game.attempt_guess(guess, max_turns)

        # Add to games, update win rate, and reset possible words
        self.games.append(game)

        # Accumulate average number of turns and recompute average
        if game.win:
            self.total_turns_won += game.xturn

        self.possible_words = self.all_words()
        self.to_solve = 0

        if game.win:
            self.games_won += 1
        return game

    def generate_word(self, game: Multi_Wordle) -> str:
        self.update_scores(game)
        max_idx = self.min_score_idx()
        for idx in range(len(self.scores)):
            if self.scores[idx] > self.scores[max_idx] and not game.games[idx].win:
                max_idx = idx
        self.to_solve = max_idx  # solve the game with highest score
        self.possible_words = self.all_words()  # always reset possible_words
        if game.wins == game.num_games:
            return None

        self.filter(game)
        return random.choice(list(self.possible_words))

    def min_score_idx(self):
        """
        argmin but without using numpy
        """
        min_idx = 0
        for idx in range(len(self.scores)):
            if self.scores[min_idx] > self.scores[idx]:
                min_idx = idx
        return min_idx

    def update_scores(self, game: Multi_Wordle) -> None:
        """
        updates self.scores to reflect the scores of each game
        """
        # if no guesses have been made; do nothing
        if len(game.guesses[0]) == 0:
            return None

        for idx in range(game.num_games):
            if self.scores[idx] == 10:  # game was solved (and stopped being played)
                continue
            feedback = game.feedback[idx][game.xturn - 1]
            score = 0
            for val in feedback:
                if val == Feedback.GREEN:
                    score += 2
                elif val == Feedback.YELLOW:
                    score += 1
            self.scores[idx] = max(score, self.scores[idx])


if __name__ == "__main__":
    nb = NaiveBot()
    nb.play_games(5, max_turns=20, num_games=4)

    gb = GreedyBot()
    gb.play_games(5, max_turns=20, num_games=4)

    print("NaiveBot:")
    print(nb)
    print("GreedyBot:")
    print(gb)
