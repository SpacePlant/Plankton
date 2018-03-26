from .lcgtruncated import LCGTruncated


class MicrosoftRand(LCGTruncated):
    def get_info(self):
        return self.PRNGInfo(name='Microsoft rand()',
                             s_name='microsoftrand',
                             type='Linear Congruential Generator',
                             seed_entropy=31,
                             out_range=2**15,
                             req_vals=3,
                             bf_compl=16)

    def _get_constants(self):
        return self.LCGConstants(a=214013,
                                 c=2531011,
                                 m=2**31)

    def _get_truncated_bits(self):
        return 16
