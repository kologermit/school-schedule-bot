# Модуль моделей БД

# Внешние модули
from tortoise.models import Model
from tortoise import fields as ORMField

# Часто встречающиеся типы. Класс используется только для создания моделей
class CommonFields:
    id =            ORMField.BigIntField(pk=True, null=False)
    string =        ORMField.CharField(max_length=1000, null=False)
    string_or_null= ORMField.CharField(max_length=1000, null=True)
    created =       ORMField.DatetimeField(auto_now=True, null=False)
    date =          ORMField.DateField(null=False)
    date_or_null =  ORMField.DateField(null=False)
    datetime =      ORMField.DatetimeField(null=False)
    time =          ORMField.TimeField(null=False)
    time_or_null =  ORMField.TimeDeltaField(null=True)
    json =          ORMField.JSONField(null=False)
    json_or_null =  ORMField.JSONField(null=True)
    datetime_or_null=ORMField.DatetimeField(null=True)
    number =        ORMField.BigIntField(null=False)
    number_or_null =ORMField.BigIntField(null=True)
    bool =          ORMField.BooleanField(null=False)
    bool_or_null =  ORMField.BooleanField(null=True)
    text =          ORMField.TextField(null=False)
    text_or_null =  ORMField.TextField(null=True)
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
    id =            CommonFields.id
    created =       CommonFields.created
    user =          CommonFields.user
    text =          CommonFields.text_or_null
    document =      CommonFields.string_or_null
    
# Модель присланных документов в сообщениях
# Нужно только для документов с раписанием
class Document(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    file_id =       CommonFields.string
    name =          CommonFields.string
    message =       CommonFields.message
    user =          CommonFields.user
    data =          CommonFields.json_or_null
    
# Модель класса
class StudentClass(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    parallel =      CommonFields.number
    symbol =        CommonFields.string
    
# Модель расписания класса
class StudentClassSchedule(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    student_class = CommonFields.student_class
    day =           CommonFields.string
    standart =      CommonFields.json
    edited =        CommonFields.json_or_null
 
# Модель рассылки расписания класса   
class StudentClassSubscribe(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    student_class = CommonFields.student_class
    user =          CommonFields.user
    
# Модель учителя
class Teacher(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    surname =       CommonFields.string
    initials =      CommonFields.string
    
# Модель расписания учителя
class TeacherSchedule(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    surname =       CommonFields.string
    initials =      CommonFields.string
    
# Модель рассылки расписания учителя
class TeacherSubscribe(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    teacher =       CommonFields.teacher
    user =          CommonFields.user
    
# Можель расписания звонков
class Ring(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    start =         CommonFields.time
    end =           CommonFields.time
    
# Модель каникул   
class Holiday(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    is_holiday =    CommonFields.bool
    is_weekend =    CommonFields.bool
    summary =       CommonFields.string