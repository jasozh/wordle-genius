import bot.main
import bot.multi_bot
import bot.quantum
import wordle.main
import wordle.multi_wordle
import wordle.quantum

if __name__ == "__main__":
    print(
        """Welcome to Wordle Genius!

[1] - Play a game of Wordle
[2] - Play a game of Multi-Wordle
[3] - Play a game of Quantum Wordle
"""
    )
    game = input("> ")
    match game:
        case "1":
            print(
                """Choose a bot to help you!
[1] - SimpleBot
[2] - MiddleBot (random)
[3] - MiddleBot (term frequency)
[4] - MiddleBot (genetic)
[5] - HardBot
"""
            )
            bot_input = input("> ")
            helper_bot = None
            match bot_input:
                case "1":
                    helper_bot = bot.main.SimpleBot()
                case "2":
                    helper_bot = bot.main.MiddleBot()
                case "3":
                    helper_bot = bot.main.MiddleBotTf()
                case "4":
                    helper_bot = bot.main.MiddleBotGenetic()
                case "5":
                    print(
                        "What type of metric would you like to use? \n"
                        + "Green: number of green letters revealed \n"
                        + "Yellow: number of yellow letters revealed \n"
                        + "Aggregate: number of green or yellow letters revealed \n"
                        + "Pool: size of remaining words without any previously-guessed letters"
                    )
                    metric = ""
                    while metric not in ["green", "yellow", "aggregate", "pool"]:
                        metric = input("> ").lower()
                        if metric in ["green", "yellow", "aggregate"]:
                            thresh = -1
                            while thresh not in [0, 1, 2, 3, 4, 5]:
                                print("Please choose a threshold: 0, 1, 2, 3, 4, 5")
                                thresh = int(input("> "))
                                if thresh not in [0, 1, 2, 3, 4, 5]:
                                    print("You picked an invalid threshold")
                        elif metric == "pool":
                            thresh = -1
                            while thresh not in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
                                print(
                                    "Please choose a threshold: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90"
                                )
                                thresh = int(input("> "))
                                if thresh not in [
                                    0,
                                    10,
                                    20,
                                    30,
                                    40,
                                    50,
                                    60,
                                    70,
                                    80,
                                    90,
                                ]:
                                    print("You picked an invalid threshold")
                        else:
                            print("You picked an invalid metric. Please pick again")

                    helper_bot = bot.main.HardBot(metric, thresh)
                case _:
                    print("Invalid input.")

            wordle.main.play(helper_bot=helper_bot)
        case "2":
            num_games = 0
            while num_games <= 0:
                num_games = int(
                    input("How many simultaneous games would you like to play? \n> ")
                )
                if num_games <= 0:
                    print("You've selected in an valid number of games")
            print(
                """Choose a bot to help you!
[1] - NaiveBot
[2] - GreedyBot
"""
            )
            bot_input = input("> ")
            helper_bot = None
            match bot_input:
                case "1":
                    helper_bot = bot.multi_bot.NaiveBot()
                case "2":
                    helper_bot = bot.multi_bot.GreedyBot()
                case _:
                    print("Invalid input.")

            multi_wordle = wordle.multi_wordle.Multi_Wordle(num_games=num_games)
            wordle.multi_wordle.play(
                multi_wordle, max_turns=int(num_games * 2.5), helper_bot=helper_bot
            )
        case "3":
            print("You will be assisted by Quantum Bot!")
            helper_bot = bot.quantum.QuantumBot()
            wordle.quantum.play(helper_bot=helper_bot)
        case _:
            print("Invalid input.")
