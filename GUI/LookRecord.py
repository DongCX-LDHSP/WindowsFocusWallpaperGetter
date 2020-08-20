from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator, Qt, QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QCheckBox, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QRadioButton, QPushButton
from PyQt5.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QTableWidget, QTableWidgetItem

from GUI.PreviewWallpaper import PreviewWallpaper
from Controller import Controller
from Enumerations import ExecuteMessage, SearchMode

from os import path


class MyQLabel(QLabel):
    def __init__(self, row):
        super(MyQLabel, self).__init__()
        self.__row = row

    def get_row(self):
        return self.__row

    def set_row(self, row):
        self.__row = row


class MyQCheckBox(QCheckBox):
    def __init__(self, row: int):
        super(MyQCheckBox, self).__init__()
        self.__row = row

    def get_row(self):
        return self.__row

    def set_row(self, row: int):
        self.__row = row


class LookRecord(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self):
        super(LookRecord, self).__init__()
        self.__previewWindows = list()

        self.__storageFolder = Controller.get_storage_folder()[1]

        self.__buttonFont = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.__buttonText = ["请先选择搜索模式，然后键入关键词",
                             "搜索模式", "id或编号", "原始名称", "搜索", "重新载入数据", "删除"]

        self.__tableHeadFont = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.__tableContentFont = QFont("Consolas", 14, QFont.Normal)
        self.__tableOperationFont = QFont("Song", 14, QFont.Bold)
        self.__tableHead = ["选择", "操作", "id", "编号", "版式", "获取时间", "原始名称"]
        self.__tableWidth = [55, 70, 80, 80, 70, 270, 865]
        self.__checkBoxes = list()
        self.__labels = list()

        self.__recordLines = list()
        self.__readRecordLinesResult = False
        self.__init_record_lines()
        if self.__readRecordLinesResult is True:
            self.__setup_ui()
            self.show()

    def __init_record_lines(self):
        ret = Controller.look_record()
        if ret[0] is ExecuteMessage.success:
            self.__recordLines = ret[1]
            self.__readRecordLinesResult = True
        else:
            QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)

    def __setup_ui(self):
        self.setWindowTitle("查看记录")
        self.resize(1540, 800)
        self.__init_widget()
        self.__init_table()
        self.__set_layout()

    def __init_widget(self):
        self.__searchBox = QLineEdit()
        # 给输入框添加校验器
        reg = QRegExp('[a-zA-Z0-9]+$')
        lineEditValidator = QRegExpValidator(self)
        lineEditValidator.setRegExp(reg)
        self.__searchBox.setValidator(lineEditValidator)

        self.__searchOption = QLabel()
        self.__idNumRadioButton = QRadioButton()
        self.__oldNameRadioButton = QRadioButton()
        self.__searchButton = QPushButton()
        self.__searchButton.released.connect(self.__search)
        self.__refreshButton = QPushButton()
        self.__refreshButton.released.connect(self.refresh_totally)
        self.__deleteButton = QPushButton()
        self.__deleteButton.released.connect(self.__delete)
        # 设置按钮的字体和显示文字
        self.__set_buttons_font_text()
        # 添加一条水平线
        self.__frame = QFrame()
        self.__frame.setFrameShape(QFrame.Shape.HLine)

    def __set_buttons_font_text(self):
        buttons = list()
        buttons.append(self.__searchBox)
        buttons.append(self.__searchOption)
        buttons.append(self.__idNumRadioButton)
        buttons.append(self.__oldNameRadioButton)
        buttons.append(self.__searchButton)
        buttons.append(self.__refreshButton)
        buttons.append(self.__deleteButton)
        for i in range(len(buttons)):
            buttons[i].setText(self.__buttonText[i])
            buttons[i].setFont(self.__buttonFont)
        self.__searchBox.setText("")
        self.__searchBox.setPlaceholderText("请先选择搜索模式，然后键入关键词")
        self.__idNumRadioButton.setChecked(True)

    def __init_table(self):
        self.__table = QTableWidget()
        self.__table.setColumnCount(len(self.__tableHead))
        self.__table.setRowCount(len(self.__recordLines))
        self.__table.setHorizontalHeaderLabels(self.__tableHead)
        # 禁止编辑
        self.__table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 隐藏左侧表头
        self.__table.verticalHeader().setVisible(False)
        self.__table.horizontalHeader().setFont(self.__tableHeadFont)
        # 压入数据
        self.__add_item_to_table()
        self.__set_table_height_width()

    def __add_item_to_table(self):
        # 清空复选框和预览标签
        del self.__checkBoxes
        del self.__labels
        self.__checkBoxes = list()
        self.__labels = list()
        for i in range(len(self.__recordLines)):
            # 放入操作控件
            selectionCheckBox = MyQCheckBox(i)
            self.__checkBoxes.append(selectionCheckBox)
            selectionCheckBox = self.__set_widget_style(selectionCheckBox)

            previewLabel = MyQLabel(i)
            self.__labels.append(previewLabel)
            previewLabel.setText("<a href = '#'>预览</a>")
            previewLabel.linkActivated.connect(self.__preview_image)
            previewLabel = self.__set_widget_style(previewLabel)

            self.__table.setCellWidget(i, 0, selectionCheckBox)
            self.__table.setCellWidget(i, 1, previewLabel)

            # 放入记录项
            message = self.__recordLines[i].get_gui_string_tuple()
            for j in range(5):
                item = QTableWidgetItem(message[j])
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.__tableContentFont)
                self.__table.setItem(i, 2 + j, item)

    def __set_table_height_width(self):
        for i in range(self.__table.rowCount()):
            self.__table.setRowHeight(i, 45)
        for i in range(len(self.__tableHead)):
            self.__table.setColumnWidth(i, self.__tableWidth[i])

    def __set_widget_style(self, widget: QWidget):
        temp = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(widget)
        temp.setLayout(layout)
        temp.setFont(self.__tableOperationFont)
        return temp

    def __set_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.__searchOption, 0, 0, 1, 3)
        layout.addWidget(self.__idNumRadioButton, 0, 3, 1, 3)
        layout.addWidget(self.__oldNameRadioButton, 0, 6, 1, 3)
        layout.addWidget(self.__searchBox, 1, 0, 1, 16)
        layout.addWidget(self.__searchButton, 1, 16, 1, 3)
        layout.addWidget(self.__deleteButton, 1, 19, 1, 3)
        layout.addWidget(self.__refreshButton, 1, 22, 1, 3)
        layout.addWidget(self.__frame, 2, 0, 1, 25)
        layout.addWidget(self.__table, 3, 0, 1, 25)
        self.setLayout(layout)

    def __search(self):
        keyWord = self.__searchBox.text()
        # 提示信息转移到控制器
        if self.__oldNameRadioButton.isChecked() is True:
            ret = Controller.search_image(keyWord, SearchMode.oldFilename)
        elif self.__idNumRadioButton.isChecked() is True:
            ret = Controller.search_image(keyWord, SearchMode.idAndNum)
        if ret[0] is ExecuteMessage.success:
            del self.__recordLines
            self.__recordLines = ret[1]
            self.__refresh_after_search()
        elif ret[0] is ExecuteMessage.failure:
            QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)

    def __refresh_after_search(self):
        self.__table.clearContents()
        self.__table.setRowCount(len(self.__recordLines))
        self.__add_item_to_table()
        self.__set_table_height_width()

    def refresh_totally(self, out_call: bool = False):
        del self.__recordLines
        self.__readRecordLinesResult = False
        self.__init_record_lines()
        if self.__readRecordLinesResult is True:
            self.__table.setRowCount(len(self.__recordLines))
            self.__add_item_to_table()
            self.__set_table_height_width()
            if out_call is False:
                QMessageBox.information(self, "刷新提示", "刷新成功！", QMessageBox.Yes)
        elif self.__readRecordLinesResult is False:
            QMessageBox.information(self, "刷新提示", "刷新失败！", QMessageBox.Yes)

    def __delete(self):
        identities = list()
        deleteRows = list()
        for checkBox in self.__checkBoxes:
            if checkBox.isChecked() is True:
                row = checkBox.get_row()
                identities.append(self.__recordLines[row].get_id())
                deleteRows.append(row)

        if len(identities) == 0:
            QMessageBox.information(self, "请选择图片", "您未选择任何图片！", QMessageBox.Yes)
        else:
            choice = QMessageBox.question(self, "请确认", "您确实要删除这{}张壁纸吗？".format(len(identities)),
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                ret = Controller.delete_image(identities)
                if ret[0] is ExecuteMessage.success:
                    self.__refresh_after_delete(deleteRows)
                QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)

    def __refresh_after_delete(self, delete_rows: list):
        for row in reversed(delete_rows):
            self.__table.removeRow(row)
            del self.__checkBoxes[row]
            del self.__labels[row]
            del self.__recordLines[row]
        # 重新编号checkBox和label
        for i in range(len(self.__checkBoxes)):
            self.__checkBoxes[i].set_row(i)
            self.__labels[i].set_row(i)

    def __preview_image(self):
        row = self.sender().get_row()
        imageLayout = self.__recordLines[row].get_layout()
        filename = path.join(self.__storageFolder, imageLayout.name, self.__recordLines[row].get_new_name())
        preview = PreviewWallpaper(filename, imageLayout)
        self.__previewWindows.append(preview)
        preview.closeSignal.connect(self.__delete_preview_window)

    def __delete_preview_window(self, window_id: int):
        for previewWindow in self.__previewWindows:
            if id(previewWindow) == window_id:
                self.__previewWindows.remove(previewWindow)
                break

    def closeEvent(self, a: QCloseEvent):
        self.closeSignal.emit()
