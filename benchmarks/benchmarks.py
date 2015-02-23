# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import metadatastore
import metadatastore.api as mdsc
import time as ttime


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """
    def setup(self):
        metadatastore.conf.mds_config['database'] = 'benchmark'
        metadatastore.conf.mds_config['host'] = '127.0.0.1'
        metadatastore.conf.mds_config['port'] = 27017
        self.config_iters = 1000
        self.bcfg_time = ttime.time()
        self.bcfg_params = {'param1': 'value1',
                            'param2': 'value2'}

    def time_keys(self):
        for _ in xrange(self.config_iters):
            mdsc.insert_beamline_config(time=self.bcfg_time,
                                        config_params=self.bcfg_params)

    def time_iterkeys(self):
        for key in self.d.iterkeys():
            pass

    def time_range(self):
        d = self.d
        for key in range(500):
            x = d[key]

    def time_xrange(self):
        d = self.d
        for key in xrange(500):
            x = d[key]


class MemSuite:
    def mem_list(self):
        return [0] * 256
