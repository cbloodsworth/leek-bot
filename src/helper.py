import datetime

def is_business_hours() -> bool:
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(0, 0)  # 12AM
    end_time = datetime.time(7, 0)  # 7AM

    if start_time <= current_time <= end_time: return True
    else: return False
