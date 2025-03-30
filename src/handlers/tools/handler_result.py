# Модуль с результатом работы обработчика

def handler_result(handler, answer):
    return {
        'handler': handler.__name__,
        'module': handler.__module__,
        'answer': answer
    }