from abc import abstractmethod, ABC
from re import A
from typing import Optional, Any

from colorama import Fore, Style, init
init(autoreset=True)

green_font = Fore.GREEN
red_font = Fore.RED
yellow_font = Fore.YELLOW
reset_style = Style.RESET_ALL

russian_alphabet = "абвгдежзийклмнопрстуфхшщчцьыъэюя"
class InputError(ValueError):
    pass


def colorcode(x: Any, color: Fore) -> str:
    return f"{color}{x}{reset_style}"


class Letter(ABC):
    def __init__(self, letter: str):
        letter = letter.lower()
        if letter not in russian_alphabet:
            wrong_letter = colorcode(letter, red_font)
            raise InputError(f'Буква должна быть из русского алфавита, не включая "ё". Вы ввели "{wrong_letter}".')
        self.letter = letter
        
    @abstractmethod
    def filter(self, word: str) -> bool:
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class RejectedLetter(Letter):
    def filter(self, word: str) -> bool:
        if self.letter in word:
            return False
        return True
        
    def __str__(self):
        return f'Буквы "{colorcode(self.letter, red_font)}" нет в слове.'
        
class AcceptedLetterWrongPosition(Letter):
    def __init__(self, letter: str, wrong_position: int):
        super().__init__(letter)
        self.wrong_position = wrong_position
        
    def filter(self, word: str) -> bool:
        if self.letter not in word:
            return False
        if word[self.wrong_position - 1] == self.letter:
            return False
        return True

    def __str__(self):
        letter = colorcode(self.letter, yellow_font)
        position = colorcode(self.wrong_position, yellow_font)
        return f'Буква "{letter}" есть в слове, но не на {position}-й позиции.'

class AcceptedLetterCorrectPosition(Letter):
    def __init__(self, letter: str, correct_position: int):
        super().__init__(letter)
        self.correct_position = correct_position
        
    def filter(self, word: str) -> bool:
        if word[self.correct_position - 1] != self.letter:
            return False
        return True
        
    def __str__(self):
        letter = colorcode(self.letter, green_font)
        position = colorcode(self.correct_position, green_font)
        return f'Буква "{letter}" есть в слове на {position}-й позиции.'

def parse_info() -> Optional[Letter]:
    info = input()
    if info.strip() == "":
        return None
    
    # check correctness
    try:
        letter, code = info.split()
    except ValueError:
        raise InputError("Должно быть ровно два значения (буква и код), разделенных пробелом.")
    
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


