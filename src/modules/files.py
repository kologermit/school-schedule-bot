# Модуль работы с файламы и папками

# Встроенные модули
from os import makedirs, path, remove

# Процедура создания папки, если таковой нет
def create_dir_if_not_exists(dir: str):
    makedirs(dir, exist_ok=True)
        
# Процедура удаления файла, если таковой имеется
def remove_file_if_exists(file_path: str):
    if path.exists(file_path):
        remove(file_path)