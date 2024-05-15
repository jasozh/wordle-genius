from bot.multi_bot import *
from wordle.multi_wordle import *


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


def generate_answers_list(num_instances, games_per_instance) -> list:
    """
    generates a list of length num_games of num_words unique words
    """
    lst = []
    for _ in range(num_instances):
        lst.append(generate_word(games_per_instance))

    return lst


if __name__ == "__main__":
    num_instances = 100
    games_per_instance = 4

    max_turn = 10
    words_list = generate_answers_list(num_instances, games_per_instance)

    nb = NaiveBot()
    nb.play_games(
        num_instances,
        max_turns=max_turn,
        num_games=games_per_instance,
        words=words_list,
    )
    print("NaiveBot")
    print(nb)
    gb = GreedyBot()
    gb.play_games(
        num_instances,
        max_turns=max_turn,
        num_games=games_per_instance,
        words=words_list,
    )
    print("GreedyBot:")
    print(gb)
