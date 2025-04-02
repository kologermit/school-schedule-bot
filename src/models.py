# Модуль моделей БД

# Встроенные модули
from datetime import datetime as DateTime, date as Date, time as Time

# Внешние модули
from tortoise.models import Model
from tortoise import fields as ORMField

Bool = bool

# Часто встречающиеся типы. Класс используется только для создания моделей
class CommonFields:
    id: int =                       ORMField.BigIntField(pk=True, null=False)
    string: str =                   ORMField.CharField(max_length=1000, null=False)
    string_or_null: str|None=       ORMField.CharField(max_length=1000, null=True)
    created: DateTime =             ORMField.DatetimeField(auto_now=True, null=False)
    date: Date =                    ORMField.DateField(null=False)
    date_or_null: Date|None =       ORMField.DateField(null=False)
    datetime: DateTime =            ORMField.DatetimeField(null=False)
    datetime_or_null: DateTime|None=ORMField.DatetimeField(null=True)
    time: Time =                    ORMField.TimeField(null=False)
    time_or_null: Time|None =       ORMField.TimeDeltaField(null=True)
    json: any =                     ORMField.JSONField(null=False)
    json_or_null: any =        ORMField.JSONField(null=True)
    number: int =                   ORMField.BigIntField(null=False)
    number_or_null: int|None =      ORMField.BigIntField(null=True)
    bool: Bool =                    ORMField.BooleanField(null=False)
    bool_or_null: Bool|None =       ORMField.BooleanField(null=True)
    text: str =                     ORMField.TextField(null=False)
    text_or_null: str|None =        ORMField.TextField(null=True)
    user =          ORMField.ForeignKeyField('models.User', null=False)
    message =       ORMField.ForeignKeyField('models.Message', null=False)
    student_class = ORMField.ForeignKeyField('models.StudentClass', null=False)
    teacher =       ORMField.ForeignKeyField('models.Teacher', null=False)


# Модель пользователя
class User(Model):
    id =            CommonFields.id
    name =          CommonFields.string
    screen =        ORMField.CharField(null=False, default='start', max_length=1000)
    tmp_data =      CommonFields.json_or_null
    created =       CommonFields.created
    
# Модель сообщения
class Message(Model):
    created =       CommonFields.created
    user =          CommonFields.user
    text =          CommonFields.text_or_null
    document =      CommonFields.string_or_null
    unique_together = ("id", "user")
    
# Модель присланных документов в сообщениях
# Нужно только для документов с раписанием
class Document(Model):
    created =       CommonFields.created
    file_id =       CommonFields.string
    name =          CommonFields.string
    message =       CommonFields.message
    user =          CommonFields.user
    path =          CommonFields.string
    
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
        **dz([str(i) for i in range(7)], list),
        **dz(list, list),
    }
    dict_rus = dz(list, list_rus)    
    
# Модель класса
class StudentClass(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    parallel =      CommonFields.number
    symbol =        CommonFields.string
    def __str__(self):
        return f'{self.parallel}{self.symbol}'
    def __repr__(self):
        return f'<StuidentClass: id:{self.id} name:{self}>'
    
# Модель расписания класса
class StudentClassSchedule(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    student_class = CommonFields.student_class
    weekday =       CommonFields.string
    data =          CommonFields.json
    type =          CommonFields.string
 
# Модель рассылки расписания класса   
class StudentClassSubscribe(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    student_class = CommonFields.student_class
    user =          CommonFields.user
    
# Модель учителя
class Teacher(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    surname =       CommonFields.string
    initials =      CommonFields.string
    def __str__(self):
        return f'{self.surname} {self.initials}'
    def __repr__(self):
        return '<Teacher id:{self.id} name:{self}>'
    
# Модель расписания учителя
class TeacherSchedule(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    teacher =       CommonFields.teacher
    weekday =       CommonFields.string
    data =          CommonFields.json
    type =          CommonFields.string
    
# Модель рассылки расписания учителя
class TeacherSubscribe(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    teacher =       CommonFields.teacher
    user =          CommonFields.user
    
# Можель расписания звонков
class Ring(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    start =         CommonFields.time
    end =           CommonFields.time
    
# Модель каникул   
class Holiday(Model):
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    is_holiday =    CommonFields.bool
    summary =       CommonFields.string