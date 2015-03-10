__author__ = 'arkilic'
import uuid
import numpy as np
import metadatastore
import metadatastore.api as mdsc


EVENT_COUNT = 1000
# I have event count so that
# tests do not take forever during
# development. I will get rid off
# this, bear with me.


class Suite:
    params = [1, 10, 100, 1000]

    def setup(self, n):
        metadatastore.conf.connection_config['database'] = 'benchmark-{0}'.format(str(uuid.uuid4()))
        metadatastore.conf.connection_config['host'] = 'localhost'
        metadatastore.conf.connection_config['port'] = 12701
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
        # Compose event data list for 1mil events in setup.
        # See params in event insert test to see how many of these are used
        func = np.cos
        num = EVENT_COUNT
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

    def time_event_insert(self, n):
        j = 0
        for i in range(n):
            e = mdsc.insert_event(event_descriptor=self.e_desc,
                                  seq_num=j,
                                  time=1315315135.5135,
                                  data=self.data[i])
            j += 1
    time_event_insert.number = 1
    time_event_insert.repeat = 1
    time_event_insert.params = [1, 10, 100, EVENT_COUNT]
    # override class gloabal params

    def time_1K_header_100_events(self, n):
        pass

    def time_1K_header_1K_events(self, n):
        pass

    def time_1K_header_1mil_events(self, n):
        pass

    def time_1k_header_3mil_events(self, n):
        pass
