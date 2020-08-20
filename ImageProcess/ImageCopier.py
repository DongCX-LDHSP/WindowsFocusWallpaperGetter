import shutil
from FilenameManager.RecordLine import RecordLine
from FilenameManager.FilenameManager import *
from os import rename, listdir, path, mkdir, remove
from ImageProcess.ImageAnalyser import *
from datetime import datetime


class ImageCopier:
    """
    ImageCopier:负责复制图片并进行重命名
    """
    def __init__(self, source_folder: str, storage_folder: str, number: tuple,
                 unused_id_and_num: list, filename_manager: FilenameManager):
        self.__sourceFolder = source_folder
        self.__storageFolder = storage_folder
        self.__imageCounter = [0, 0]
        self.__numCounter = [0, 0]
        self.__number = number
        self.__unusedIdAndNum = unused_id_and_num
        self.__filenameManager = filename_manager
        self.__newGetFilenames = list()
        self.__recordLines = list()
        self.__exampleName = "wallpaper"

    def copy_wallpaper(self):
        """
        复制壁纸
        1. 筛选新壁纸
        2. 生成RecordLine
        3. 复制壁纸
        4. 基于生成的RecordLine重命名壁纸
        5. 更新文件名称存储信息
        :return: 新增壁纸数量列表
        """
        self.__select_new_image()
        self.__generate_record_line()
        self.__copy_file()
        self.__rename_wallpaper()
        self.__update_filename_storage()
        return self.__imageCounter, self.__numCounter

    def __select_new_image(self):
        """
        筛选新壁纸
        :return: 暂无
        """
        new_filenames = listdir(self.__sourceFolder)
        for filename in new_filenames:
            if self.__filenameManager.is_in_old_filenames(filename) is False:
                self.__newGetFilenames.append(filename)

    def __generate_record_line(self):
        """
        生成RecordLine，便于后续处理
        1. 生成id
        2. 获取图片版式及图片格式
        3. 基于格式对图像进行不同的处理
        4. horizontal和vertical生成RecordLine；unknown和invalidFile暂时未进行处理
        5. 生成完毕之后添加到相应成员变量中
        :return: 暂无
        """
        identityUp = self.__number[0] + self.__number[1]
        for old_name in self.__newGetFilenames:
            absoluteName = path.join(self.__sourceFolder, old_name)
            i_layout, i_format = ImageAnalyser.distinguish_image(absoluteName)
            if i_layout not in [ImageLayout.unknown, ImageLayout.invalidFile]:
                # 依据待处理图片版式选择要处理的数据
                flag = 0 if i_layout is ImageLayout.horizontal else 1

                # 记录行属性预生成
                try:
                    identity = self.__unusedIdAndNum[0].pop(0)
                except IndexError:
                    identityUp += 1
                    identity = identityUp
                try:
                    num = self.__unusedIdAndNum[flag + 1].pop(0)
                except IndexError:
                    self.__numCounter[flag] += 1
                    num = self.__number[flag] + self.__numCounter[flag]
                self.__imageCounter[flag] += 1
                new_name = self.__exampleName + str(num) + '.' + i_format.name
                self.__recordLines.append(RecordLine(identity, num, old_name, new_name, i_layout, datetime.now()))

    def __copy_file(self):
        """
        基于生成的RecordLine对象拷贝壁纸
        1. 逐一生成存储路径，并在必要时创建目录
        2. 复制壁纸
        :return: 暂无
        """
        for record_line in self.__recordLines:
            source = path.join(self.__sourceFolder, record_line.get_old_name())
            destination = path.join(self.__storageFolder, record_line.get_layout().name)
            if path.exists(destination) is False:
                mkdir(destination)
            shutil.copy(source, destination)

    def __rename_wallpaper(self):
        """
        重命名获取的壁纸
        1. 生成旧文件名
        2. 生成新的文件名
        3. 使用os.rename重命名
        :return: 暂无
        """
        for record_line in self.__recordLines:
            old_name = path.join(self.__storageFolder, record_line.get_layout().name, record_line.get_old_name())
            new_name = path.join(self.__storageFolder, record_line.get_layout().name, record_line.get_new_name())
            rename(old_name, new_name)

    def __update_filename_storage(self):
        self.__filenameManager.append_filenames(self.__recordLines)

    @staticmethod
    def move_wallpaper(old_storage_folder: str, new_storage_folder: str):
        """
        用于重设存储路径时转移壁纸
        1. 获取目录结构
        2. 生成旧路径
        3. 生成新路径
        4. 使用shutil.move移动文件或文件夹
        :param old_storage_folder: 旧的壁纸存储文件夹
        :param new_storage_folder: 新的壁纸存储文件夹
        :return: 暂无
        """
        topLevelFolderAndFiles = listdir(old_storage_folder)
        for fileOrFolder in topLevelFolderAndFiles:
            old_path = path.join(old_storage_folder, fileOrFolder)
            new_path = path.join(new_storage_folder, fileOrFolder)
            shutil.move(old_path, new_path)

    @staticmethod
    def move_filename_storage(old_storage_folder: str, new_storage_folder: str):
        topLevelFolderAndFiles = listdir(old_storage_folder)
        for fileOrFolder in topLevelFolderAndFiles:
            old_path = path.join(old_storage_folder, fileOrFolder)
            if path.isfile(old_path):
                new_path = path.join(new_storage_folder, fileOrFolder)
                shutil.move(old_path, new_path)

    @staticmethod
    def delete_wallpaper(storage_folder: str, numbers: list):
        for horizontalNum in numbers[0]:
            absoluteName = path.join(storage_folder, ImageLayout.horizontal.name,
                                     "wallpaper" + str(horizontalNum) + ".jpg")
            remove(absoluteName)
        for verticalNum in numbers[1]:
            absoluteName = path.join(storage_folder, ImageLayout.vertical.name,
                                     "wallpaper" + str(verticalNum) + ".jpg")
            remove(absoluteName)
