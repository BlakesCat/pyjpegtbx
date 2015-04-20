import os
import sys
import json

from PyQt5.QtCore import (
    QDir, Qt, QVariant
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QItemDelegate, QLabel, QHeaderView
)
from PyQt5.QtGui import (
    QPixmap, QStandardItemModel, QStandardItem
)

import ui_jpegtbx


class ImageDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        '''
        returns the widget used to change data from the model
        and can be reimplemented to customize editing behavior.
        '''
        if index.data() is None:
            return super().createEditor(parent, option, index)
        else:
            pass
            # jsobj = json.loads(index.data())
            # print('createEditor', type(jsobj), jsobj)
            # label = QLabel(parent)
            # # pic = QPixmap(jsobj['file'])
            # # label.setPixmap(pic)
            # return label

    def setEditorData(self, editor, index):
        '''
        provides the widget with data to manipulate.
        '''
        if index.data() is None:
            super().setEditorData(editor, index)
        else:
            pass
            # jsobj = json.loads(index.data())
            # print('setEditorData', type(jsobj), jsobj)
            # pic = QPixmap(jsobj['file'])
            # pic = pic.scaled(
            #     jsobj['width'], jsobj['height'],
            #     Qt.KeepAspectRatio
            # )
            # editor.setPixmap(pic)

    def setModelData(self, editor, model, index):
        '''
        returns updated data to the model.
        '''
        print('setModelData')
        # super().setModelData(editor, model, index)
        pass

    def updateEditorGeometry(self, editor, option, index):
        '''
        ensures that the editor is displayed correctly with respect to the item view.
        '''
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        if index.data() is None:
            super().paint(painter, option, index)
        else:
            jsobj = json.loads(index.data())
            pic = QPixmap(jsobj['file'])
            pic = pic.scaled(
                jsobj['width'], jsobj['height'],
                Qt.KeepAspectRatio
            )
            painter.drawPixmap(option.rect.x(), option.rect.y(), pic)


class ImageItem(QStandardItem):
    def __init__(self, filename, size):
        super().__init__()
        self.filename = filename
        self.size = size

pics = ['lfs.jpg', 'tmp0.jpg', 'tmp1.jpg']


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = ui_jpegtbx.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setCurFilePath()

        self.mainViewSize = {'col': 4, 'row': 3}  # col, row
        self.mainViewModel = QStandardItemModel()
        self.mainViewModel.setColumnCount(self.mainViewSize['col'])
        self.mainViewModel.setRowCount(self.mainViewSize['row'])
        # 绑定model
        self.ui.mainView.setModel(self.mainViewModel)
        # 加载Delegate类
        delegate = ImageDelegate()
        self.ui.mainView.setItemDelegate(delegate)
        # 行、列宽自动适应
        self.ui.mainView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.mainView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 加载数据
        for i, pic in enumerate(pics):
            col, row = i % self.mainViewSize['col'], i / self.mainViewSize['col']
            index = self.mainViewModel.index(row, col)

            data = {
                'file': pic,
                'height': 250,
                'width': 250,
            }
            item = QVariant(json.dumps(data))

            self.mainViewModel.setData(index, item)

    def setCurFilePath(self, filepath=None):
        if not filepath:
            path = sys.path[0]
            # 判断文件是编译后的文件还是脚本文件
            if os.path.isdir(path):  # 脚本文件目录
                dirpath = path
            else:  # 编译后的文件, 返回它的上一级目录
                dirpath = os.path.dirname(path)
        else:
            pass
        self.ui.le_curFilepath.setText(dirpath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
