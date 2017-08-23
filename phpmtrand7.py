from prng import PRNG
from phpmtrand import PHPmtrand


class PHPmtrand7(PHPmtrand):
    def get_info(self):
        return PRNG.PRNGInfo(name='PHP 7.1+ mt_rand()',
                             s_name='phpmtrand7',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2 ** 31 - 1),
                             req_vals=1248,
                             bf_compl=3)

    def _update(self, value_vector):
        val = (value_vector.current_value & PHPmtrand._HIGH_MASK) | (value_vector.next_value & PHPmtrand._LOW_MASK)
        val >>= 1
        if value_vector.next_value % 2:  # Fixed in PHP 7.1
            val ^= PHPmtrand._XOR_MASK
        return value_vector.period_value ^ val
