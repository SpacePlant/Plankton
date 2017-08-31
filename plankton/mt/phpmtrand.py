from ..prng import ValueMismatchException
from .mt19937 import MT19937


class PHPmtrand(MT19937):
    def get_info(self):
        return self.PRNGInfo(name='PHP mt_rand()',
                             s_name='phpmtrand',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2 ** 31 - 1),
                             req_vals=1248,
                             bf_compl=3)

    # Calculates new value in current state based on values in previous state.
    def _update(self, value_vector):
        val = (value_vector.current_value & self._MASK_HIGH) | (value_vector.next_value & self._MASK_LOW)
        val >>= 1
        if value_vector.current_value % 2:  # PHP implementation differs from MT19937
            val ^= self._XOR_MASK
        return value_vector.period_value ^ val

    # Recovers the internal state from output.
    def _recover_state(self, vals, verification):
        self._state = [0 for _ in range(self._STATE_SIZE)]

        for current_index in range(self._STATE_SIZE):
            next_index = (current_index + 1) % self._STATE_SIZE
            period_index = (current_index + self._PERIOD) % self._STATE_SIZE

            # Calculate new value based on all different combinations of old values.
            value_combinations = [self._ValueVector(current_value, next_value, period_value)
                                  for current_value in vals[current_index]
                                  for next_value in vals[next_index]
                                  for period_value in vals[period_index]]

            vals[current_index].clear()
            vals[next_index].clear()
            vals[period_index].clear()
            for value_vector in value_combinations:
                result = self._update(value_vector)

                # A possible original value was determined.
                if self._temper(result) == verification[current_index]:
                    vals[current_index].add(result)
                    vals[next_index].add(value_vector.next_value)
                    vals[period_index].add(value_vector.period_value)
                    self._state[current_index] = value_vector.current_value

            # No possible original value was determined.
            if not vals[current_index]:
                raise ValueMismatchException()

    # Tempers a value from the internal state.
    def _temper(self, val):
        return super()._temper(val) >> 1  # Destroy LSB

    # Reverses the temper operation.
    def _reverse_temper(self, val):
        results = set()
        for valx in [val << 1, (val << 1) + 1]:  # LSB can be 0 or 1
            results.add(super()._reverse_temper(valx))
        return results

    def recover(self, vals):
        self._verify_input(vals)

        reversed_state = []
        for val in vals[:self._STATE_SIZE]:
            reversed_state.append(self._reverse_temper(val))

        self._recover_state(reversed_state, vals[self._STATE_SIZE:self._STATE_SIZE * 2])

        self._reload()
        self._reload()

        self._seeded = True

        self._verify_output(vals[self._STATE_SIZE * 2:])
