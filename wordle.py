from random import choice
from typing import Optional, List
import os
import argparse
from greedy import GreedyAlgorithm

import pandas as pd

from wordlealgorithm import WordleAlgorithm, ManualAlgorithm
from gameinfo import Letter, classify_letter, load_possible_words


class IncorrectWord(ValueError):
    """Raised when incorrect word is used as a guess"""

    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--word",
        default=None,
        help="word to guess, randomly chosen if not specified",
    )
    parser.add_argument(
        "--t",
        default="./five_letter_words.csv",
        help="path to file with all possible words",
    )
    parser.add_argument(
        "--algorithm",
        help="""Algorithm to run. 
        Default: Manual""",
    )
    return parser.parse_args()


def clear_screen():
    """Clears command line screen."""
    os.system("cls" if os.name == "nt" else "clear")


class GameState:
    """
    Represents the state of the game. Keeps track of correct word
    and all the guesses. Returns information about the letters
    according to guesses made.
    """

    def __init__(self, correct_word: str) -> None:
        self.correct_word = correct_word
        self.guesses: List[List[Letter]] = []

    def add_guess(self, guess: str) -> None:
        "New guess"
        self.guesses.append(
            [classify_letter(l, i, self.correct_word) for i, l in enumerate(guess)]
        )

    def print_tabloid(self) -> None:
        "Prints tabloid"
        clear_screen()
        for guess in self.guesses:
            print(*guess, sep="")

    @property
    def game_info(self) -> List[Letter]:
        "Returns all information gained from all the guesses"
        return [letter for guess in self.guesses for letter in guess]

    @property
    def number_of_attempts(self) -> int:
        "Number of guesses so far"
        return len(self.guesses)


def play_game(
    correct_word: str,
    possible_words: pd.DataFrame,
    guesser: Optional[WordleAlgorithm] = None,
) -> None:
    """
    Plays a round of game wordle.
    The third optional parameter specifies algorithm to play with.
    If None is passed the game is played manually.
    """
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
                    f"Automatic algorithm returned a word not present in the table of all possible words: {guess}"
                )
            continue
        game_state.add_guess(guess)

        if guess == correct_word:
            game_state.print_tabloid()
            print(
                f'Congratulations, you guessed the word "{correct_word}" in {game_state.number_of_attempts} attempts!'
            )
            break

    print("Exiting.")


def main():
    args = parse_args()

    possible_words: pd.DataFrame = load_possible_words(args.t)
    correct_word: str = (
        choice(possible_words["word"]) if args.word is None else args.word
    )
    correct_word = correct_word.lower()
    if correct_word not in possible_words["word"].to_list():
        raise IncorrectWord(
            f'You typed in the word "{correct_word}" which is not in the table of all possible words.'
        )

    algorithm = args.algorithm
    if algorithm == "greedy":
        algorithm = GreedyAlgorithm(possible_words)

    play_game(correct_word, possible_words, algorithm)


if __name__ == "__main__":
    main()
