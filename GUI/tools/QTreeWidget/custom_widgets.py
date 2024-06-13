from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, QUrl, QMimeData
from PyQt5.QtGui import QDrag
import os, sys



class CustomTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Кастомный делегат для иконок
        self.setItemDelegate(CustomItemDelegate(self))
        self.setHeaderHidden(True)
        self.allowed_extensions = ('.tridb', '.dat', '.str')

        self.already_populated = []

        # Логика нажатия мышкой
        self.icon_clicked = False
        self.doubleclicked = False

        # Отображение содержимого не-root узлов деревьев только по нажатию по ним
        self.itemExpanded.connect(self.populate_subtree)
        
    def populate_tree(self, path):
        """Заполнить ветку root-элемента"""
        self.root_name = os.path.basename(path)
        self.root_item = self.create_tree_item(path, self.root_name, True)
        self.addTopLevelItem(self.root_item)

        self.toggle_item_expansion(self.root_item)


    def populate_subtree(self, tree_item):
        """Заполнить ветку non-root-элемента"""
        if tree_item not in self.already_populated:
            path = self.get_item_path(tree_item)
            is_folder = self.is_folder(path)
            if is_folder:
                print('>>> populate_subtree() populating tree node:', path)
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if self.is_allowed_file(item_path):
                        is_folder = self.is_folder(item_path)
                        child_item = self.create_tree_item(item_path, item, is_folder, tree_item)
                        tree_item.addChild(child_item)
            self.already_populated.append(tree_item)


    def get_item_path(self, item):
        """Получить путь элемента"""
        if item is self.root_item:
            return self.root_path
        
        path_parts = []

        print('item:',  item.text(0), 'parent:', item.parent().text(0))

        while item is not None:
            if item.text(0) != self.root_name:
                path_parts.insert(0, item.text(0))
                item = item.parent()
            else:
                break
        return os.path.join(self.root_path, *path_parts)


    @staticmethod
    def is_folder(path):
        """Проверка является ли указанный путь папкой"""
        return os.path.isdir(path)

    @classmethod
    def create_tree_item(cls, item_path, name, is_folder, parent=None):
        item = QTreeWidgetItem([name])
        item.setData(0, Qt.UserRole, QUrl.fromLocalFile(item_path))
        if is_folder:
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setSizeHint(0, QSize(25, 25))
        if parent:
            parent.addChild(item)
            item.setSizeHint(0, QSize(30, 30))
        return item

    
    def is_allowed_file(self, path):
        """Проверка разрешенных файлов"""
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            return ext.lower() in self.allowed_extensions

        return True    

        
    def hide_indicators(self, root):
        """Скрытие индикаторов раскрытия веток"""
        branches = [root.child(i) for i in range(root.childCount())]
        for branch in branches:
            branch.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)


    def on_item_collapsed(self, item):
        if self.icon_clicked:
            print(f"Индикатор папки '{item.text(0)}' свернут")
            self.icon_clicked = False
            item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
            self.collapseItem(item)


    def toggle_item_expansion(self, item):
        """Переключение раскрытия элемента дерева"""
        if item.isExpanded() and self.doubleclicked:
            self.collapseItem(item)                                       
            item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
        elif item.isExpanded() and not self.doubleclicked:       
            self.collapseItem(item)                                       
            item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
        elif not item.isExpanded():
            self.expandItem(item)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            self.hide_indicators(item)


    def mousePressEvent(self, event):
        """Обработка нажатия мыши по индикатору"""
        item = self.itemAt(event.pos())
        print('clicked:', item.text(0), type(item))

        if item and event.pos().x() <= self.visualItemRect(item).left():
            self.icon_clicked = True
            if item.isExpanded():
                self.on_item_collapsed(item)


        url = item.data(0, Qt.UserRole)
        mimeData = QMimeData()
        mimeData.setUrls([QUrl(url)])
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_()

        super().mousePressEvent(event)


    def mouseDoubleClickEvent(self, event):
        """Обработка двойного клика мыши по элементу"""
        self.doubleclicked = True
        item = self.itemAt(event.pos())
        print('doubleclicked:', item.text(0), type(item))
        if item:
            self.toggle_item_expansion(item)
            self.doubleclicked = False

  



class TreeWidget_DragOnly(CustomTreeWidget):
    def __init__(self, parent=None, root_path=None,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root_path = root_path
        
        self.populate_tree(self.root_path)

        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setDragDropMode(QAbstractItemView.DragDrop)

    def start_logging(self):
        """Перехват вывода print()"""
        self.original_stdout = sys.stdout
        sys.stdout = self

    def write(self, message):
        """Запись вывода в файл"""
        with open(rf"{env.logs_folder}/custom_widget/logs.txt", "a") as f:
            f.write(message)
        self.original_stdout.write(message)

    def flush(self):
        # Реализуем метод flush(), чтобы соответствовать протоколу файлового объекта
        self.original_stdout.flush()


    def dragEnterEvent(self, event):
        url = event.mimeData().urls()[0].toLocalFile()
        print('dragged:', url)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        """Переопределенный метод dropEvent для запрета перетаскивания элементов внутри виджета"""
        if event.source() == self:
            event.ignore()
        else:
            super().dropEvent(event)





class TreeWidget_DropOnly(CustomTreeWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setDragEnabled(False)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setDefaultDropAction(Qt.LinkAction)


    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dragEnterEvent(self, event):
        
        print('entered url:', event.mimeData().urls()[0].toLocalFile())
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            self.root_path = urls[0].toLocalFile()
            print('dropped url:', self.root_path)            
            print('dropped name:', urls[0].fileName())
            self.populate_tree(self.root_path)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)






if __name__ == '__main__':
    try:

        import sys
        from pathlib import Path

        project_path = str(Path(__file__).resolve().parent.parent.parent)
        print(project_path)
        sys.path.insert(0, project_path)       # добавить в PATH

        # Конфигуратор иконок для каталогов
        from tools.manage_icons import CustomItemDelegate

        import env
        
        app = QApplication([])

        treewidget = TreeWidget_DragOnly(None, env.geo_folder)
        # treewidget = TreeWidget_DropOnly(None)
        treewidget.show()

        sys.exit(app.exec_())

    except SystemExit:
        print('Выход')

else:

    from tools.manage_icons import CustomItemDelegate
    import env