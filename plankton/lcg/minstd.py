from .lcg import LCG


class MINSTD(LCG):
    def get_info(self):
        return self.PRNGInfo(name='Minimal Standard',
                             s_name='minstd',
                             type='Linear Congruential Generator',
                             seed_size=31,
                             out_range=2**31 - 1,
                             req_vals=1,
                             bf_compl=0)

    def _get_constants(self):
        return self.LCGConstants(a=16807,
                                 c=0,
                                 m=2**31 - 1)
