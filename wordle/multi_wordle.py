from wordle.main import *


class Multi_Wordle(GameState):
    def __init__(self, num_games=2, words=None):
        """
        Initial num_games number of games to be played simultaneously

        words: an optional list of pre-determined answers to this game
        """
        assert words is None or len(words) == num_games
        # keep track of number of games
        self.num_games = num_games

        # the list of games within multi-wordle
        self.games = []

        # the guesses that have been made
        self.guesses = []

        # the feedback for each game within Multi_Wordle
        self.feedback = []

        # the list of correct words
        if words is None:
            self.answers = []

            for idx in range(num_games):
                # for each game:
                # create a game state
                # generate a new answer word (cannot have been selected already)
                # add the new word to self.answers; add the new_game to self.games
                # add its feedback and guesses to the respective arrays
                new_game = GameState()
                new_game.word = self.generate_words(self.answers)
                self.answers.append(new_game.word)
                self.games.append(new_game)
                self.guesses.append(new_game.guesses)
                self.feedback.append(new_game.feedback)
        else:
            self.answers = words
            for idx in range(num_games):
                # for each game:
                # create a game state
                # generate a new answer word (cannot have been selected already)
                # add the new word to self.answers; add the new_game to self.games
                # add its feedback and guesses to the respective arrays
                new_game = GameState(self.answers[idx])
                self.games.append(new_game)
                self.guesses.append(new_game.guesses)
                self.feedback.append(new_game.feedback)

        # number of turns taken in this game
        self.xturn = 0

        # keep track of the number of games within multi_wordle that have been won
        self.wins = 0

        # have we won multi_wordle?
        self.win = self.wins == self.num_games

    def generate_words(self, cant_pick_these):
        """
        Generates a word according to GameState's function, with the caveat that
        there are words that cannot be picked (basically words already picked)
        """
        ret = super().generate_word()

        while ret in cant_pick_these:
            ret = super().generate_word()

        return ret

    def print_game_state(self):
        """
        Prints each game in the game_state of x_wordle
        """
        for idx in range(len((self.games))):
            print(f"Board for Wordle game {idx}:")
            self.games[idx].print_game_state()
            print()

    def attempt_guess(self, guess: str, max_turns):
        """
        Attempts guess as the guess for each game in the game state
        """
        win_count = 0
        for game in self.games:
            if game.is_finished(max_turns):
                # don't continue to play finished individual games
                if game.win:  # still need to increment the win count if already won
                    win_count += 1
                continue
            game.attempt_guess(guess)  # call parent method
            if game.win:  # increment the number of wins
                win_count += 1

        self.xturn += 1  # increment number of turns
        self.wins = win_count  # set the win count
        self.win = self.wins == self.num_games  # check if you've won Multi_Wordle

    def is_finished(self, max_turns=8) -> bool:
        """
        Returns whether the game is over or not. The game is over if the player
        wins or if the turn count exceeds max_turns. Default is 6 for regular
        Wordle games.
        """
        # Subtract 1 because self.xturn is 0-indexed
        return self.xturn > max_turns - 1 or self.wins == self.num_games

    def __repr__(self) -> str:
        """
        Returns a string representation of the game
        """
        ret = "turns: " + str(self.xturn) + "\n"

        for idx in range(len(self.games)):
            # add the word
            ret += f"{idx} game: word is {self.games[idx].word}\n"
            for i in range(len(self.games[idx].guesses)):
                ret += str(self.games[idx].guesses[i]) + "\n"
                ret += str(self.games[idx].feedback[i]) + "\n"
            ret += f"win? {self.games[idx].win}"
            ret += "\n\n"

        ret += "Wins: " + str(self.wins) + "\n"
        ret += "Win? " + str(self.win) + "\n"
        return ret


def play(game, max_turns=8, helper_bot=None):
    """
    Plays an interactive game of Multi_Wordle.
    """
    # Intro
    num = game.num_games
    print(f"Welcome to {num}-Wordle!\n")

    # Play game
    while not game.is_finished(max_turns=max_turns):
        if helper_bot:
            suggestion = helper_bot.generate_word(game)
            print(f"Your helper bot thinks you should guess {suggestion}!")
        guess = input("What is your guess?\n> ")
        game.attempt_guess(guess, max_turns)
        game.print_game_state()

    # End game
    print(f"Thanks for playing {num}-wordle!")
    if game.win:
        print(f"Congratulations! You won {num}-Wordle!")
    else:
        print("You lost. Better luck next time! Sad.")
        print("The words were:", game.answers)


if __name__ == "__main__":
    # dwordle = Multi_Wordle(num_games=2)
    # play(dwordle)

    qwordle = Multi_Wordle(num_games=2)
    play(qwordle, 10)
