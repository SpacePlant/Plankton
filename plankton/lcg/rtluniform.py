from .lcg import LCG


class RtlUniform(LCG):
    def get_info(self):
        return self.PRNGInfo(name='Native API RtlUniform()',
                             s_name='rtluniform',
                             type='Linear Congruential Generator',
                             seed_entropy=31,
                             out_min=0,
                             out_max=(2**31 - 2),
                             req_vals=1,
                             bf_compl=0)

    def get_constants(self):
        return self.LCGConstants(a=0x7FFFFFED,
                                 c=0x7FFFFFC3,
                                 m=2**31 - 1)