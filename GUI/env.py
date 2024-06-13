from pathlib import Path
import sys, os

script_path = os.path.abspath(__file__)                     
directory = os.path.dirname(script_path) # C:\Users\Vlad\Desktop\project_geo2024 - Определяет путь до папки проекта, не трогать

project_folder = os.path.basename(directory)

import getpass

user = getpass.getuser()
users_path, user_path = directory.split(user)[0], user

# Корневая папка Геология
geo_folder = rf'{directory}\data\ГЕО\МЕДЬ'       # Заменить содержимое на свою иерархию 

# Корневая папка Маркшейдерия
mark_folder = rf'{directory}\data\МАРК\МЕДЬ'     # Заменить содержимое на свою иерархию

# Корневая папка Проектирование
proj_folder = rf'{directory}\data\ТЕХН\МЕДЬ'     # Заменить содержимое на свою иерархию

# Корневая папка Другое -- по умолчанию выбран рабочий стол
others_folder = rf"{os.path.join(users_path, user_path, 'Desktop')}"

# Конфигурация GUI 
libs_folder = os.path.join(directory, 'libs')
# Папка с вспомогательными скриптами
tools_folder = os.path.join(directory, 'tools')
# Папка с логами 
logs_folder = os.path.join(directory, 'logs')
# Папка с временными файлами для Micromine
temp_folder = os.path.join(directory, 'temp')
# Папка для сохранения отчетов по БМ                                    
report_folder = os.path.join(temp_folder, 'reports')                # -- Очищается после каждого запуска Отчет по БМ
# Папка для сохранения .xlsx таблиц из отчетов                              
tables_folder = os.path.join(temp_folder, 'tables')                 # -- Очищается после каждого запуска Отчет по БМ

# Триангуляционная БД для временного хранения срезов каркаса        # -- Очищается после каждого запуска Отчет по БМ
slices = os.path.join(temp_folder, 'set.tridb')


