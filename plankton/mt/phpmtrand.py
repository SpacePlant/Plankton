from .phpmtrand7 import PHPmtrand7


class PHPmtrand(PHPmtrand7):
    def get_info(self):
        return self.PRNGInfo(name='PHP mt_rand()',
                             s_name='phpmtrand',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2**31 - 1),
                             req_vals=1248,
                             bf_compl=3)

    def _update(self, value_vector):
        val = (value_vector.current_value & self._MASK_HIGH) | (value_vector.next_value & self._MASK_LOW)
        val >>= 1
        if value_vector.current_value % 2:  # PHP implementation differs from MT19937
            val ^= self._XOR_MASK
        return value_vector.period_value ^ val
