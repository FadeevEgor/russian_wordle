from random import choice
from typing import Set
import os

import argparse
from termcolor import colored


class IncorrectWord(ValueError):
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--correct_word", default=None, help="word to guess")
    parser.add_argument(
        "--possible_words",
        default="./five_letter_words.csv",
        help="path to file with all possible words",
    )
    return parser.parse_args()


def load_possible_words(words_path: str) -> set:
    with open(words_path, encoding="cp1251") as f:
        words = f.read().splitlines()
    return set(words[1:])


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_instruction():
    wrong_letter = colored("а", "white", "on_grey")
    correct_letter_wrong_position = colored("б", attrs=["reverse"])
    correct_letter_correct_position = colored("в", "yellow", attrs=["reverse"])

    print("На каждом ходу вы совершаете догадку, вводя слово из 5 букв.")
    print("В ответ вы получаете слово закодированную цветом информацию:")
    print(f"{wrong_letter} - не угадана буква;", end=", ")
    print(f"{correct_letter_wrong_position} - угадана буква, но не позиция;", end=", ")
    print(
        f"{correct_letter_correct_position} - угадана буква и позиция.",
    )
    input("Нажмите Enter, чтобы начать!")


def color_letters(guess: str, correct_word):
    letters = []
    for i, letter in enumerate(guess):
        if letter not in correct_word:
            letters.append(colored(letter, "white", "on_grey"))
        elif correct_word[i] == letter:
            letters.append(colored(letter, "yellow", attrs=["reverse"]))
        else:
            letters.append(colored(letter, attrs=["reverse"]))
    return "".join(letters)


def play_game(correct_word: str, possible_words: Set[str]):
    tabloid = []
    print_instruction()
    guess = ""
    while True:
        clear_screen()
        if tabloid:
            print(*tabloid, sep="\n")
        if guess == correct_word:
            attempts = len(tabloid)
            print(f"Поздравляю, вы угадали слово {correct_word} за {attempts} попыток!")
            break

        guess = input().strip().lower()
        if guess == "":
            break
        if guess not in possible_words:
            print("Вы загадали слово, которого нет в нашей таблице.")
            continue

        colored_guess = color_letters(guess, correct_word)
        tabloid.append(colored_guess)

    print("Выход.")


def main():
    args = parse_args()
    possible_words: Set[str] = load_possible_words(args.possible_words)
    correct_word: str = (
        choice(list(possible_words)) if args.correct_word is None else args.correct_word
    )
    correct_word = correct_word.lower()
    if correct_word not in possible_words:
        raise IncorrectWord("Вы загадали слово, которого нет в нашей таблице.")
    play_game(correct_word, possible_words)


if __name__ == "__main__":
    main()
