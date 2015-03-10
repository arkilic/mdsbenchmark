import numpy as np
from metadatastore.api import *
from .common import setup_db


class Suite:
    def setup(self, n):
        setup_db()
