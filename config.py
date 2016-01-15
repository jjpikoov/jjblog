class ProductionConfig(object):
    """Config of whole application in production"""
    DEBUG = False
    TESTING = False
    DATABASE = ''  # set sqlite db file you want
    SECRET_KEY = ''  # set it really hard to guess
    USERNAME = ''  # master admin username
    PASSWORD = ''  # master admin password
    BLOG_NAME = ''


class DevConfig(object):
    """Config of whole application in production"""
    DEBUG = True
    TESTING = True
    DATABASE = '/tmp/jjblog'
    SECRET_KEY = 'very_secret_key1'
    USERNAME = 'admin'
    PASSWORD = 'admin'
    BLOG_NAME = "jjpikoov's blog"
