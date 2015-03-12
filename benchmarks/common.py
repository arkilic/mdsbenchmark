import uuid
from metadatastore import conf


def setup_db():
    db_name = 'benchmark-{0}'.format(str(uuid.uuid4()))
    conf.connection_config['database'] = db_name
    conf.connection_config['host'] = 'localhost'
    conf.connection_config['port'] = 27017
