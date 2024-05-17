import bot.main
import bot.multi_bot
import bot.quantum
import wordle.main
import wordle.multi_wordle
import wordle.quantum

if __name__ == "__main__":
    print("""Welcome to Wordle Genius!

[1] - Play a game of Wordle
[2] - Play a game of Multi-Wordle
[3] - Play a game of Quantum Wordle
""")
    game = input("> ")
    match game:
        case "1":
            print("""Choose a bot to help you!
[1] - SimpleBot
[2] - MiddleBot (random)
[3] - MiddleBot (term frequency)
[4] - MiddleBot (genetic)
[5] - HardBot
""")
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
                    helper_bot = bot.main.HardBot()
                case _:
                    print("Invalid input.")

            wordle.main.play(helper_bot=helper_bot)
        case "2":
            print("""Choose a bot to help you!
[1] - NaiveBot
[2] - GreedyBot
""")
            bot_input = input("> ")
            helper_bot = None
            match bot_input:
                case "1":
                    helper_bot = bot.multi_bot.NaiveBot()
                case "2":
                    helper_bot = bot.multi_bot.GreedyBot()
                case _:
                    print("Invalid input.")

            multi_wordle = wordle.multi_wordle.Multi_Wordle(num_games=2)
            wordle.multi_wordle.play(multi_wordle)
        case "3":
            print("You will be assisted by Quantum Bot!")
            helper_bot = bot.quantum.QuantumBot()
            wordle.quantum.play(helper_bot=helper_bot)
        case _:
            print("Invalid input.")
