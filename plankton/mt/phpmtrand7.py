from .mt19937 import MT19937
from .phpmtrand import PHPmtrand


class PHPmtrand7(PHPmtrand):
    def get_info(self):
        return self.PRNGInfo(name='PHP 7.1+ mt_rand()',
                             s_name='phpmtrand7',
                             type='Mersenne Twister',
                             seed_entropy=32,
                             out_min=0,
                             out_max=(2 ** 31 - 1),
                             req_vals=1248,
                             bf_compl=3)

    def _update(self, value_vector):
        return MT19937._update(self, value_vector)  # Fixed in PHP 7.1
