from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Controller import Controller


class SetStorageFolderDialog(QFileDialog):
    def __init__(self):
        super(SetStorageFolderDialog, self).__init__()

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "请选择存储文件夹", ".")
        if directory != "":
            moveWallpaper = QMessageBox.question(self, "请选择", "你想要转移壁纸到新文件夹吗？\n"
                                                              "1. 若不转移将不能预览现有壁纸！\n"
                                                              "2. 重设存储路径后将延续已有编号！\n"
                                                              "建议转移壁纸。",
                                                 QMessageBox.Yes | QMessageBox.No)
            ret = Controller.set_storage_folder(directory, moveWallpaper == QMessageBox.Yes)
            QMessageBox.information(self, ret[0].value, ret[1], QMessageBox.Yes)
            self.close()
