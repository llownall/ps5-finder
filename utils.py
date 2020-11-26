def get_minute_ending(value):
    if 5 <= value % 100 <= 20:
        return 'минут'
    elif value % 10 == 1:
        return 'минута'
    elif 2 <= value % 10 <= 4:
        return 'минуты'
    else:
        return 'минут'


def get_hour_ending(value):
    if 5 <= value % 100 <= 20:
        return 'часов'
    elif value % 10 == 1:
        return 'час'
    elif 2 <= value % 10 <= 4:
        return 'часа'
    else:
        return 'часов'


def get_human_time(duration):
    if duration.seconds < 60:
        return 'меньше минуты'
    elif duration.seconds < 3600:
        minutes = duration.seconds // 60
        return f'{minutes} {get_minute_ending(minutes)}'
    else:
        hours = duration.seconds // 3600
        minutes = (duration.seconds - hours * 3600) // 60
        return f'{hours} {get_hour_ending(hours)} {minutes} {get_minute_ending(minutes)}'
