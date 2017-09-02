from collections import namedtuple
from ..prng import PRNG


class LCG(PRNG):
    LCGConstants = namedtuple('LCGConstants', ['a',   # Multiplier
                                               'c',   # Increment
                                               'm'])  # Modulus

    def __init__(self):
        self._state = self._DEFAULT_SEED

    # Returns a tuple with the LCG constants
    def get_constants(self):
        pass

    def seed(self, val):
        self._state = val % self.get_constants().m

    def next(self):
        constants = self.get_constants()
        self._state = (constants.a * self._state + constants.c) % constants.m
        return self._state

    def recover(self, vals):
        self._verify_input(vals)
        self.seed(vals[0])
        self._verify_output(vals[1:])
