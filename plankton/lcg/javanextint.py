from .lcgtruncated import LCGTruncated


class JavaNextInt(LCGTruncated):
    def get_info(self):
        return self.PRNGInfo(name='Java Random nextInt()',
                             s_name='javanextint',
                             type='Linear Congruential Generator',
                             seed_entropy=48,
                             out_range=2**32,
                             req_vals=2,
                             bf_compl=16)

    def _get_constants(self):
        return self.LCGConstants(a=0x5DEECE66D,
                                 c=0xB,
                                 m=2**48)

    def _get_truncated_bits(self):
        return 16

    def seed(self, val):
        self._state = (val ^ self._get_constants().a) % self._get_constants().m
