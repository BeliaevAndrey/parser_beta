import logging

FILE = 'grabbing.log'
FORMAT = '{asctime} - {levelname}: {msg}'

logging.basicConfig(filename=FILE, filemode='w', format=FORMAT,
                    style='{', level=logging.NOTSET
                    )
logger = logging.getLogger(__name__)
