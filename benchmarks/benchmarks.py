# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import metadatastore
import metadatastore.api as mdsc



class Suite:
    
    params = [1, 10, 100, 1000, 10000, 100000]
    def setup(self, n):
        metadatastore.conf.mds_config['database'] = 'benchmark'
        metadatastore.conf.mds_config['host'] = '127.0.0.1'
        metadatastore.conf.mds_config['port'] = 2898
        self.obj = range(n)
    
    def time_bcfg(self, n):
        for _ in self.obj:
            mdsc.insert_beamline_config(time=1315315135.5135,
                                        config_params={'param1': 1})
    time_bcfg.number = 1
    time_bcfg.repeat = 1
