import os
from typing import List
from argparse import ArgumentParser

import pandas as pd
from gameinfo import Letter, InputError, parse_info


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--frequencies",
        default="./letter_frequencies.csv",
        help="path to letter frequencies table",
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


def load_tables(frequencies_path: str, words_path: str) -> pd.DataFrame:
    frequencies = pd.read_csv(
        frequencies_path, sep=";", index_col="letter", encoding="cp1251"
    )
    frequencies.loc["е"] += frequencies.loc["ё"]

    words = pd.read_csv(words_path, encoding="cp1251")
    words.head()

    def total_probability(word: str) -> float:
        unique_letters = set(word)
        return sum(frequencies.loc[letter, "frequency"] for letter in unique_letters)

    words["probability"] = words["word"].map(total_probability)
    return words.sort_values("probability", ascending=False)


def consider_info(words: pd.DataFrame, info: List[Letter]) -> pd.DataFrame:
    for letter in info:
        mask = words["word"].map(letter.filter)
        words = words[mask]
    return words


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


def greedy():
    args = parse_args()

    words: pd.DataFrame = load_tables(args.frequencies, args.words)
    info: list[Letter] = []
    words_to_show = args.n

    while True:
        print("=" * 80)
        words = consider_info(words, info)
        print(f"Вот список {words_to_show} лучших слов из {len(words)} возможных.")
        print(words.head(words_to_show).to_string(index=False))
        print_instruction()
        try:
            letter = parse_info()
        except InputError as msg:
            print(msg)
            continue
        if letter is None:
            break

        print(letter)
        info.append(letter)

    print("Выход.")


if __name__ == "__main__":
    greedy()
