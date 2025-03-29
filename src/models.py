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
    schedule =      ORMField.ForeignKeyField('models.Schedule', null=False)


# Модель пользователя
class User(Model):
    id =            CommonFields.id
    name =          CommonFields.string
    screen =        ORMField.CharField(null=False, default='start', max_length=1000)
    tmp_data =      CommonFields.json_or_null
    settings =      CommonFields.json
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
    
# Модель расписания
class Schedule(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    class_symbol =  CommonFields.string_or_null
    class_parallel =CommonFields.number_or_null
    teacher_surname=CommonFields.string_or_null
    teacher_initials=CommonFields.string_or_null
    day =           CommonFields.string
    standart =      CommonFields.json
    edited =        CommonFields.json_or_null
    
# Модель рассылки расписания
class Subscribe(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.created
    user =          CommonFields.user
    schedule =      CommonFields.schedule
    
class Holidays(Model):
    id =            CommonFields.id
    created =       CommonFields.created
    deleted =       CommonFields.datetime_or_null
    is_holiday =    CommonFields.bool
    is_weekend =    CommonFields.bool
    summary =       CommonFields.string