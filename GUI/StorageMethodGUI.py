from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QRadioButton, QPushButton, QMessageBox, QVBoxLayout

from Controller import Controller
from Enumerations import StorageMethod, ExecuteMessage


class StorageMethodGUI(QDialog):
    def __init__(self):
        super(StorageMethodGUI, self).__init__()
        self.__settingsNotFound: bool
        self.__buttonFont = QFont("Microsoft YaHei", 12, QFont.Bold)

        ret = Controller.get_storage_folder()
        if ret[0] is ExecuteMessage.success:
            self.__storageFolder = ret[1]
            self.__settingsNotFound = False
        else:
            self.__storageFolder = ""
            self.__settingsNotFound = True
            self.__ret = ret

        ret = Controller.get_storage_method()
        if ret[0] is ExecuteMessage.success:
            self.__currentStorageMethod = ret[1]
            self.__settingsNotFound = False
            self.__setup_ui()
        else:
            self.__currentStorageMethod = StorageMethod.unknown
            self.__setup_ui()
            self.__settingsNotFound = True
            self.__ret = ret

    def __setup_ui(self):
        self.setWindowTitle("设置存储方式")
        self.setFixedSize(250, 130)

        # 生成单选按钮
        self.__databaseButton = QRadioButton("数据库")
        self.__databaseButton.setFont(self.__buttonFont)
        self.__textFileButton = QRadioButton("纯文本文件")
        self.__textFileButton.setFont(self.__buttonFont)
        self.__saveButton = QPushButton("保存")
        self.__saveButton.setText("保存")
        self.__saveButton.released.connect(self.__call_set_storage_method)
        self.__saveButton.setFont(self.__buttonFont)

        # 设置默认选项
        if self.__currentStorageMethod is StorageMethod.database:
            self.__databaseButton.setChecked(True)
        elif self.__currentStorageMethod is StorageMethod.textFile:
            self.__textFileButton.setChecked(True)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.__databaseButton)
        layout.addWidget(self.__textFileButton)
        layout.addWidget(self.__saveButton)
        self.setLayout(layout)

    def __call_set_storage_method(self):
        if self.__databaseButton.isChecked() is True:
            ret = Controller.set_storage_method(StorageMethod.database, self.__storageFolder)
        elif self.__textFileButton.isChecked() is True:
            ret = Controller.set_storage_method(StorageMethod.textFile, self.__storageFolder)

        # 给用户反馈设置结果
        QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)

        # 执行完毕后关闭对话框
        self.close()

    def deal_settings_not_found(self):
        QMessageBox.information(self, self.__ret[0].value, self.__ret[1], QMessageBox.Yes)
        self.close()

    def settings_is_not_found(self):
        return self.__settingsNotFound
