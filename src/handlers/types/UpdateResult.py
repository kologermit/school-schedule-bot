from copy import deepcopy

class UpdateResult:
    count_subscribers: int
    count_lessons: int
    def __init__(self, count_subscribers: int, count_lessons: int):
        self.count_subscribers = deepcopy(count_subscribers)
        self.count_lessons = deepcopy(count_lessons)
        