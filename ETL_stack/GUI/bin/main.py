# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QSizeGrip, QMainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon
from pathlib import Path

path = str(Path(__file__).resolve().parent.parent) + '/libs'
sys.path.insert(0, path)


from gui.interface import Ui_MainWindow

app = QApplication([])
screen_resolution = app.desktop().screenGeometry()
display_width, display_height = screen_resolution.width(), screen_resolution.height()

class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.slide_state = False
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        self.flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        self.setWindowFlags(self.flags)

        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.ui.apps_grid.mouseMoveEvent = moveWindow
        self.ui.pushButton_8.clicked.connect(lambda: self.slideLeftMenu())

    def anim(self, width, newWidth):
        self.animation = QPropertyAnimation(self.ui.toolbox_frame, b'maximumWidth')
        self.animation.setDuration(260)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def restore_or_maximize_window(self):
        'Полноэкранный режим/Оконный режим'
        if self.isMaximized():
            self.showNormal()
            self.ui.restore_window_button.setIcon(QIcon(':/window/icons/fullscreen.png'))
            self.ui.toolbox_frame.setMaximumSize(QSize(display_width // 6 - 13, 16777215))
            width = 0
            if self.slide_state:
                newWidth = 0
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/right.png'))
                self.ui.toolbox_frame.setMaximumSize(QSize(0, 16777215))
            else:
                newWidth = display_width // 5 - 13
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/menu.png'))

        else:
            self.showMaximized()
            self.ui.restore_window_button.setIcon(QIcon(':/window/icons/halfscreen.png'))
            self.ui.toolbox_frame.setMaximumSize(QSize(display_width // 5 - 13, 16777215))
            width = 0
            if self.slide_state:
                newWidth = 0
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/right.png'))
                self.ui.toolbox_frame.setMaximumSize(QSize(0, 16777215))
            else:
                newWidth = display_width // 5 - 13
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/menu.png'))

    def mousePressEvent(self, event):
        'Перемещение окна'
        self.clickPosition = event.globalPos()

    def slideLeftMenu(self):
        'Анимация слайд-меню'
        if self.isMaximized():
            self.ui.toolbox_frame.setMaximumSize(QSize(display_width // 5 - 13, 16777215))
            width = self.ui.toolbox_frame.width()
            if width == 0:
                newWidth = display_width // 5 - 13
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/menu.png'))
                self.slide_state = False
            else:
                newWidth = 0
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/right.png'))
                self.slide_state = True
            self.anim(width, newWidth)
        else:
            self.ui.toolbox_frame.setMaximumSize(QSize(display_width // 6 - 13, 16777215))
            width = self.ui.toolbox_frame.width()
            if width == 0:
                newWidth = display_width // 6 - 13
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/menu.png'))
                self.slide_state = False
            else:
                newWidth = 0
                self.ui.pushButton_8.setIcon(QIcon(':/slide_menu/icons/right.png'))
                self.slide_state = True
            self.anim(width, newWidth)

if __name__ == '__main__':
    window = GUI()
    window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Окно было закрыто')