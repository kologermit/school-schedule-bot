from copy import deepcopy

from modules import b

class UpdateResult:
    count_subscribers: int
    count_lessons: int
    def __init__(self, count_subscribers: int, count_lessons: int):
        self.count_subscribers = deepcopy(count_subscribers)
        self.count_lessons = deepcopy(count_lessons)
    def results_to_text(name: str, results: dict[str, any]) -> str:
        return (
            b(f'Отчёт по рассылке {name}:\n')
            +'\n'.join(f'- {student_class} - Уроков: {result.count_lessons} - Подписок: {result.count_subscribers}' 
                for student_class, result in results.items())
        )