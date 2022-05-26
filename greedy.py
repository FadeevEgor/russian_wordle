from functools import partial
import os
from typing import List
from argparse import ArgumentParser
from collections import Counter

import pandas as pd
from gameinfo import Letter, InputError, parse_info
from wordlealgorithm import WordleAlgorithm


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--update_frequencies",
        default=False,
        type=bool,
        help="whether to update frequencies on each step or not.",
    )
    parser.add_argument(
        "--words",
        default="./five_letter_words.csv",
        help="path to file with all possible words",
    )
    parser.add_argument(
        "--n", type=int, default=15, help="number of words to show on each iteration"
    )
    return parser.parse_args()


def load_possible_words(words_path: str) -> pd.DataFrame:
    return pd.read_csv(words_path, encoding="cp1251")


def add_frequency_column(words: pd.DataFrame) -> pd.DataFrame:
    letter_frequencies = compute_frequencies_of_letters(words["word"])
    f = partial(total_frequency_of_word, letter_frequencies=letter_frequencies)
    words["frequency"] = words["word"].map(f)
    return words.sort_values("frequency", ascending=False)


def total_frequency_of_word(word: str, letter_frequencies: pd.Series) -> float:
    unique_letters = set(word)
    return sum(letter_frequencies.loc[letter] for letter in unique_letters)


def compute_frequencies_of_letters(words: pd.Series) -> pd.Series:
    letter_counter = Counter()
    for word in words:
        letter_counter.update(word)
    letter_frequencies = pd.Series(letter_counter)
    return letter_frequencies / letter_frequencies.sum()


def print_instruction():
    print("Введи новую полученную информацию в формате 'буква код'.")
    print(
        "- код = 1...5 - порядковый номер буквы в слове, если угадано точное положение буквы;"
    )
    print("- код = 0, если буквы в слове нет;")
    print(
        "- код = -5...-1, если угадана буква, но не её позиция, то позиция указывается с отрицательным знаком."
    )
    print("Пустая строка, чтобы выйти.")


class GreedyAlgorithm(WordleAlgorithm):
    def __init__(self, words: pd.DataFrame, update_frequencies: bool = True) -> None:
        self.words = add_frequency_column(words.copy())
        self.update_frequencies = update_frequencies

    def k_guesses(self, info: List[Letter], k: int = 15) -> pd.DataFrame:
        for letter in info:
            mask = self.words["word"].map(letter.filter)
            self.words = self.words[mask]
        if self.update_frequencies:
            self.words = add_frequency_column(self.words)
        return self.words.head(k)

    def guess(self, info: List[Letter]) -> str:
        for letter in info:
            mask = self.words["word"].map(letter.filter)
            self.words = self.words[mask]
        if self.update_frequencies:
            self.words = add_frequency_column(self.words)
        return self.words["word"].iloc[0]


def main():
    args = parse_args()
    words_to_show: int = args.n
    update_frequencies = args.update_frequencies
    words_path: str = args.words

    words: pd.DataFrame = load_possible_words(words_path)
    guesser = GreedyAlgorithm(words, update_frequencies)
    info: list[Letter] = []
    while True:
        print("=" * 80)
        top_k_guesses = guesser.k_guesses(info, words_to_show)
        print(
            f"Вот список {words_to_show} лучших слов из {len(guesser.words)} возможных."
        )
        print(top_k_guesses.to_string(index=False))
        print_instruction()
        try:
            letter = parse_info()
        except InputError as msg:
            print(msg)
            continue
        if letter is None:
            break

        print(letter.description())
        info.append(letter)

    print("Выход.")


if __name__ == "__main__":
    main()
