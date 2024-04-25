from main import *


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
        for idx in range(num_games):
            new_game = super.__init__()
            new_game.word = self.generate_word(new_game.answers)
            self.answers.append(new_game.word)
            self.games.append(new_game)
            self.guesses.append(new_game.guesses)
            self.feedback.append(new_game.feedback)

        self.xturn = 0
        self.wins = 0
        self.win = self.wins == self.num_games

    def generate_word(self, cant_pick_these):
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
        for game in self.games:
            game.print_game_state()

    def attempt_guess(self, guess: str):
        """
        Attempts guess as the guess for each game in the game state
        """

        for game in self.games:
            game.attempt_guess(guess)
            if game.win:  # increment the number of wins
                self.wins += 1
        self.xturn += 1  # increment number of turns
        self.win = self.wins == self.num_games

    def is_finished(self, max_turns=8) -> bool:
        """
        Returns whether the game is over or not. The game is over if the player
        wins or if the turn count exceeds max_turns. Default is 6 for regular
        Wordle games.
        """
        # Subtract 1 because self.turn is 0-indexed
        return self.turn > max_turns - 1 or self.wins == self.num_games

    def __repr__(self) -> str:
        """
        Returns a string representation of the game
        """
        ret = "turns: " + str(self.xturn) + "\n"

        for idx in range(len(self.games)):
            ret += str(idx) + " game: word is " + self.games[idx].word  # add the word
            for i in range(len(self.games[idx].guesses)):
                ret += str(self.games[idx].guesses[i]) + "\n"
                ret += str(self.games[idx].feedback[i]) + "\n"

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
    dwordle = Multi_Wordle(num_games=2)
    dwordle.play()
