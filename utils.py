import datetime

def needs_sleep(limit_remaining,limit_reset):
    if limit_remaining <= 1:
        reset_time = datetime.datetime.fromtimestamp(float(limit_reset))
        now = datetime.datetime.now()
        seconds_to_sleep = (reset_time - now).seconds
        return seconds_to_sleep
    return False