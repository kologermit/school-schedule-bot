def dz(a: str, b: str): return dict(zip(a, b))

class WeekdayEnum:
    
    MONDAY =    'MONDAY'
    TUESDAY =   'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY =  'THURSDAY'
    FRIDAY =    'FRIDAY'
    SATURDAY =  'SATURDAY'
    ALL_DAYS =  'ALL DAYS'
    
    RUS_MONDAY =    'ПОНЕДЕЛЬНИК'
    RUS_TUESDAY =   'ВТОРНИК'
    RUS_WEDNESDAY = 'СРЕДА'
    RUS_THURSDAY =  'ЧЕТВЕРГ'
    RUS_FRIDAY =    'ПЯТНИЦА'
    RUS_SATURDAY =  'СУББОТА'
    RUS_ALL_DAYS =  'ВСЯ НЕДЕЛЯ'
    
    list = [MONDAY , TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, ALL_DAYS]
    list_rus = [
        RUS_MONDAY, RUS_TUESDAY, RUS_WEDNESDAY, 
        RUS_THURSDAY, RUS_FRIDAY, RUS_SATURDAY, 
        RUS_ALL_DAYS
    ]
    dict = {
        **dz(('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'), list),
        **dz(list_rus, list),
        **dz([str(i) for i in range(1, 7)], list),
        **dz(list, list),
    }
    dict_rus = dz(list, list_rus)