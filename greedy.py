from functools import partial
from sqlite3 import adapt
from typing import List
from argparse import ArgumentParser, Namespace
from collections import Counter

import pandas as pd

from gameinfo import Letter, filter_impossible_words, load_possible_words
from wordlealgorithm import WordleAlgorithm
from interaction import interact


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--adapt",
        default=True,
        type=bool,
        help="boolean value defining whether to recalculate frequency of letters on each step",
    )
    parser.add_argument(
        "--t",
        default="./five_letter_words.csv",
        help="path to the table with all possible words",
    )
    parser.add_argument(
        "--n", type=int, default=15, help="number of words to show on each iteration"
    )
    return parser.parse_args()


def add_frequency_column(words: pd.DataFrame) -> pd.DataFrame:
    """
    for each word in the table computes total frequency of letters
    and adds corresponding column to the table
    """
    letter_frequencies = compute_frequencies_of_letters(words["word"])
    f = partial(total_frequency_of_word, letter_frequencies=letter_frequencies)
    words["frequency"] = words["word"].map(f)
    return words.sort_values("frequency", ascending=False)


def total_frequency_of_word(word: str, letter_frequencies: pd.Series) -> float:
    """
    computes total frequency of letters in the word
    """
    unique_letters = set(word)
    return sum(letter_frequencies.loc[letter] for letter in unique_letters)


def compute_frequencies_of_letters(words: pd.Series) -> pd.Series:
    """
    computes frequencies of each letter in the table of words
    and returns this as pandas.Series
    """
    letter_counter = Counter()
    for word in words:
        letter_counter.update(word)
    letter_frequencies = pd.Series(letter_counter)
    return letter_frequencies / letter_frequencies.sum()


class GreedyAlgorithm(WordleAlgorithm):
    """
    Greedy algorithm which values a word based on frequencies of letters
    the word consists of: the more total frequency of letter in the word
    the better the guess. Frequency of a letter is computed based on the
    table of all possible five letter words. Algorithm can work in adap-
    tive mode in which it recompute letter frequencies each time a new
    information has come.
    """

    def __init__(self, possible_words: pd.DataFrame, adapt: bool = True) -> None:
        super().__init__(add_frequency_column(possible_words.copy()))
        self.adapt = adapt

    def rank_guesses(self, info: List[Letter]) -> pd.DataFrame:
        """
        ranks all possible words on the basis of total frequencies of
        letters in a words and return it in the form of table.
        """
        words = filter_impossible_words(self.possible_words, info)
        if self.adapt:
            words = add_frequency_column(words)
        self.possible_words = words.sort_values("frequency", ascending=False)
        return self.possible_words

    def guess(self, info: List[Letter]) -> str:
        """
        computes and returns the word with biggest total frequencies of
        letters.
        """
        self.possible_words = filter_impossible_words(self.possible_words, info)
        if self.adapt:
            self.possible_words = add_frequency_column(self.possible_words)
        return self.possible_words["word"].iloc[0]


def main():
    args = parse_args()
    possible_words = load_possible_words(path=args.t)
    guesser = GreedyAlgorithm(possible_words=possible_words, adapt=adapt)
    interact(guesser, words_to_show=args.n)


if __name__ == "__main__":
    main()
