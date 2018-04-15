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

        # Brute-force the truncated bits.
        truncated_bits = self._get_truncated_bits()
        reguired_values = self.get_info().req_vals
        for i in range(2**truncated_bits):
            self._state = (vals[0] << truncated_bits) | i
            for val in vals[1:reguired_values]:
                # Candidate did not match.
                if self.next() != val:
                    break
            # Candidate did match.
            else:
                self._verify_output(vals[reguired_values:])
                return

        raise ValueMismatchException()
