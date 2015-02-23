# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import metadatastore
import metadatastore.api as mdsc


class Suite:
    params = [1, 10, 100, 1000]

    def setup(self, n):
        metadatastore.conf.mds_config['database'] = 'benchmark'
        metadatastore.conf.mds_config['host'] = '127.0.0.1'
        metadatastore.conf.mds_config['port'] = 2898
        self.obj = range(n)
        self.bcfg = mdsc.insert_beamline_config(time=1315315135.5135,
                                                config_params={'param1': 1})
        self.data_keys = {'linear_motor': {'source': 'PV:pv1',
                                           'shape': None,
                                           'dtype': 'number'},
                          'scalar_detector': {'source': 'PV:pv2',
                                              'shape': None,
                                              'dtype': 'number'},
                          'Tsam': {'source': 'PV:pv3',
                                   'dtype': 'number',
                                   'shape': None}}
        self.custom = {'custom_key': 'value'}
        self.scan_id = 1903

    def time_single_bcfg(self, n):
        for _ in self.obj:
            mdsc.insert_beamline_config(time=1315315135.5135,
                                        config_params={'param1': 1})
    time_single_bcfg.number = 1
    time_single_bcfg.repeat = 1

    def time_single_runstart(self, n):
        for _ in self.obj:
            rs = mdsc.insert_run_start(scan_id=int(self.scan_id),
                                       beamline_id='benchmark_b',
                                       time=1315315135.5135,
                                       beamline_config=self.bcfg,
                                       custom=self.custom)
    time_single_runstart.number = 1
    time_single_runstart.repeat = 1
