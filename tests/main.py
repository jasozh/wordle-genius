from bot.main import *
from wordle.main import *


def generate_word(num_words) -> list:
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
    return random.sample(data_into_list, num_words)


if __name__ == "__main__":
    num_games = 1000
    words = generate_word(num_games)

    sb = SimpleBot()
    mb = MiddleBot()
    print("Testing Simple Bot")
    sb.play_games(num_games, words=words)
    print(sb)
    with open("data/simple_bot.txt", "a") as f:
        f.write(
            f"Type: Simple Bot, Total number of games: {len(sb.games)}, Win rate: {sb.games_won / len(sb.games)}, Total turns for winning games: {sb.total_turns_won}, Avg turns: {round(sb.total_turns_won / sb.games_won, 2)}\n"
        )

    print("Testing Middle Bot")

    mb.play_games(num_games, words=words)
    print(mb)

    with open("data/middle_bot.txt", "a") as f:
        f.write(
            f"Type: Middle Bot, Total number of games: {len(mb.games)}, Win rate: {mb.games_won / len(mb.games)}, Total turns for winning games: {mb.total_turns_won}, Avg turns: {round(mb.total_turns_won / mb.games_won, 2)}\n"
        )

    # generate data for 100 games per bot
    # record type and thresholds
    for i in range(6):
        print("Testing Yellow bot " + str(i) + " right now.")
        bot = HardBot("yellow", i)
        bot.play_games(num_games, words=words)
        print(bot)
        with open("data/yellow_data.txt", "a") as f:
            f.write(
                f"Type: Yellow, Metric: {i}, Total number of games: {len(bot.games)}, Win rate: {bot.games_won / len(bot.games)}, Total turns for winning games: {bot.total_turns_won}, Avg turns: {round(bot.total_turns_won / bot.games_won, 2)}\n"
            )

    for i in range(6):
        print("Testing Aggregate bot " + str(i) + " right now.")
        bot = HardBot("aggregate", i)
        bot.play_games(num_games, words=words)
        print(bot)
        with open("data/aggregate_data.txt", "a") as f:
            f.write(
                f"Type: Aggregate, Metric: {i}, Total number of games: {len(bot.games)}, Win rate: {bot.games_won / len(bot.games)}, Total turns for winning games: {bot.total_turns_won}, Avg turns: {round(bot.total_turns_won / bot.games_won, 2)}\n"
            )

    for i in range(6):
        print("Testing Green bot " + str(i) + " right now.")
        bot = HardBot("green", i)
        bot.play_games(num_games, words=words)
        print(bot)
        with open("data/green_data.txt", "a") as f:
            f.write(
                f"Type: Green, Metric: {i}, Total number of games: {len(bot.games)}, Win rate: {bot.games_won / len(bot.games)}, Total turns for winning games: {bot.total_turns_won}, Avg turns: {round(bot.total_turns_won / bot.games_won, 2)}\n"
            )

    for i in range(0, 100, 10):
        print("Testing pool bot " + str(i) + " right now.")
        bot = HardBot("pool", i)
        bot.play_games(num_games, words=words)
        print(bot)
        with open("data/pool_data.txt", "a") as f:
            f.write(
                f"Type: Pool, Metric: {i}, Total number of games: {len(bot.games)}, Win rate: {bot.games_won / len(bot.games)}, Total turns for winning games: {bot.total_turns_won}, Avg turns: {round(bot.total_turns_won / bot.games_won, 2)}\n"
            )
