from statistics import mean, mode, median
from typing import List
from argparse import ArgumentParser, Namespace

import pandas as pd
from tqdm import tqdm

from gameinfo import (
    Letter,
    classify_letter,
    filter_impossible_words,
    load_possible_words,
)
from wordlealgorithm import WordleAlgorithm
from interaction import interact

supported_statistics = {
    "mean": mean,
    "max": max,
    "mode": mode,
    "median": median,
}


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--stat",
        default="mean",
        choices=supported_statistics.keys(),
        help="statistic to use.",
    )
    parser.add_argument(
        "--t",
        default="./five_letter_words.csv",
        help="path to file with all possible words",
    )
    parser.add_argument(
        "--n", type=int, default=15, help="number of words to show on each iteration"
    )
    return parser.parse_args()


class CuttingAlgorithm(WordleAlgorithm):
    """
    The algorithm which for each possible word estimates the number of words
    is going to be left if the word is used as a guess: the fewer words left
    the better the guess. By default the ranking of guesses is performed based
    on average number words left, but following statistics can be specified: max,
    mode and median.
    """

    def __init__(self, possible_words: pd.DataFrame, stat: str = "mean") -> None:
        super().__init__(possible_words)
        self.stat = stat

    def rank_guesses(self, info: List[Letter]) -> pd.DataFrame:
        "Ranks all possible guesses based on statistic chosen"
        self.possible_words = filter_impossible_words(self.possible_words, info)
        if len(self.possible_words) < 1000:
            print(len(self.possible_words))
            cuts_estimation = self.estimate_cuts(info)
            return cuts_estimation.sort_values(self.stat)
        return pd.DataFrame({"word": ["окрас"]})

    def guess(self, info: List[Letter]) -> str:
        "Returns the most prominent word based on statistic chosen"
        self.possible_words = filter_impossible_words(self.possible_words, info)
        if len(self.possible_words) < 1000:
            cuts_estimation = self.estimate_cuts(info)
            return cuts_estimation.idxmin()[self.stat]
        return "окрас"

    def estimate_cuts(self, info: List[Letter]) -> pd.DataFrame:
        "For each word computes statistics of expected words left"
        cuts_estimation = {}
        words = filter_impossible_words(self.possible_words, info)
        words_list = words["word"].to_list()
        for guess in tqdm(words_list):
            distribution = [
                cut_size(guess, target, info, words) for target in words_list
            ]
            cuts_estimation[guess] = {
                name: f(distribution) for name, f in supported_statistics.items()
            }
        return pd.DataFrame(cuts_estimation).transpose().reset_index()


def cut_size(
    guess: str, correct_word: str, info: List[Letter], words: pd.DataFrame
) -> int:
    "Computes number of words left for specified guess and correct word"
    words = filter_impossible_words(
        words.copy(),
        info + [classify_letter(l, i, correct_word) for i, l in enumerate(guess)],
    )
    return len(words)


def main():
    args = parse_args()
    words_to_show: int = args.t
    stat = args.stat
    words_path: str = args.words

    words = load_possible_words(words_path)
    guesser = CuttingAlgorithm(words, stat)
    interact(guesser, words_to_show)


if __name__ == "__main__":
    main()
