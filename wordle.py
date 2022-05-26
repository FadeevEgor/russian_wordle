from random import choice
from typing import Set, Optional, List
import os
import argparse
from greedy import GreedyAlgorithm

import pandas as pd

from wordlealgorithm import WordleAlgorithm, ManualAlgorithm
from gameinfo import (
    Letter,
    RejectedLetter,
    AcceptedLetterCorrectPosition,
    AcceptedLetterWrongPosition,
)


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
    parser.add_argument(
        "--algorithm",
        help="""Algorithm to run. 
        Default: Manual""",
    )
    return parser.parse_args()


def load_possible_words(words_path: str) -> set:
    return pd.read_csv("./five_letter_words.csv", encoding="cp1251")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class GameState:
    def __init__(self, correct_word: str) -> None:
        self.correct_word = correct_word
        self.guesses: List[List[Letter]] = []

    def classify_letter(self, letter: str, position: int) -> Letter:
        for letter_type in (
            RejectedLetter,
            AcceptedLetterWrongPosition,
            AcceptedLetterCorrectPosition,
        ):
            if letter_type.classify(letter, position, self.correct_word):
                return letter_type(letter, position)

    def add_guess(self, guess: str) -> None:
        self.guesses.append([self.classify_letter(l, i) for i, l in enumerate(guess)])

    def print_tabloid(self) -> None:
        clear_screen()
        if not self.guesses:
            return
        for guess in self.guesses:
            print(*guess, sep="")

    @property
    def game_info(self) -> List[Letter]:
        return [letter for guess in self.guesses for letter in guess]

    @property
    def number_of_attempts(self) -> int:
        return len(self.guesses)


def play_game(
    correct_word: str,
    possible_words: pd.DataFrame,
    guesser: Optional[WordleAlgorithm] = None,
):
    if guesser is None:
        guesser = ManualAlgorithm(possible_words)
    game_state = GameState(correct_word)
    guess = ""
    while True:
        game_state.print_tabloid()
        guess = guesser.guess(game_state.game_info)
        print(guess)
        if guess == "":
            break

        if guess not in possible_words["word"].to_list():
            if not isinstance(guesser, ManualAlgorithm):
                raise IncorrectWord(
                    f"Автоматический алгоритм выдал слово, которого нет в таблице: {guess}"
                )
            continue
        game_state.add_guess(guess)

        if guess == correct_word:
            game_state.print_tabloid()
            print(
                f"Поздравляю, вы угадали слово {correct_word} за {game_state.number_of_attempts} попыток!"
            )
            break

    print("Выход.")


def main():
    args = parse_args()

    possible_words: pd.DataFrame = load_possible_words(args.possible_words)
    correct_word: str = (
        choice(possible_words["word"])
        if args.correct_word is None
        else args.correct_word
    )
    correct_word = correct_word.lower()
    if correct_word not in possible_words["word"].to_list():
        raise IncorrectWord("Вы загадали слово, которого нет в нашей таблице.")

    algorithm = args.algorithm
    if algorithm == "greedy":
        algorithm = GreedyAlgorithm(possible_words)

    play_game(correct_word, possible_words, algorithm)


if __name__ == "__main__":
    main()
