def make_readable(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


print(make_readable(10))