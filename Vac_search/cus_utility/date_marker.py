from datetime import datetime as _dt

_DATETIME_STR_FORMAT = '%Y.%m.%d - %H:%M'


def datestamp() -> str:
    return _dt.strftime(_dt.now(), _DATETIME_STR_FORMAT)


if __name__ == '__main__':
    pass
