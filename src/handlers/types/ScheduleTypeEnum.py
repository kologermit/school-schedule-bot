class ScheduleTypeEnum:
    STANDART='STANDART'
    EDITED='EDITED'
    
    RUS_STANDART='СТАНДАРТ'
    RUS_EDITED='ИЗМЕНЕНИЯ'
    
    list=[STANDART, EDITED]
    list_rus=[RUS_STANDART, RUS_EDITED]
    dict={
        STANDART: STANDART,
        EDITED: EDITED, 
        RUS_STANDART: STANDART,
        RUS_EDITED: EDITED,
    }
    dict_rus={
        STANDART: RUS_STANDART,
        EDITED: RUS_EDITED
    }