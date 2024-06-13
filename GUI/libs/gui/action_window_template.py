from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QScrollArea, QScrollBar,QVBoxLayout
from PyQt5.QtCore import Qt, QRectF, QRect, QSize, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainterPath, QRegion

import sys



class Action_window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.minimize_window_button.clicked.connect(self.minimize_window)
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.restore_window_button.clicked.connect(self.restore_window)
        self.original_geometry = None

        self.flags = Qt.FramelessWindowHint
        self.setWindowFlags(self.flags)

        self.dragPos = QPoint()
        # Объекты за которые можно перетаскивать окно интерфейса
        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.mouseMoveEvent
        # ... Добавить сюда ещё при желании

        self.tree_views = (
            self.ui.geo_tw, self.ui.geo_tw_1, self.ui.geo_tw_2,
            self.ui.mark_tw, self.ui.proj_tw, self.ui.other_tw,
            self.ui.other_tw_1, self.ui.other_tw_2
        )

        self.set_window_mask()
        self.is_maximized = False
        self.is_minimized = False

        # Инициализируем свойства для анимации
        self.maximize_animation = QPropertyAnimation(self, b"geometry")
        self.minimize_animation = QPropertyAnimation(self, b"geometry")
        self.restore_animation = QPropertyAnimation(self, b"geometry")

        self.previous_geometry = None


    def mousePressEvent(self, event):
        self.dragPos = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()



    def set_window_mask(self):
        radius = 10.0
        path = QPainterPath()
        x = QRect(0, 0, 1010, 790)
        path.addRoundedRect(QRectF(x), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def minimize_window(self):
        if self.original_geometry is None:
            self.original_geometry = self.geometry()

        if not self.is_maximized:
            self.previous_geometry = self.geometry()

        self.is_minimized = True
            
        self.minimize_animation.setDuration(500)
        self.minimize_animation.setStartValue(self.geometry())
        self.minimize_animation.setEndValue(QRect(0, QDesktopWidget().height() - 50, 200, 50))
        self.minimize_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.minimize_animation.finished.connect(self.showMinimized)
        self.minimize_animation.start()

    def showEvent(self, event):
        if self.original_geometry is not None:
            if self.is_maximized:
                self.is_minimized = True
                self.maximize_window()
            else:
                self.restore_animation.setDuration(300)
                self.restore_animation.setStartValue(self.geometry())
                self.restore_animation.setEndValue(self.previous_geometry)
                self.restore_animation.setEasingCurve(QEasingCurve.OutQuad)
                self.restore_animation.start()
                self.is_minimized = True

        super().showEvent(event)


    def keyPressEvent(self, event):
        ...
        # model, treeview, items = self.get_current_model_and_treeview()

        # if event.key() == Qt.Key_Delete:

        #     selected_indexes = treeview.selectedIndexes()


        #     # Удаляем элементы по каждому индексу в обратном порядке, чтобы избежать ошибки "индекс вышел из диапазона"
        #     for index in reversed(selected_indexes):
        #         # Получаем родительский элемент
        #         parent = index.parent()
        #         if parent.isValid():
        #             parent_name = model.data(parent, Qt.DisplayRole)
        #         # Получаем имя удаляемого элемента
        #         element_name = model.data(index, Qt.DisplayRole)
        #         # Если корень
        #         if not parent.isValid():
        #             model.removeRow(index.row())
        #             del items[element_name]
        #         # Если элемент
        #         else:
        #             model.removeRow(index.row(), parent)
        #             items[parent_name]['childs'].remove(element_name)



        # elif event.key() == Qt.Key_Escape:
        #     treeview.clearSelection()


    def restore_window(self):
        if self.isMaximized():
            self.restore_animation.setDuration(200)
            self.restore_animation.setStartValue(self.geometry())
            self.restore_animation.setEndValue(self.previous_geometry)  # Используем метод normalGeometry
            self.restore_animation.setEasingCurve(QEasingCurve.OutQuad)
            self.restore_animation.finished.connect(self.finish_restore_animation)
            self.restore_animation.start()
            # self.set_icon_size(28)
            self.is_maximized = False
            self.is_minimized = False
        else:
            self.previous_geometry = self.geometry()
            self.maximize_window()
            # self.set_icon_size(37)
            self.is_maximized = True
            self.is_minimized = False
            

    def finish_restore_animation(self):
        self.showNormal()
        self.set_window_mask()

    def maximize_window(self):
        if self.is_minimized:
            geometry = self.previous_geometry
        else:
            geometry = self.geometry()

        self.maximize_animation.setDuration(200)
        self.maximize_animation.setStartValue(geometry)
        self.maximize_animation.setEndValue(QRect(0, 0, QApplication.desktop().width(), QApplication.desktop().height()))
        self.maximize_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.maximize_animation.finished.connect(self.showMaximized)
        self.maximize_animation.start()
        self.setMask(QRegion())
        
        self.is_maximized = True
        self.is_minimized = False



if __name__ == '__main__':

    try:
        from interface import Ui_MainWindow

        app = QApplication([])
        window = Action_window()
        window.show()
        sys.exit(app.exec_())
    except SystemExit:
        print('Выход')
else:
    from gui.interface import Ui_MainWindow
