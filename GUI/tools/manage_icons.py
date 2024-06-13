from PyQt5.QtWidgets import  QFileIconProvider, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QFileInfo,  QSize, Qt, QModelIndex, QRect
from PyQt5.QtGui import QIcon, QPainter

import os
import env

class CustomItemDelegate(QStyledItemDelegate):
    """
    Этот класс является пользовательским делегатом элементов, который обрабатывает отображение
    элементов в представлении. Он устанавливает иконку и определяет её размер для различных
    расширений файлов, а также отрисовывает текст рядом со значком.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_sizes = {
            ".dat": QSize(25, 25),
            ".tridb": QSize(25, 25),
            ".str": QSize(25, 25)
        }

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        """
        Отрисовывает элемент в представлении.
        :param painter: Объект QPainter, используемый для рисования.
        :param option: QStyleOptionViewItem, содержащий параметры элемента.
        :param index: QModelIndex элемента.
        """
        filename = index.data(Qt.DisplayRole)

        # Устанавливаем значок и размер в зависимости от расширения файла
        if '.' not in filename:
            icon = QIcon(os.path.join(env.directory, 'libs', 'icons', 'folder.png'))
            icon_size = QSize(20, 20)
        else:
            extension = os.path.splitext(filename)[1].lower()
            icon_size = self.icon_sizes.get(extension, QSize(25, 25))
            icon = QIcon(os.path.join(env.directory, 'libs', 'icons', f'{extension[1:]}.png'))

        # Отрисовываем иконку
        pixmap = icon.pixmap(icon_size)
        painter.drawPixmap(
            QRect(option.rect.x(), option.rect.y() + 5, icon_size.width(), icon_size.height()),
            pixmap
        )

        # Отрисовываем текст элемента с заданным отступом от иконки
        text_option = QStyleOptionViewItem(option)
        text_option.rect.setLeft(option.rect.left() + icon_size.width() + 5) # Расстояние между иконкой и текстом
        super().paint(painter, text_option, index)
