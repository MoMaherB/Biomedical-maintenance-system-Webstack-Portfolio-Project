from datetime import datetime, timedelta


def default_time():
    return datetime.utcnow() + timedelta(hours=2)