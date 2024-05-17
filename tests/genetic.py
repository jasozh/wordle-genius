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
    num_games = 100
    words = generate_word(num_games)

    mbrand = MiddleBot()
    mbtf = MiddleBotTf()
    mbgenetic = MiddleBotGenetic()
    print("Testing Middle Bot with random")
    mbrand.play_games(num_games, words=words)
    with open("data/middlebot_compare.txt", "a") as f:
        f.write(
            f"Type: Middle bot with random\tTotal number of games: {len(mbrand.games)}, Win rate: {mbrand.games_won / len(mbrand.games)}, Total turns for winning games: {mbrand.total_turns_won}, Avg turns: {round(mbrand.total_turns_won / mbrand.games_won, 2)}\n"
        )

    print("Testing Middle Bot with tf")
    mbtf.play_games(num_games, words=words)

    with open("data/middlebot_compare.txt", "a") as f:
        f.write(
            f"Type: Middle bot with tf\t\tTotal number of games: {len(mbtf.games)}, Win rate: {mbtf.games_won / len(mbtf.games)}, Total turns for winning games: {mbtf.total_turns_won}, Avg turns: {round(mbtf.total_turns_won / mbtf.games_won, 2)}\n"
        )

    print("Testing Middle Bot with genetic")
    mbgenetic.play_games(num_games, words=words)

    with open("data/middlebot_compare.txt", "a") as f:
        f.write(
            f"Type: Middle bot with genetic\tTotal number of games: {len(mbgenetic.games)}, Win rate: {mbgenetic.games_won / len(mbgenetic.games)}, Total turns for winning games: {mbgenetic.total_turns_won}, Avg turns: {round(mbgenetic.total_turns_won / mbgenetic.games_won, 2)}\n"
        )
