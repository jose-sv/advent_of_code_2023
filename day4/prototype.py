#!/usr/bin/env python3
""" My solution for day 4 of advent of code 2023! """
from tqdm import tqdm
from loguru import logger


class Card:
    def __init__(self, _card: str):
        self.original_card = _card
        self.parse(_card)

        self.count()

    def count(self):
        """Count the number of winning values!"""
        self.win_count = 0
        win_nums = []
        for val in self.exist:
            if self.winning[val] == 1:
                logger.debug(f"{val} is a winning number")
                win_nums.append(val)
                self.win_count += 1

        logger.info(
            f"Card {self.card_id} has {self.win_count} winning numbers! ({win_nums})"
        )

    def parse(self, _card: str):
        """Interpret the card str"""
        self.card_id = 0
        self.exist = []
        # name, winning, found = 0, [], []
        self.winning = [0] * 999  # each spot denotes a number; max = 999
        # to_process = [winning, found]
        processing = 0
        current_val = ""

        for _char in _card[4:]:
            logger.debug(f"start: {current_val} + {_char}")

            if _char == " ":  # terminate and skip
                if current_val != "":
                    if processing == 0:
                        self.winning[int(current_val)] = 1
                    else:
                        self.exist.append(int(current_val))

                current_val = ""
                continue

            if _char == ":":  # end of name
                self.card_id = int(current_val)  # strip ':'
                current_val = ""
                logger.debug(f"set name to {self.card_id}")
                continue

            if _char == "|":  # switch from winning to exist
                processing = 1
                logger.debug("End of winning")
                continue

            current_val += _char

            logger.debug(f"end: {current_val}")

        # 'if' not necessary unless input has trailing space...
        # if current_val != "":
        self.exist.append(int(current_val))

        logger.debug(f"{self.card_id}, {self.winning}, {self.exist}")


if __name__ == "__main__":
    # TODO make argument
    with open("input.txt") as in_f:
        for _card in in_f:
            Card(_card)
