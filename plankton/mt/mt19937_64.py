from .mt19937 import MT19937


class MT19937_64(MT19937):
    _STATE_SIZE = 312                                   # n (MT19937-64 constant)
    _PERIOD = 156                                       # m (MT19937-64 constant)

    _INITIALIZATION_MULTIPLIER = 0x5851F42D4C957F2D     # f (MT19937-64 constant)
    _WORD_SHIFT = 62                                    # w - 2 (MT19937-64 constant)

    _XOR_MASK = 0xB5026F5AA96619E9                      # a (MT19937-64 constant)

    _BITSHIFT_1 = 29                                    # u (MT19937-64 constant)
    _BITSHIFT_2 = 17                                    # s (MT19937-64 constant)
    _BITSHIFT_3 = 37                                    # t (MT19937-64 constant)
    _BITSHIFT_4 = 43                                    # l (MT19937-64 constant)

    _BITMASK_1 = 0x5555555555555555                     # d (MT19937-64 constant)
    _BITMASK_2 = 0x71D67FFFEDA60000                     # b (MT19937-64 constant)
    _BITMASK_3 = 0xFFF7EEE000000000                     # c (MT19937-64 constant)

    _MASK_HIGH = 0xFFFFFFFF80000000                     # Bit 31 to 63
    _MASK_LOW = 0x7FFFFFFF                              # Bit 0 to 30

    def get_info(self):
        return self.PRNGInfo(name='MT19937-64',
                             s_name='mt19937_64',
                             type='Mersenne Twister',
                             seed_entropy=64,
                             out_min=0,
                             out_max=(2 ** 64 - 1),
                             req_vals=312,
                             bf_compl=0)

    def _reverse_temper(self, val):
        val ^= val >> self._BITSHIFT_4
        val ^= (val << self._BITSHIFT_3) & self._BITMASK_3
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b11111111111111111 << 17)
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b11111111111111111 << 34)
        val ^= (val << self._BITSHIFT_2) & self._BITMASK_2 & (0b1111111111111 << 51)
        val ^= (val >> self._BITSHIFT_1) & self._BITMASK_1 & (0b11111111111111111111111111111 << 6)
        val ^= (val >> self._BITSHIFT_1) & self._BITMASK_1 & 0b111111
        return val
