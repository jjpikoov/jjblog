class ProductionConfig(object):
    """Config of whole application in production"""
    DEBUG = False
    TESTING = False
    DATABASE = ''  # set sqlite db file you want
    SECRET_KEY = ''  # set it really hard to guess
    USERNAME = ''  # master admin username
    PASSWORD = ''  # master admin password


class DevConfig(object):
    """Config of whole application in production"""
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'  # set sqlite db file you want
    SECRET_KEY = 'very_secret_key1'  # set it really hard to guess
    USERNAME = 'admin'  # master admin username
    PASSWORD = 'admin'  # master admin password
