__author__ = 'arkilic'
import numpy as np
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
        self.run_start = mdsc.insert_run_start(scan_id=int(self.scan_id),
                                               owner='benchmark_script',
                                               beamline_id='benchmark_b',
                                               time=1315315135.5135,
                                               beamline_config=self.bcfg,
                                               custom=self.custom)
        self.e_desc = mdsc.insert_event_descriptor(data_keys=self.data_keys,
                                                   time=1315315135.5135,
                                                   run_start=self.run_start)
        func = np.cos
        num = 1000
        start = 0
        stop = 10
        sleep_time = .1
        self.data = list()
        for idx, i in enumerate(np.linspace(start, stop, num)):
            self.data.append({'linear_motor': [i, 1315315135.5135],
                              'Tsam': [i + 5, 1315315135.5135],
                              'scalar_detector': [func(i) +
                                                  np.random.randn() / 100,
                                                  1315315135.5135]})

    def time_single_bcfg(self, n):
        for _ in self.obj:
            mdsc.insert_beamline_config(time=1315315135.5135,
                                        config_params={'param1': 1})
    time_single_bcfg.number = 1
    time_single_bcfg.repeat = 1

    def time_single_runstart(self, n):
        for _ in self.obj:
            mdsc.insert_run_start(scan_id=int(self.scan_id),
                                  beamline_id='benchmark_b',
                                  owner='benchmark_script',
                                  time=1315315135.5135,
                                  beamline_config=self.bcfg,
                                  custom=self.custom)
    time_single_runstart.number = 1
    time_single_runstart.repeat = 1

    def time_single_descriptor(self, n):
        for _ in self.obj:
            mdsc.insert_event_descriptor(data_keys=self.data_keys,
                                         time=1315315135.5135,
                                         run_start=self.run_start)
    time_single_descriptor.number = 1
    time_single_descriptor.repeat = 1

    def time_1K_event_insert(self, n):
        j = 0
        for d in self.data:
            e = mdsc.insert_event(event_descriptor=self.e_desc,
                                  seq_num=j,
                                  time=1315315135.5135,
                                  data=d)
            j += 1
    time_1K_event_insert.number = 1
    time_1K_event_insert.repeat = 1
