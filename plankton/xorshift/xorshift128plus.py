from z3 import Solver, BitVecs, LShR, sat
from ..prng import PRNG, ValueMismatchException


class Xorshift128Plus(PRNG):
    _BITSHIFT_1 = 23
    _BITSHIFT_2 = 17
    _BITSHIFT_3 = 26

    _MASK = 0xFFFFFFFFFFFFFFFF

    def get_info(self):
        return self.PRNGInfo(name='xorshift128+',
                             s_name='xorshift128+',
                             type='Xorshift',
                             seed_entropy=128,
                             out_range=2**64,
                             req_vals=3,
                             bf_compl=0)

    def __init__(self):
        self._state = [0, 0]
        self.seed(self._DEFAULT_SEED)

    def seed(self, val):
        self._state[0] = val & self._MASK
        self._state[1] = (val >> 64) & self._MASK

    def next(self):
        x = self._state[0]
        y = self._state[1]

        x ^= x << self._BITSHIFT_1 & self._MASK
        x ^= x >> self._BITSHIFT_2
        x ^= y ^ (y >> self._BITSHIFT_3)

        self._state[0] = y
        self._state[1] = x

        return x + y & self._MASK

    def recover(self, vals):
        self._verify_input(vals)

        # Use Z3 solver.
        solver = Solver()

        states = BitVecs('s0 s1', 64)
        outputs = BitVecs('o0 o1 o2', 64)

        # Add output constraints based on given values.
        for val, output in zip(vals, outputs):
            solver.add(output == val)

        # Generate symbolic representations of the next states.
        def next_state(x, y):
            x ^= (x << self._BITSHIFT_1)
            x ^= LShR(x, self._BITSHIFT_2)
            x ^= y ^ LShR(y, self._BITSHIFT_3)
            return x

        for _ in outputs[1:]:
            states.append(next_state(states[-2], states[-1]))

        # Add output constraints based on states.
        for index, output in enumerate(outputs):
            solver.add(output == states[index] + states[index + 1])

        # A satisfiyng model was found.
        if solver.check() == sat:
            model = solver.model()
            self._state[0] = model[states[0]].as_long()
            self._state[1] = model[states[1]].as_long()
        # No satisfiyng model was found.
        else:
            raise ValueMismatchException()

        self._verify_output(vals[1:])
