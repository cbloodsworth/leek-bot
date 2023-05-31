import datetime

def is_business_hours() -> bool:
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(0, 0)  # 12AM
    end_time = datetime.time(7, 0)  # 7AM

    if start_time <= current_time <= end_time: return True
    else: return False

def seconds_until_7pm():
    now = datetime.datetime.now()
    target = now.replace(hour=23, minute=0, second=0, microsecond=0)
    
    if now.hour >= 23:
        target += datetime.timedelta(days=1)  # Move target to tomorrow if it's already past 7 PM
    
    diff = (target - now).total_seconds()
    return diff

