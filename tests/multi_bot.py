from bot.multi_bot import *
from wordle.main import *


def generate_words(words_per_list, num_lists) -> list:
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
    ret = []
    for i in range(num_lists):
        answers = random.sample(data_into_list, words_per_list)
        ret.append(answers)
    return ret


if __name__ == "__main__":
    num_lists = 1000
    num_words_per_list = 4
    max_turns = 30

    words = generate_words(num_words_per_list, num_lists)

    print("NaiveBot playing")
    nb = NaiveBot()
    nb.play_games(num_lists, max_turns, num_words_per_list, words)
    print(nb)

    print("GreedyBot playing")
    gb = GreedyBot()
    gb.play_games(num_lists, max_turns, num_words_per_list, words)
    print(gb)
