from loguru import logger
from modules import wait_next_day
from modules import send_to_admin
from models import StudentClassSchedule, StudentClass
from models import WeekdayEnum, ScheduleTypeEnum
from config import BOT_ADMINS
from dispatcher import bot_sync


async def init():
    while True:
        yesterday, today = await wait_next_day('remove_student_class_schedule')
        weekday = WeekdayEnum.dict[str(yesterday.weekday())]
        weekday_rus = WeekdayEnum.dict_rus[weekday]
        schedule_filter = StudentClassSchedule.filter_all(weekday=weekday,type=ScheduleTypeEnum.EDITED)
        schedule_studentt_class_ids = list(map(lambda s: s.student_class_id, await schedule_filter))
        student_classes = await StudentClass.filter_all(id__in=schedule_studentt_class_ids)
        logger.info({'event': 'REMOVE_STUDENT_CLASS_SCHEDULE', 'classes': student_classes})
        send_to_admin(f'Удаление расписания учеников {weekday_rus.lower()}', bot_sync, BOT_ADMINS)
        await schedule_filter.update(deleted=today)