from bot.main import *
from wordle.main import *

if __name__ == "__main__":

    # generate data for 100 games per bot
    # record type and thresholds
    for i in range(6):
        print("Testing Yellow bot " + str(i) + " right now.")
        bot = HardBot("yello", i)
        bot.play_games(100)
        with open("tests/yellow_data.txt", "a") as f:
            f.write(
                f"Type: Yellow, Metric: {i}, Total number of games: {bot.num_games}, Win rate: {bot.games_won/bot.num_games}, Avg turns: {bot.total_turns / bot.num_games}\n"
            )

    # for i in range(6):
    #     print("Testing Aggregate bot " + str(i) + " right now.")
    #     bot = HardBot("aggregate", i)
    #     bot.play_games(100)
    #     with open("data/aggregate_data.txt", "a") as f:
    #         f.write(
    #             f"Type: Aggregate, Metric: {i}, Total number of games: {bot.num_games}, Win rate: {bot.win_rate/bot.num_games}, Avg turns: {bot.total_turns / bot.num_games}\n"
    #         )

    # for i in range(6):
    #     print("Testing Green bot " + str(i) + " right now.")
    #     bot = HardBot("green", i)
    #     bot.play_games(100)
    #     with open("data/green_data.txt", "a") as f:
    #         f.write(
    #             f"Type: Green, Metric: {i}, Total number of games: {bot.num_games}, Win rate: {bot.win_rate/bot.num_games}, Avg turns: {bot.total_turns / bot.num_games}\n"
    #         )

    # for i in range(0, 100, 10):
    #     print("Testing pool bot " + str(i) + " right now.")
    #     bot = HardBot("pool", i)
    #     bot.play_games(100)
    #     with open("data/pool_data.txt", "a") as f:
    #         f.write(
    #             f"Type: Pool, Metric: {i}, Total number of games: {bot.num_games}, Win rate: {bot.win_rate/bot.num_games}, Avg turns: {bot.total_turns / bot.num_games}\n"
    #         )
