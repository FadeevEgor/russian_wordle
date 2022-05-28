from abc import ABC, abstractmethod
from typing import List
from string import Template

from gameinfo import (
    Letter,
    RejectedLetter,
    AcceptedLetterWrongPosition,
    AcceptedLetterCorrectPosition,
    filter_impossible_words,
)

import pandas as pd


class IncorrectWordError:
    "Should be raised when incorrect word was"


class WordleAlgorithm(ABC):
    """
    Abstract base class for an wordle algorithm.
    Should be able to make a guess based on words possible and information gained.
    """

    def __init__(self, possible_words: pd.DataFrame) -> None:
        self.possible_words = possible_words

    @abstractmethod
    def guess(self, info: List[Letter]) -> str:
        "Makes a guess"
        pass

    @abstractmethod
    def rank_guesses(self, info: List[Letter]) -> pd.DataFrame:
        "Ranks all possible words."
        pass


class ManualAlgorithm(WordleAlgorithm):
    def __init__(self, possible_words: pd.DataFrame) -> None:
        super().__init__(possible_words)
        self.print_instruction()

    def guess(self, info: List[Letter]) -> str:
        return input().strip().lower()

    def rank_guesses(self, info: List[Letter]) -> pd.DataFrame:
        return filter_impossible_words(self.possible_words, info)

    def print_instruction(self):
        with open("./player_instruction.txt") as f:
            instruction = f.read()
        instruction = Template(instruction).substitute(
            {
                "a": RejectedLetter("а"),
                "b": AcceptedLetterWrongPosition("б"),
                "c": AcceptedLetterCorrectPosition("в"),
            }
        )
        print(instruction)
        input("Press Enter to start!")
