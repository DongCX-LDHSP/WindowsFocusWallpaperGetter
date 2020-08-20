from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCloseEvent, QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QVBoxLayout, QApplication

import sys
import platform
import re

from GUI.StorageMethodGUI import StorageMethodGUI
from GUI.InitStorageFolder import InitStorageFolderDialog
from GUI.SetStorageFolderDialog import SetStorageFolderDialog
from GUI.LookRecord import LookRecord
from Controller import Controller
from Enumerations import ExecuteMessage


class MainWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.__lookRecordWindow = None

        self.__buttons = list()
        self.__buttonFont = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.__buttonNames = ["getWallpaperButton", "lookRecordButton",
                              "SetStorageFolder", "ResetSourceFolder", "SetStorageMethod"]
        self.__buttonTexts = ["获取壁纸", "查看记录", "设置保存文件夹", "重置源文件夹", "设置存储方式"]
        self.__buttonSlots = [self.__get_focus_wallpaper,
                              self.__look_record,
                              self.__set_storage_folder,
                              self.__reset_source_folder,
                              self.__set_storage_method_dialog]
        self.__reOperatingSystemName = re.compile(r"Windows-10*")
        self.__setup_ui()

    def __check_operating_system(self):
        if self.__reOperatingSystemName.match(platform.platform()) is not None:
            return True
        return False

    def __setup_ui(self):
        if self.__check_operating_system() is True:
            self.setWindowTitle("Windows聚焦壁纸获取")
            self.setFixedSize(380, 260)
            self.__generate_buttons()
            self.setLayout(self.__add_buttons_to_vertical_layout())
            self.show()
            self.__check_storage_folder()
        else:
            QMessageBox.warning(self, "操作系统错误", "请在Windows10下运行该程序!", QMessageBox.Yes)
            self.close()

    def __generate_buttons(self):
        for i in range(len(self.__buttonNames)):
            button = QPushButton(self.__buttonNames[i])
            button.setText(self.__buttonTexts[i])
            button.released.connect(self.__buttonSlots[i])
            button.setFont(self.__buttonFont)
            self.__buttons.append(button)

    def __add_buttons_to_vertical_layout(self):
        layout = QVBoxLayout()
        for button in self.__buttons:
            layout.addWidget(button)
        return layout

    def __check_storage_folder(self):
        ret = Controller.check_storage_folder()
        if ret[0] is ExecuteMessage.success:
            if ret[1] != "":
                QMessageBox.information(self, "初始化", ret[1], QMessageBox.Yes)
                initStorageFolder = InitStorageFolderDialog()
                initStorageFolder.setWindowModality(Qt.ApplicationModal)
                initStorageFolder.storageFolderNotSet.connect(self.__storage_folder_not_set)
                initStorageFolder.open_directory_dialog()
                del initStorageFolder

    def __storage_folder_not_set(self):
        self.close()

    def __get_focus_wallpaper(self):
        ret = Controller.get_focus_wallpaper()
        QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)
        if self.__lookRecordWindow is not None:
            self.__lookRecordWindow.refresh_totally(True)

    def __look_record(self):
        if self.__lookRecordWindow is None:
            self.__lookRecordWindow = LookRecord()
            self.__lookRecordWindow.setWindowModality(Qt.ApplicationModal)
            self.__lookRecordWindow.closeSignal.connect(self.__del_look_record_window)
        else:
            self.__lookRecordWindow.setWindowState(Qt.WindowActive)

    def __del_look_record_window(self):
        self.__lookRecordWindow = None

    @staticmethod
    def __set_storage_folder():
        setStorageFolderDialog = SetStorageFolderDialog()
        setStorageFolderDialog.setWindowModality(Qt.ApplicationModal)
        setStorageFolderDialog.open_directory_dialog()
        del setStorageFolderDialog

    def __reset_source_folder(self):
        ret = Controller.reset_source_folder()
        QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)

    @staticmethod
    def __set_storage_method_dialog():
        setStorageMethodGUI = StorageMethodGUI()
        setStorageMethodGUI.setWindowModality(Qt.ApplicationModal)
        if setStorageMethodGUI.settings_is_not_found() is True:
            setStorageMethodGUI.deal_settings_not_found()
        else:
            setStorageMethodGUI.exec()

    def closeEvent(self, a0: QCloseEvent):
        if self.__lookRecordWindow is not None:
            self.__lookRecordWindow.close()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./Images/WindowsSpotLightWallpaperGetter.ico"))
    mainWindow = MainWindow()
    sys.exit(app.exec_())
