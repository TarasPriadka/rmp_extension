from logging.config import dictConfig
import logging

logging_config = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
}

def get_logger():
    '''
    Function to unify all logging configs
    '''
    dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger