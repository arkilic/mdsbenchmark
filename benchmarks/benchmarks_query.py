__author__ = 'arkilic'
import numpy as np
import metadatastore
import metadatastore.api as mdsc


class Suite:
    def setup(self, n):
        metadatastore.conf.mds_config['database'] = 'benchmark'
        metadatastore.conf.mds_config['host'] = '127.0.0.1'
        metadatastore.conf.mds_config['port'] = 2898
