from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Controller import Controller


class InitStorageFolderDialog(QFileDialog):
    storageFolderNotSet = pyqtSignal()

    def __init__(self):
        super(InitStorageFolderDialog, self).__init__()

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "请选择存储文件夹", ".")
        if directory != "":
            ret = Controller.set_storage_folder(directory, False, True)
            QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)
        else:
            self.storageFolderNotSet.emit()
