#____________________________________________  Import (START)  _______________________________________________
import os, env              # Импортировать переменные окружения env и модуль os для работы с ними

os.chdir(env.directory)     # Явно назначить папку проекта



import sys
sys.path.insert(0, env.libs_folder)        # добавить в PATH папку libs
sys.path.insert(0, env.tools_folder)       # добавить в PATH папку tools

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

import sqlite3      # Библиотека для работы с встраиваемой СУБД SQLite

# !deprecated 
# import asyncio      # Библиотека для асихронного кода
# Асинхронная загрузка каталогов Геология, Маркшейдерия и Проектирование
# from tools.QTreeWidget.async_loader import async_show_all_tabs, async_show_geo_other_tabs

# !deprecated
# Фильтр событий попавших в Drop 
# from drag_n_drop import CustomEventFilter

from gui.action_window_template import Action_window           # Импорт GUI интерфейса с настроеными анимациями
from gui.styles import btn_style_unactive, btn_style_active    # Импорт стилей для динамических кнопок

# Конфигуратор отображения статистических графиков по каркасу/срезам
from stats import make_stats, restyle_reports

from datetime import datetime

#____________________________________________  Import (END)  _______________________________________________

    
class GUI(Action_window):
    """Инициализирует пользовательский интерфейс"""
    def __init__(self):
        Action_window.__init__(self)

        event_message = f"""
            <br> {'&nbsp;'*8} {datetime.now()} <br>
            {'&nbsp;'*8} Программа запускается в папке проекта: {os.getcwd()}
            """
        self.add_text_to_logs(event_message, error=False)

        
        self.alert_list = []

        # Таймер для автоматической проверки списка алертов alerts_list
        self.timer = QTimer()
        self.timer.setInterval(500)  # Проверка каждые 500 миллисекунд
        self.timer.timeout.connect(self.check_alert_list)
        self.timer.start()

        # Хеш-таблицы для хранения элементов для разных QStandardItemModel
        self.items_dict = {}          # Хранит состояние дерева в контейнере Загрузка данных
        self.items_dict_1 = {}        # Хранит состояние дерева в контейнере Обновление БМ
        self.items_dict_2 = {}        # Хранит состояние дерева в контейнере Перевод БМ
    
        self.active_button = None     # Хранит состояние активной page (Загрузка данных , ...)
        self.active_tab = 0           # Хранит состояние активной tab (Геология , ...)
        
        self.show_content(self.ui.loadData_btn)
        self.get_active_tab(self.active_tab)

        # Бинд кнопок для каждого page (Загрузка данных , ...) на функцию отображения контента этого page 
        self.ui.loadData_btn.clicked.connect(lambda:self.show_content(self.ui.loadData_btn))
        self.ui.loadWells_btn.clicked.connect(lambda:self.show_content(self.ui.loadWells_btn))
        self.ui.updateBM_btn.clicked.connect(lambda:self.show_content(self.ui.updateBM_btn))
        self.ui.reportBM_btn.clicked.connect(lambda:self.show_content(self.ui.reportBM_btn))
        self.ui.transferBM_btn.clicked.connect(lambda:self.show_content(self.ui.transferBM_btn))
        self.ui.logs_btn.clicked.connect(lambda:self.show_content(self.ui.logs_btn))
        self.ui.run_btn.clicked.connect(lambda:self.run_event(self.ui.run_btn))

        self.ui.tabWidget.currentChanged.connect(self.get_active_tab)

        self.ui.geo_tw.start_logging()



    def get_active_tab(self, index):
        self.active_tab = index

        tab_to_log_message = {
            0: f"Выбрана вкладка: Геология",
            1: f"Выбрана вкладка: Маркшейдерия",
            2: f"Выбрана вкладка: Проектирование",
            3: f"Выбрана вкладка: Другое"
        }

        if index in tab_to_log_message:
            event_message = f"""
            <br> {'&nbsp;'*8} {datetime.now()} <br>
            {'&nbsp;'*8} {tab_to_log_message[index]}
            """
            self.add_text_to_logs(event_message, error=False)


    def get_current_container(self):
        """Получить treewidget и хэш-таблицу для текущей вкладки"""
        if self.ui.stackedWidget.currentIndex() == 0:
            treewidget = self.ui.container_treewidget
            items = self.items_dict
        elif self.ui.stackedWidget.currentIndex() == 3:
            treewidget = self.ui.container_treewidget_1
            items = self.items_dict_1
        elif self.ui.stackedWidget.currentIndex() == 4:
            treewidget = self.ui.container_treewidget_2
            items = self.items_dict_2
        return treewidget, items


    def show_content(self, btn):
        """Запускает события при нажатии виджетов."""
        btn.setStyleSheet(btn_style_active) # При нажатии применяет стиль для активной кнопки
        self.ui.label.setText(btn.text())

        if not self.active_button:
            self.active_button = btn
            self.handle_tab_selection(btn)
        elif btn == self.active_button:
            event_message = f"""
            <br> {'&nbsp;'*8} {datetime.now()} <br>
            {'&nbsp;'*8} Выбран текущий виджет
            """
            self.add_text_to_logs(event_message, error=False)
        else:
            self.active_button.setStyleSheet(btn_style_unactive)
            btn.setStyleSheet(btn_style_active)
            self.active_button = btn
            self.handle_tab_selection(btn)

    def handle_tab_selection(self, btn):
        """Обрабатывает выбор виджета."""
        btn_to_log_message = {
            self.ui.loadData_btn: f"Выбран виджет: Загрузка данных",
            self.ui.loadWells_btn: f"Выбран виджет: Загрузка скважин",
            self.ui.reportBM_btn: f"Выбран виджет: Отчет по БМ",
            self.ui.updateBM_btn: f"Выбран виджет: Обновление БМ",
            self.ui.transferBM_btn: f"Выбран виджет: Перевод БМ",
            self.ui.logs_btn: f"Выбран виджет: Журнал логов",
        }

        if btn in btn_to_log_message:
            event_message = f"""
            <br> {'&nbsp;'*8} {datetime.now()} <br>
            {'&nbsp;'*8} {btn_to_log_message[btn]}
            """
            self.add_text_to_logs(event_message, error=False)

        # Запускает соответствующие функции загрузки и отображения контента при выборе определенной вкладки
        if btn == self.ui.loadData_btn:
            self.show_loadData()
        elif btn == self.ui.loadWells_btn:
            self.load_wells_page()
        elif btn == self.ui.reportBM_btn:
            self.load_report_page()
        elif btn == self.ui.updateBM_btn:
            self.load_update_BM(self.ui.geo_tw_1, self.ui.other_tw_1)
        elif btn == self.ui.transferBM_btn:
            self.load_transform_BM()
        elif btn == self.ui.logs_btn:
            self.show_logs()



    def show_loadData(self):
        """Загрузка проводника для вкладки Загрузка данных"""
        
        # Асинхронная загрузка деревьев проводников для Геологии, Маркшейдерии, Проектирования и Прочего
        # asyncio.run(async_show_all_tabs(geo_tw, mark_tw, proj_tw, other_tw))

        self.ui.stackedWidget.setCurrentIndex(0) # переключиться на вкладку Загрузка данных

    def load_wells_page(self):
        """переключиться на виджет Загрузка скважин"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def load_report_page(self):
        """переключиться на виджет Отчет по БМ"""
        self.ui.stackedWidget.setCurrentIndex(2)

    def load_update_BM(self, geo_tw, other_tw):
        """переключиться на виджет Обновление БМ"""
        self.ui.stackedWidget.setCurrentIndex(3)
        # asyncio.run(async_show_geo_other_tabs(geo_tw, other_tw))
        
    def load_transform_BM(self):
        """переключиться на виджет Перевод БМ"""
        self.ui.stackedWidget.setCurrentIndex(4)



    def check_alert_list(self):
        """Проверяет наличие оповещений"""
        # Проверяем, был ли добавлен новый элемент в alerts_list
        if len(self.alert_list) > 0:
            self.ui.logs_btn.setIcon(QIcon(":/alerts/icons/data_alert.png"))


    def show_logs(self):
        """Переключиться на виджет Журнал логов"""
        self.ui.stackedWidget.setCurrentIndex(5)
        self.alert_list = []
        self.ui.logs_btn.setIcon(QIcon())


    def add_text_to_logs(self, text, error=False):
        """Пишет текст в QTextEdit с записями логов"""
        if error:
            # Новый фрагмент текста с красным цветом
            new_text = f"<font color='red'>{text}</font>"
        else:
            new_text = text

        self.ui.logs_content.append(new_text)

    # def handle_dropped_file(self, dropped_path):
    #     """Принимает и обрабатывает попавшие в Drop файлы"""

    #     current_treewidget, current_items = self.get_current_container()


        # is_dir = os.path.isdir(dropped_path)

        # def paths_filenames(path):
        #     paths = set()
        #     for entry in os.listdir(path):
        #         full_path = os.path.join(path, entry)
        #         if os.path.isfile(full_path):
        #             paths.add(entry)
        #         elif os.path.isdir(full_path):
        #             paths.update(paths_filenames(full_path))
        #     return paths

        # def set_file_to_treewidget(dropped_path):
        #     dropped_name = dropped_path.replace('\\', '/').split('/')[-1]

        #     if dropped_path.lower().endswith('.tridb') and dropped_name not in current_items:
        #         try:
        #             conn = sqlite3.connect(dropped_path)
        #             cursor = conn.cursor()
        #             query = f"""
        #                         SELECT Name
        #                         FROM GeneralInformation
        #                         """
        #             names_list = [name[0] for name in \
        #                           cursor.execute(query)]
                    
        #             current_items[dropped_name] = {'childs': names_list, 'parent': ''}

        #         except Exception as e:
        #             error_message = f"""
        #                 <br> {'&nbsp;'*8} {datetime.now()} <br>
        #                 {'&nbsp;'*8} Error >>> handle_dropped_file() <br>
        #                 {'&nbsp;'*12} Ошибка при выполнении запроса к .tridb <br>
        #                 {'&nbsp;'*12} args: (self, {dropped_path}) <br>
        #                 {'&nbsp;'*12} Текст ошибки: {e}
        #                 """
        #             self.alert_list.append(e)
        #             self.add_text_to_logs(error_message, error=True)
        #         finally:
        #             if conn:
        #                 conn.close()

        #     elif dropped_path.lower().endswith('.dat') or dropped_path.lower().endswith('.str'):
        #         if dropped_name not in current_items:
        #             current_items[dropped_name] = {'parent': '', 'childs': ''}

        # if is_dir:
        #     paths = paths_filenames(dropped_path)
        #     for path in paths:
        #         set_file_to_treewidget(path)
        # else:
        #     set_file_to_treewidget(dropped_path)





    


try:
    app = QApplication([])
    window = GUI()
    window.show()
    sys.exit(app.exec_())
except SystemExit:
    print('Выход')

