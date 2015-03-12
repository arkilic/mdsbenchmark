from six.moves import range
import numpy as np
from metadatastore.api import *
from .common import setup_db
from dataportal.broker import DataBroker, EventQueue
from dataportal.muxer import DataMuxer


N = 5


class CompareUpdates(object):
    def time_naive_updating(self):
        events = DataBroker.fetch_events(self.header)
        self.dm.append_events(events)

    def time_updating_from_queue(self):
        self.queue.update()
        self.dm.append_events(self.queue.get())


class ScalarUpdate(CompareUpdates):
    def setup(self):
        setup_db()
        blc = insert_beamline_config({}, time=0.)
        rs = insert_run_start(time=0., scan_id=1, beamline_id='_',
                              beamline_config=blc)
        data_keys = {'foo': {'source': '_', 'dtype': 'number'}}
        ev_desc = insert_event_descriptor(run_start=rs, time=0.,
                                          data_keys=data_keys)
        self.header = DataBroker[-1]
        self.queue = EventQueue(self.header)

        for i in range(100*N):
            insert_event(time=float(i), data={'foo': (i, i)},
                         seq_num=i, event_descriptor=ev_desc)
        events = DataBroker.fetch_events(self.header)
        self.dm = DataMuxer.from_events(events)
        self.queue.update()
        self.queue.get()

        # Then add more events, to be retrieved by the benchmarks.
        for i in range(N):
            insert_event(time=float(i), data={'foo': (i, i)},
                         seq_num=i, event_descriptor=ev_desc)


class NonscalarUpdate(CompareUpdates):
    def setup(self):
        setup_db()
        blc = insert_beamline_config({}, time=0.)
        rs = insert_run_start(time=0., scan_id=1, beamline_id='_',
                              beamline_config=blc)
        data_keys = {'foo': {'source': '_', 'dtype': 'number'}}
        ev_desc = insert_event_descriptor(run_start=rs, time=0.,
                                          data_keys=data_keys)
        self.header = DataBroker[-1]
        self.queue = EventQueue(self.header)

        for i in range(100*N):
            insert_event(time=float(i), data={'foo': (i, i)},
                         seq_num=i, event_descriptor=ev_desc)
        events = DataBroker.fetch_events(self.header)
        self.dm = DataMuxer.from_events(events)
        self.queue.update()
        self.queue.get()

        # Then add more events, to be retrieved by the benchmarks.
        for i in range(N):
            insert_event(time=float(i), data={'foo': (i, i)},
                         seq_num=i, event_descriptor=ev_desc)
        
    def time_naive_updating(self):
        events = DataBroker.fetch_events(self.header)
        self.dm.append_events(events)

    def time_updating_from_queue(self):
        self.queue.update()
        self.dm.append_events(self.queue.get())
