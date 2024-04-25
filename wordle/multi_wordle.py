from wordle.main import *


class Multi_Wordle(GameState):
    def __init__(self, num_games=2):
        """
        Initial num_games number of games to be played simultaneously
        """
        self.num_games = num_games
        self.games = []
        self.guesses = []
        self.feedback = []
        self.answers = []

        # self.answers = ["hello", "world", "robot", "bossy"]
        for idx in range(num_games):
            new_game = GameState()
            new_game.word = self.generate_words(self.answers)
            # new_game.word = self.answers[idx]
            self.answers.append(new_game.word)
            self.games.append(new_game)
            self.guesses.append(new_game.guesses)
            self.feedback.append(new_game.feedback)

        self.xturn = 0
        self.wins = 0
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
            print(f"Board for game {idx}:")
            self.games[idx].print_game_state()
            print("\n")

    def attempt_guess(self, guess: str):
        """
        Attempts guess as the guess for each game in the game state
        """
        win_count = 0
        for game in self.games:
            if game.is_finished():
                if game.win:  # still need to increment the win count if already won
                    win_count += 1
                continue
            game.attempt_guess(guess)
            if game.win:  # increment the number of wins
                win_count += 1
        self.xturn += 1  # increment number of turns
        self.wins = win_count
        self.win = self.wins == self.num_games

    def is_finished(self, max_turns=8) -> bool:
        """
        Returns whether the game is over or not. The game is over if the player
        wins or if the turn count exceeds max_turns. Default is 6 for regular
        Wordle games.
        """
        # Subtract 1 because self.turn is 0-indexed
        return self.xturn > max_turns - 1 or self.wins == self.num_games

    def __repr__(self) -> str:
        """
        Returns a string representation of the game
        """
        ret = "turns: " + str(self.xturn) + "\n"

        for idx in range(len(self.games)):
            ret += f"{idx} game: word is {self.games[idx].word}\n"  # add the word
            for i in range(len(self.games[idx].guesses)):
                ret += str(self.games[idx].guesses[i]) + "\n"
                ret += str(self.games[idx].feedback[i]) + "\n"
            ret += f"win? {self.games[idx].win}"
            ret += "\n\n"

        ret += "Wins: " + str(self.wins) + "\n"
        ret += "Win? " + str(self.win) + "\n"
        return ret


def play(game, max_turns=8):
    """
    Plays an interactive game of x-wordl.
    """
    # Intro
    num = game.num_games
    print(f"Welcome to {num}-Wordle!\n")

    # Play game
    while not game.is_finished(max_turns=max_turns):
        guess = input("What is your guess?\n")
        game.attempt_guess(guess)
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

    qwordle = Multi_Wordle(num_games=4)
    play(qwordle, 10)
