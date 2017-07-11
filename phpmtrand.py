from collections import namedtuple
from prng import PRNG, ValueMismatchException


class PHPmtrand(PRNG):
    _ValueVector = namedtuple('ValueVector', ['current_value', 'next_value', 'period_value'])

    _STATE_SIZE = 624							# n (MT19937 constant)
    _PERIOD = 397								# m (MT19937 constant)

    _INITIALIZATION_MULTIPLIER = 0x6C078965		# f (MT19937 constant)
    _WORD_SHIFT = 30							# w - 2 (MT19937 constant)

    _XOR_MASK = 0x9908B0DF						# a (MT19937 constant)

    _BITSHIFT_1 = 11							# u (MT19937 constant)
    _BITSHIFT_2 = 7								# s (MT19937 constant)
    _BITSHIFT_3 = 15							# t (MT19937 constant)
    _BITSHIFT_4 = 18							# l (MT19937 constant)

    _BITMASK_1 = 0x9D2C5680						# b (MT19937 constant)
    _BITMASK_2 = 0xEFC60000						# c (MT19937 constant)

    _MASK = 0xFFFFFFFF							# Bit 0 to 31
    _HIGH_MASK = 0x80000000						# Bit 31
    _LOW_MASK = 0x7FFFFFFF						# Bit 0 to 30

    def __init__(self):
        self._seeded = False
        self._state = [0 for _ in range(PHPmtrand._STATE_SIZE)]
        self._index = PHPmtrand._STATE_SIZE

    def get_info(self):
        return PRNG.PRNGInfo(name='PHP mt_rand()',
                             s_name='phpmtrand',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2 ** 31 - 1),
                             req_vals=1248,
                             bf_compl=3)

    # Calculates new value in current state based on values in previous state.
    def _update(self, value_vector):
        val = (value_vector.current_value & PHPmtrand._HIGH_MASK) | (value_vector.next_value & PHPmtrand._LOW_MASK)
        val >>= 1
        if value_vector.current_value % 2:  # PHP implementation differs from MT19937
            val ^= PHPmtrand._XOR_MASK
        return value_vector.period_value ^ val

    # Updates the internal state.
    def _reload(self):
        for current_index in range(PHPmtrand._STATE_SIZE):
            next_index = (current_index + 1) % PHPmtrand._STATE_SIZE
            period_index = (current_index + PHPmtrand._PERIOD) % PHPmtrand._STATE_SIZE

            current_value = self._state[current_index]
            next_value = self._state[next_index]
            period_value = self._state[period_index]

            self._state[current_index] = self._update(PHPmtrand._ValueVector(current_value, next_value, period_value))

        self._index = 0

    def _recover_state(self, vals, verification):
        self._state = [0 for _ in range(PHPmtrand._STATE_SIZE)]

        for current_index in range(PHPmtrand._STATE_SIZE):
            next_index = (current_index + 1) % PHPmtrand._STATE_SIZE
            period_index = (current_index + PHPmtrand._PERIOD) % PHPmtrand._STATE_SIZE

            # Calculate new value based on all different combinations of old values.
            value_combinations = [PHPmtrand._ValueVector(current_value, next_value, period_value)
                                  for current_value in vals[current_index]
                                  for next_value in vals[next_index]
                                  for period_value in vals[period_index]]

            vals[current_index].clear()
            for value_vector in value_combinations:
                result = self._update(value_vector)

                # The correct original value was determined.
                if self._tamper(result) == verification[current_index]:
                    vals[current_index].add(result)
                    self._state[current_index] = value_vector.current_value

            # The correct original value was not determined.
            if not self._state[current_index]:
                raise ValueMismatchException()

    # Tampers a value from the internal state.
    def _tamper(self, val):
        val ^= val >> PHPmtrand._BITSHIFT_1
        val ^= (val << PHPmtrand._BITSHIFT_2) & PHPmtrand._BITMASK_1
        val ^= (val << PHPmtrand._BITSHIFT_3) & PHPmtrand._BITMASK_2
        val ^= val >> PHPmtrand._BITSHIFT_4
        return val >> 1  # Destroy LSB

    # Reverses the tamper operation.
    def _reverse_tamper(self, val):
        results = set()
        for valx in [val << 1, (val << 1) + 1]:  # LSB can be 0 or 1
            valx ^= valx >> PHPmtrand._BITSHIFT_4
            valx ^= (valx << PHPmtrand._BITSHIFT_3) & PHPmtrand._BITMASK_2
            valx ^= (valx << PHPmtrand._BITSHIFT_2) & PHPmtrand._BITMASK_1 & (0b1111111 << 7)
            valx ^= (valx << PHPmtrand._BITSHIFT_2) & PHPmtrand._BITMASK_1 & (0b1111111 << 14)
            valx ^= (valx << PHPmtrand._BITSHIFT_2) & PHPmtrand._BITMASK_1 & (0b1111111 << 21)
            valx ^= (valx << PHPmtrand._BITSHIFT_2) & PHPmtrand._BITMASK_1 & (0b1111 << 28)
            valx ^= (valx >> PHPmtrand._BITSHIFT_1) & (0b11111111111 << 10)
            valx ^= (valx >> PHPmtrand._BITSHIFT_1) & 0b1111111111
            results.add(valx)
        return results

    def seed(self, val):
        self._state[0] = val & PHPmtrand._MASK
        for i in range(1, PHPmtrand._STATE_SIZE):
            self._state[i] = (PHPmtrand._INITIALIZATION_MULTIPLIER * (
                self._state[i - 1] ^ (self._state[i - 1] >> PHPmtrand._WORD_SHIFT)) + i) & PHPmtrand._MASK

        self._seeded = True

    def next(self):
        if not self._seeded:
            self.seed(PRNG._DEFAULT_SEED)

        if self._index >= PHPmtrand._STATE_SIZE:
            self._reload()

        result = self._tamper(self._state[self._index])

        self._index += 1
        return result

    def recover(self, vals):
        self._verify_input(vals)

        reversed_state = []
        for val in vals[:PHPmtrand._STATE_SIZE]:
            reversed_state.append(self._reverse_tamper(val))

        self._recover_state(reversed_state, vals[PHPmtrand._STATE_SIZE:])

        self._reload()
        self._reload()

        self._seeded = True

        self._verify_output(vals[PHPmtrand._STATE_SIZE * 2:])
