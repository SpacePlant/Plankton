from .phpmtrand7 import PHPmtrand7


class PHPmtrand(PHPmtrand7):
    def get_info(self):
        return self.PRNGInfo(name='PHP mt_rand()',
                             s_name='phpmtrand',
                             type='Mersenne Twister',
                             seed_size=32,
                             out_range=2**31,
                             req_vals=1248,
                             bf_compl=3)

    def _update(self, value_vector):
        val = (value_vector.current_value & self._MASK_HIGH) | (value_vector.next_value & self._MASK_LOW)
        val >>= 1
        if value_vector.current_value % 2:  # PHP implementation differs from MT19937
            val ^= self._XOR_MASK
        return value_vector.period_value ^ val
