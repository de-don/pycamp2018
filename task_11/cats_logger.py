import logging.config
import argparse

import cats_mutliprocessing as cats_mutliprocessing
import cats_threading as cats_threading
import cats_futures as cats_futures

config = {
    'version': 1,
    'formatters': {
        'detail': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s '
                      '%(processName)-10s : %(message)s'
        },
        'normal': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s: %(message)s'
        },
        'minimal': {
            'class': 'logging.Formatter',
            'format': '%(name)-15s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detail',
        },
        'file_tmp': {
            'class': 'logging.FileHandler',
            'filename': 'logs/INFO_tmp.log',
            'mode': 'w',
            'formatter': 'normal',
        },
        'file_logs': {
            'class': 'logging.FileHandler',
            'filename': 'logs/WARNING_logs.log',
            'mode': 'w',
            'formatter': 'minimal',
        },
    },
    'loggers': {
        'cats_threading': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'cats_mutliprocessing': {
            'level': 'INFO',
            'handlers': ['file_tmp'],
        },
        'cats_futures': {
            'level': 'WARNING',
            'handlers': ['file_logs'],
        },
        'urllib3.connectionpool': {
            'level': 'DEBUG',
            'handlers': ['file_tmp'],
        },
    },
}
logging.config.dictConfig(config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--loglevel', dest="loglevel",
        choices=['DEBUG', 'INFO', 'WARNING'],
        default='DEBUG',
    )
    levels = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30}
    args = parser.parse_args()
    level = levels[args.loglevel] - 10

    logging.disable(level)

    cats_threading.main()
    cats_mutliprocessing.main()
    cats_futures.main()
