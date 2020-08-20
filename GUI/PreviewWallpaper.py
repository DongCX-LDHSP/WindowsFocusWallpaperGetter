from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

from Enumerations import ImageLayout


class PreviewWallpaper(QWidget):
    closeSignal = pyqtSignal(object)

    def __init__(self, filename, layout):
        super(PreviewWallpaper, self).__init__()
        self.__filename = filename
        self.__imageLayout = layout
        self.__horizontalSize = (16 * 90, 9 * 90)
        self.__verticalSize = (9 * 55, 16 * 55)
        self.__pixmap: QPixmap
        self.__setup_ui()

    def __setup_ui(self):
        if os.path.exists(self.__filename) is True:
            if self.__imageLayout in [ImageLayout.horizontal, ImageLayout.vertical]:
                self.setWindowTitle(os.path.basename(self.__filename))
                self.setWindowFlag(Qt.FramelessWindowHint)
                self.__set_window_size()
                self.__move_to_center()
                self.__zoom_image()
                self.__set_image()
                self.__set_layout()
                self.show()
            else:
                QMessageBox.warning(self, "不能预览", "未知版式的文件和非法文件不能预览！", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "打开文件失败", "找不到文件！\n"
                                "这可能是因为您之前调整过存储路径而没有转移壁纸！", QMessageBox.Yes)

    def __set_window_size(self):
        if self.__imageLayout is ImageLayout.horizontal:
            size = QSize(*self.__horizontalSize)
        elif self.__imageLayout is ImageLayout.vertical:
            size = QSize(*self.__verticalSize)
        self.setFixedSize(size)

    def __move_to_center(self):
        if self.__imageLayout is ImageLayout.horizontal:
            self.move((1920 - self.__horizontalSize[0]) // 2,
                      (1080 - self.__horizontalSize[1]) // 2)
        elif self.__imageLayout is ImageLayout.vertical:
            self.move((1920 - self.__verticalSize[0]) // 2,
                      (1080 - self.__verticalSize[1]) // 2)

    def __zoom_image(self):
        if self.__imageLayout is ImageLayout.horizontal:
            size = QSize(*self.__horizontalSize)
        elif self.__imageLayout is ImageLayout.vertical:
            size = QSize(*self.__verticalSize)
        image = QImage(self.__filename)
        self.__pixmap = QPixmap.fromImage(image.scaled(size, Qt.IgnoreAspectRatio))

    def __set_image(self):
        self.__imageLabel = QLabel()
        self.__imageLabel.resize(1600, 900)
        self.__imageLabel.setPixmap(self.__pixmap)

    def __set_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.__imageLabel)
        # 设置布局占用窗口的范围为铺满窗口
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.close()

    def closeEvent(self, a0: QCloseEvent):
        self.closeSignal.emit(id(self))
