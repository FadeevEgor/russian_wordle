from typing import Optional, List

from wordlealgorithm import WordleAlgorithm
from gameinfo import (
    Letter,
    RejectedLetter,
    AcceptedLetterWrongPosition,
    AcceptedLetterCorrectPosition,
    InputError,
)


def print_instruction() -> None:
    """
    Prints instruction to an user.
    """
    with open("user_instruction.txt", encoding="cp1251") as f:
        print(f.read())


def parse_letter(letter, code) -> Letter:
    """
    Parse a letter and a code and returns a Letter instance.
    If input is incorrect, raises an error
    """
    try:
        code = int(code)
    except ValueError:
        raise InputError("The code should be an integer.")

    if code not in range(-5, 6):
        raise InputError("The code should be in range from -5 tо 5.")

    # make an instance of Letter
    if code == 0:
        return RejectedLetter(letter)
    elif code > 0:
        return AcceptedLetterCorrectPosition(letter, code)
    elif code < 0:
        return AcceptedLetterWrongPosition(letter, -code)
    else:
        raise ValueError(f"Not supported code: {code}")


def parse_info() -> Optional[List[Letter]]:
    """
    Parses the info an user typed in.
    Raises an error
    """
    line = input().strip()
    if line == "":
        return None

    tokens = line.split()
    if len(tokens) % 2:
        raise InputError("The number of tokens should be even.")
    return [
        parse_letter(letter, code) for letter, code in zip(tokens[::2], tokens[1::2])
    ]


def interact(guesser: WordleAlgorithm, words_to_show: int) -> None:
    """
    Runs interactive session.
    """
    info: list[Letter] = []
    while True:
        print("=" * 80)
        ranked_guesses = guesser.rank_guesses(info)
        print(
            f"Here is top {words_to_show} most prominent words out of {len(guesser.possible_words)} possible."
        )
        print(ranked_guesses.head(words_to_show).to_string(index=False))
        print_instruction()
        try:
            letters = parse_info()
        except InputError as msg:
            print(msg)
            continue
        if letters is None:
            break

        for l in letters:
            print(l.description())
        info.extend(letters)

    print("Exit.")
