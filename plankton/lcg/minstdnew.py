from .lcg import LCG


class MINSTDNew(LCG):
    def get_info(self):
        return self.PRNGInfo(name='Minimal Standard (New)',
                             s_name='minstdnew',
                             type='Linear Congruential Generator',
                             seed_entropy=31,
                             out_min=0,
                             out_max=(2**31 - 2),
                             req_vals=1,
                             bf_compl=0)

    def _get_constants(self):
        return self.LCGConstants(a=48271,
                                 c=0,
                                 m=2**31 - 1)
