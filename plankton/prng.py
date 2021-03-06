from collections import namedtuple


class PRNG:
    PRNGInfo = namedtuple('PRNGInfo', ['name',          # The name of the PRNG
                                       's_name',        # The shortened name of the PRNG
                                       'type',          # The algorithm type
                                       'seed_size',     # The size of the seed (bits)
                                       'out_range',     # The normalized range of the values generated by the PRNG
                                       'req_vals',      # The number of required subsequent values for state recovery
                                       'bf_compl'])     # The complexity of the brute-force for state recovery (bits)

    _DEFAULT_SEED = 12345678

    # Returns a tuple with the PRNG details.
    def get_info(self):
        pass

    # Seeds the RNG.
    def seed(self, val):
        pass

    # Extracts the next set of values from the RNG.
    def next(self):
        pass

    # Recovers the internal state of the RNG from previous output.
    def recover(self, vals):
        pass

    # Verifies input for state recovery.
    def _verify_input(self, vals):
        rng_info = self.get_info()

        if len(vals) < rng_info.req_vals:
            raise NotEnoughValuesException(rng_info.req_vals)

        for val in vals:
            if not 0 <= val < rng_info.out_range:
                raise InvalidValueException(rng_info.out_range)

    # Verifies subsequent output from the PRNG.
    def _verify_output(self, vals):
        for val in vals:
            if val != self.next():
                raise ValueMismatchException()


class NotEnoughValuesException(Exception):
    def __init__(self, req_vals):
        super().__init__(self, 'At least {} values are required to recover the state.'.format(req_vals))


class InvalidValueException(Exception):
    def __init__(self, out_range):
        super().__init__(self, 'Input values have to be in the range [0;{}[.'.format(out_range))


class ValueMismatchException(Exception):
    def __init__(self):
        super().__init__(self, 'Subsequent input does not match subsequent RNG output.')
