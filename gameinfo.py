from abc import abstractmethod, ABC
from typing import List

from termcolor import colored
import pandas as pd


class InputError(ValueError):
    pass


def load_possible_words(path: str) -> pd.DataFrame:
    "Loads table of all possible five letter words."
    return pd.read_csv(path, encoding="cp1251")


class Letter(ABC):
    """
    Abstract class for information about presence of a letter in the word.
    """

    russian_alphabet = "абвгдежзийклмнопрстуфхшщчцьыъэюя"

    def __init__(self, letter: str, position: int = 0) -> None:
        letter = letter.lower()
        if letter not in Letter.russian_alphabet:
            wrong_letter = colored(letter, "red")
            raise InputError(
                f'The letter should be from russian alphabet excluding letter "ё". Ypu typed in "{wrong_letter}".'
            )
        self.letter = letter
        self.position = position

    @abstractmethod
    def filter(self, word: str) -> bool:
        "Checks whether the word satisfies the information about the letter."
        pass

    @abstractmethod
    def __str__(self) -> str:
        "Color code the letter"
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Letter):
            return NotImplemented
        if type(self) != type(other):
            return False
        if self.letter != other.letter:
            return False
        if self.position != other.position:
            return False
        return True

    @abstractmethod
    def description(self) -> str:
        "Description of the letter"
        pass

    @staticmethod
    @abstractmethod
    def classify(letter: str, position: int, word: str) -> bool:
        "Check whether the letter should be classified as this type."
        pass


class RejectedLetter(Letter):
    "The class for absent in the word letters."

    def filter(self, word: str, position: int = 0) -> bool:
        if self.letter in word:
            return False
        return True

    def __str__(self) -> str:
        return self.letter.upper()

    def description(self) -> str:
        colored_letter = colored(self.letter, "red")
        return f'There is not letter "{colored_letter}" in the word.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        return False if letter in word else True


class AcceptedLetterWrongPosition(Letter):
    """
    The class for letters present in the word, but the position of which is not guessed.
    """

    def __str__(self) -> str:
        return colored(self.letter.upper(), attrs=["reverse"])

    def filter(self, word: str) -> bool:
        if self.letter not in word:
            return False
        if word[self.position - 1] == self.letter:
            return False
        return True

    def description(self) -> str:
        colored_letter = colored(self.letter, "yellow")
        colored_position = colored(self.position, "yellow")
        return f'There is the letter "{colored_letter}" in the word, but no at position {colored_position}.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        if letter not in word:
            return False
        if word[position] == letter:
            return False
        return True


class AcceptedLetterCorrectPosition(Letter):
    """The class for present letters exact position of which is guessed."""

    def __str__(self) -> str:
        return colored(self.letter.upper(), "yellow", attrs=["reverse"])

    def filter(self, word: str) -> bool:
        if word[self.position - 1] != self.letter:
            return False
        return True

    def description(self) -> str:
        colored_letter = colored(self.letter, "green")
        colored_position = colored(self.position, "green")
        return f'The letter "{colored_letter}" is at position {colored_position} in the word.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        return True if word[position] == letter else False


def classify_letter(letter: str, position: int, correct_word: str) -> Letter:
    """
    Classifies the letter to one of three types and returns an instance of correct class.
    """
    for letter_type in (
        RejectedLetter,
        AcceptedLetterWrongPosition,
        AcceptedLetterCorrectPosition,
    ):
        if letter_type.classify(letter, position, correct_word):
            return letter_type(letter, position + 1)


def filter_impossible_words(words: pd.DataFrame, info: List[Letter]) -> pd.DataFrame:
    """
    Filters impossible words from the table according to the information in all letters
    """
    for letter in info:
        mask = words["word"].map(letter.filter)
        words = words[mask]
    return words
