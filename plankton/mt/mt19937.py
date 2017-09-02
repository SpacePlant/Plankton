from collections import namedtuple
from ..prng import PRNG


class MT19937(PRNG):
    _ValueVector = namedtuple('ValueVector', ['current_value', 'next_value', 'period_value'])

    _STATE_SIZE = 624                           # n (MT19937 constant)
    _PERIOD = 397                               # m (MT19937 constant)

    _INITIALIZATION_MULTIPLIER = 0x6C078965     # f (MT19937 constant)
    _WORD_SHIFT = 30                            # w - 2 (MT19937 constant)

    _XOR_MASK = 0x9908B0DF                      # a (MT19937 constant)

    _BITSHIFT_1 = 11                            # u (MT19937 constant)
    _BITSHIFT_2 = 7                             # s (MT19937 constant)
    _BITSHIFT_3 = 15                            # t (MT19937 constant)
    _BITSHIFT_4 = 18                            # l (MT19937 constant)

    _BITMASK_1 = 0xFFFFFFFF                     # d (MT19937 constant)
    _BITMASK_2 = 0x9D2C5680                     # b (MT19937 constant)
    _BITMASK_3 = 0xEFC60000                     # c (MT19937 constant)

    _MASK_HIGH = 0x80000000                     # Bit 31
    _MASK_LOW = 0x7FFFFFFF                      # Bit 0 to 30

    _MODULUS = 2**32

    def __init__(self):
        self._seeded = False
        self._state = [0 for _ in range(self._STATE_SIZE)]
        self._index = self._STATE_SIZE

    def get_info(self):
        return self.PRNGInfo(name='MT19937',
                             s_name='mt19937',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2**32 - 1),
                             req_vals=624,
                             bf_compl=0)

    # Calculates new value in current state based on values in previous state.
    def _update(self, value_vector):
        val = (value_vector.current_value & self._MASK_HIGH) | (value_vector.next_value & self._MASK_LOW)
        val >>= 1
        if value_vector.next_value % 2:
            val ^= self._XOR_MASK
        return value_vector.period_value ^ val

    # Updates the internal state.
    def _reload(self):
        for current_index in range(self._STATE_SIZE):
            next_index = (current_index + 1) % self._STATE_SIZE
            period_index = (current_index + self._PERIOD) % self._STATE_SIZE

            current_value = self._state[current_index]
            next_value = self._state[next_index]
            period_value = self._state[period_index]

            self._state[current_index] = self._update(self._ValueVector(current_value, next_value, period_value))

        self._index = 0

    # Tempers a value from the internal state.
    def _temper(self, val):
        val ^= val >> self._BITSHIFT_1 & self._BITMASK_1
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2
        val ^= (val << self._BITSHIFT_3) & self._BITMASK_3
        val ^= val >> self._BITSHIFT_4
        return val

    # Reverses the temper operation.
    def _reverse_temper(self, val):
        val ^= val >> self._BITSHIFT_4
        val ^= (val << self._BITSHIFT_3) & self._BITMASK_3
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b1111111 << 7)
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b1111111 << 14)
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b1111111 << 21)
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b1111 << 28)
        val ^= (val >> self._BITSHIFT_1) & self._BITMASK_1 & (0b11111111111 << 10)
        val ^= (val >> self._BITSHIFT_1) & self._BITMASK_1 & 0b1111111111
        return val

    def seed(self, val):
        self._state[0] = val % self._MODULUS
        for i in range(1, self._STATE_SIZE):
            self._state[i] = (self._INITIALIZATION_MULTIPLIER * (
                self._state[i - 1] ^ (self._state[i - 1] >> self._WORD_SHIFT)) + i) % self._MODULUS

        self._index = self._STATE_SIZE
        self._seeded = True

    def next(self):
        if not self._seeded:
            self.seed(self._DEFAULT_SEED)

        if self._index >= self._STATE_SIZE:
            self._reload()

        result = self._temper(self._state[self._index])

        self._index += 1
        return result

    def recover(self, vals):
        self._verify_input(vals)

        self._state = [self._reverse_temper(val) for val in vals[:self._STATE_SIZE]]

        self._reload()
        self._seeded = True

        self._verify_output(vals[self._STATE_SIZE:])
