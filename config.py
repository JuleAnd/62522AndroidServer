import os
__author__ = 'jacobgilsaa'


__VERSION__ = "1.0.0"
__CONFIGURATIONS__ = {
    'DEBUG': 'True',
    'BASE_DIR': os.path.abspath(os.path.dirname(__file__)),
    'THREADS_PER_PAGE': 2,
    'SECRET_KEY': os.urandom(24),
    'MONGODB_SETTINGS': {
        'DB': 'test',
        'host': 'localhost',
        'port': 27017
    }
}