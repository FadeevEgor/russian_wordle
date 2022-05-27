from abc import abstractmethod, ABC
from re import A
from typing import Optional, Any, List

from termcolor import colored


class InputError(ValueError):
    pass


class Letter(ABC):
    russian_alphabet = "абвгдежзийклмнопрстуфхшщчцьыъэюя"

    def __init__(self, letter: str, position: int = 0) -> None:
        letter = letter.lower()
        if letter not in Letter.russian_alphabet:
            wrong_letter = colored(letter, "red")
            raise InputError(
                f'Буква должна быть из русского алфавита, не включая "ё". Вы ввели "{wrong_letter}".'
            )
        self.letter = letter
        self.position = position

    @abstractmethod
    def filter(self, word: str) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
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
        pass

    @staticmethod
    @abstractmethod
    def classify(letter: str, position: int, word: str) -> bool:
        pass


class RejectedLetter(Letter):
    def filter(self, word: str, position: int = 0) -> bool:
        if self.letter in word:
            return False
        return True

    def __str__(self) -> str:
        return self.letter.upper()

    def description(self) -> str:
        colored_letter = colored(self.letter, "red")
        return f'Буквы "{colored_letter}" нет в слове.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        return False if letter in word else True


class AcceptedLetterWrongPosition(Letter):
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
        return f'Буква "{colored_letter}" есть в слове, но не на {colored_position}-й позиции.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        if letter not in word:
            return False
        if word[position] == letter:
            return False
        return True


class AcceptedLetterCorrectPosition(Letter):
    def __str__(self) -> str:
        return colored(self.letter.upper(), "yellow", attrs=["reverse"])

    def filter(self, word: str) -> bool:
        if word[self.position - 1] != self.letter:
            return False
        return True

    def description(self) -> str:
        colored_letter = colored(self.letter, "green")
        colored_position = colored(self.position, "greed")
        return f'Буква "{colored_letter}" есть в слове на {colored_position}-й позиции.'

    @staticmethod
    def classify(letter: str, position: int, word: str) -> bool:
        return True if word[position] == letter else False


def parse_info() -> Optional[Letter]:
    info = input()
    if info.strip() == "":
        return None

    # check correctness
    try:
        letter, code = info.split()
    except ValueError:
        raise InputError(
            "Должно быть ровно два значения (буква и код), разделенных пробелом."
        )

    try:
        code = int(code)
    except ValueError:
        raise InputError("Код должен быть целым числом.")

    if code not in range(-5, 6):
        raise InputError("Код должен быть в диапазоне от -5 до 5.")

    # make an instance of Letter
    if code == 0:
        return RejectedLetter(letter)
    elif code > 0:
        return AcceptedLetterCorrectPosition(letter, code)
    elif code < 0:
        return AcceptedLetterWrongPosition(letter, -code)
    else:
        raise ValueError(f"Не предусмотренный код: {code}")
