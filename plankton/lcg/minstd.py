from .lcg import LCG


class MINSTD(LCG):
    def get_info(self):
        return self.PRNGInfo(name='Minimal Standard',
                             s_name='minstd',
                             type='Linear Congruential Generator',
                             seed_entropy=31,
                             out_min=0,
                             out_max=(2**31 - 2),
                             req_vals=1,
                             bf_compl=0)

    def get_constants(self):
        return self.LCGConstants(a=16807,
                                 c=0,
                                 m=2**31 - 1)
