from loguru import logger
from modules import wait_next_day
from modules import send_to_admin
from models import TeacherSchedule, Teacher
from models import WeekdayEnum, ScheduleTypeEnum
from config import BOT_ADMINS
from dispatcher import bot_sync


async def init():
    while True:
        yesterday, today = await wait_next_day('remove_teacher_schedule')
        weekday = WeekdayEnum.dict[str(yesterday.weekday())]
        weekday_rus = WeekdayEnum.dict_rus[weekday]
        schedule_filter = TeacherSchedule.filter(
            deleted__isnull=True,
            weekday=weekday,
            type=ScheduleTypeEnum.EDITED,
        )
        teacher_ids = list(map(lambda s: s.teacher_id, await schedule_filter))
        teachers = await Teacher.filter(id__in=teacher_ids)
        logger.info({'event': 'REMOVE_TEACHER_SCHEDULE', 'teachers': teachers})
        send_to_admin(f'Удаление расписания учителей {weekday_rus.lower()}', bot_sync, BOT_ADMINS)
        await schedule_filter.update(deleted=today)