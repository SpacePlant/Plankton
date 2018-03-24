from ..prng import ValueMismatchException
from .lcg import LCG


class LCGTruncated(LCG):
    # Returns the amount of bits truncated
    def _get_truncated_bits(self):
        pass

    def next(self):
        return super().next() >> self._get_truncated_bits()

    def recover(self, vals):
        self._verify_input(vals)

        truncated_bits = self._get_truncated_bits()
        for i in range(2**truncated_bits):
            self._state = (vals[0] << truncated_bits) | i
            if self.next() == vals[1]:
                self._verify_output(vals[2:])
                return

        raise ValueMismatchException()
