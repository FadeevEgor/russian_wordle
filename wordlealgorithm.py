from abc import ABC, abstractmethod
from gameinfo import (
    Letter,
    RejectedLetter,
    AcceptedLetterWrongPosition,
    AcceptedLetterCorrectPosition,
)
from typing import List, Set

import pandas as pd


class IncorrectWordError:
    "Should be raised when incorrect word was"


class WordleAlgorithm(ABC):
    @abstractmethod
    def guess(self, info: List[Letter]) -> str:
        pass


class ManualAlgorithm(WordleAlgorithm):
    def __init__(self, possible_words: pd.DataFrame) -> None:
        super().__init__()
        self.possible_words = possible_words
        self.print_instruction()

    def guess(self, info: List[Letter]) -> str:
        return input().strip().lower()

    def print_instruction(self):
        wrong_letter = RejectedLetter("а")
        correct_letter_wrong_position = AcceptedLetterWrongPosition("б")
        correct_letter_correct_position = AcceptedLetterCorrectPosition("в")
        print("На каждом ходу вы совершаете догадку, вводя слово из 5 букв.")
        print("В ответ вы получаете слово закодированную цветом информацию:")
        print(f"{str(wrong_letter)} - не угадана буква;", end=", ")
        print(
            f"{str(correct_letter_wrong_position)} - угадана буква, но не позиция;",
            end=", ",
        )
        print(
            f"{correct_letter_correct_position} - угадана буква и позиция.",
        )
        input("Нажмите Enter, чтобы начать!")
