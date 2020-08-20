import json
import os
from enum import Enum


# todo 枚举变量抽离
class ResetMessage(Enum):
    """
    ResetMessage:设置更新结果枚举类
    """
    success = 0             # 重置成功
    locationNotExist = 1    # 路径不存在
    fileNotFound = 2        # settings文件找不到


class StorageMethod(Enum):
    """
    StorageMethod:存储方式枚举类
    """
    textFile = 0
    database = 1
    unknown = 2


class SettingsAnalyser:
    """
    SettingsAnalyser:设置分析类
    用于解析出图片源和存储位置及已经存储了相应版式的多少图片
    """
    def __init__(self):
        self.__filename = os.path.join(os.getcwd(), "./settings.json")
        self.__settings = dict()
        self.__sourceFolder = str()
        self.__storageFolder = str()
        self.__storageMethod: StorageMethod
        self.__horizontalNumber = 0
        self.__verticalNumber = 0
        self.__unusedIdentityAndNumber = [[], [], []]
        self.__initialResult: ResetMessage
        self.__read_file()

    def __load_settings(self):
        with open(self.__filename, encoding="utf-8", mode="r") as file:
            self.__settings = json.load(file)

    def __assign_settings(self):
        self.__sourceFolder = self.__settings["SourceFolder"]
        self.__storageFolder = self.__settings["StorageFolder"]
        self.__storageMethod = StorageMethod(self.__settings["StorageMethod"])
        self.__horizontalNumber = self.__settings["HorizontalNumber"]
        self.__verticalNumber = self.__settings["VerticalNumber"]
        self.__unusedIdentityAndNumber = self.__settings["UnusedIdentityAndNumber"]

    def __read_file(self):
        """
        读取json文件的内容
        1. 载入设置
        2. 为类中的相应属性赋值
        3. 返回结果
        :return: 暂无
        """
        try:
            self.__load_settings()
            self.__assign_settings()
            self.__initialResult = ResetMessage.success
        except FileNotFoundError:
            self.__initialResult = ResetMessage.fileNotFound

    def get_initial_result(self):
        return self.__initialResult

    def get_source_folder(self):
        return self.__sourceFolder.replace("Username", os.getlogin(), 1)

    def get_storage_folder(self):
        return self.__storageFolder

    def get_storage_method(self):
        return self.__storageMethod

    def get_horizontal_number(self):
        return self.__horizontalNumber

    def get_vertical_number(self):
        return self.__verticalNumber

    def get_unused_identity_and_number(self):
        return self.__unusedIdentityAndNumber

    def reset_source_folder(self):
        """
        重置壁纸源文件夹
        1. 先给设置字典中的源壁纸路径赋默认值
        2. 更新json文件
        3. 文件操作成功回写到相应成员变量中，否则转到4
        4. 使用旧的成员变量值回写设置字典
        5. 返回操作结果
        :return: ResetMessage
        """
        try:
            self.__settings["SourceFolder"] = "C:/Users/Username/AppData/Local/Packages/Microsoft." \
                                              "Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"
            self.__update_file()
            # 对程序中正在运行中的数据进行更新
            self.__sourceFolder = self.__settings["SourceFolder"].replace("Username", os.getlogin(), 1)
            return ResetMessage.success
        except FileNotFoundError:
            self.__settings["SourceFolder"] = self.__sourceFolder
            return ResetMessage.fileNotFound

    def set_storage_folder(self, location: str):
        """
        重设壁纸存储路径
        1. 判断新路径是否存在
        2. 若存在则更新设置字典，否则跳转到6
        3. 更新json文件
        4. 文件操作成功回写到相应成员变量，否则跳转到5
        5. 使用旧的存储路径回写设置字典
        6. 返回操作结果
        :param location: 新的壁纸存储路径
        :return: ResetMessage
        """
        if os.path.exists(location) is True:
            try:
                self.__settings["StorageFolder"] = location
                self.__update_file()
                # 对程序中正在使用中的数据进行更新
                self.__storageFolder = self.__settings["StorageFolder"]
                return ResetMessage.success
            except FileNotFoundError:
                self.__settings["StorageFolder"] = self.__storageFolder
                return ResetMessage.fileNotFound
        else:
            return ResetMessage.locationNotExist

    def set_storage_method(self, method: StorageMethod):
        """
        设置存储方式
        :param method: 新的存储方式
        :return: ResetMessage
        """
        if method in [StorageMethod.database, StorageMethod.textFile]:
            self.__settings["StorageMethod"] = method.value
            try:
                self.__update_file()
                # 文件更新成功，对程序中正在使用的数据进行更新
                self.__storageMethod = method
                return ResetMessage.success
            except FileNotFoundError:
                # 文件写入失败，用旧的存储方式回写到设置字典中
                self.__settings["StorageMethod"] = self.__storageMethod.value
                return ResetMessage.fileNotFound

    def refresh_number(self, horizontal_num: int, vertical_num: int):
        """
        刷新设置文件中的图片数量
        1. 判断是否有更新必要
        2. 若有则更新设置字典，否则跳转到6
        3. 更新json文件
        4. 文件操作成功则回写到相应成员变量中，否则跳转到5
        5. 使用旧的数值回写设置字典
        6. 返回操作结果
        :param horizontal_num: 新增的水平版式的图片数量
        :param vertical_num: 新增的竖直版式的图片数量
        :return: ResetMessage
        """
        self.__settings["HorizontalNumber"] += horizontal_num
        self.__settings["VerticalNumber"] += vertical_num
        try:
            self.__update_file()
            # 对程序中正在使用中的数据进行更新
            self.__horizontalNumber = self.__settings["HorizontalNumber"]
            self.__verticalNumber = self.__settings["VerticalNumber"]
            return ResetMessage.success
        except FileNotFoundError:
            self.__settings["HorizontalNumber"] = self.__horizontalNumber
            self.__settings["VerticalNumber"] = self.__verticalNumber
            return ResetMessage.fileNotFound

    def add_unused_identity_and_number(self, unused_id_num: list):
        length = len(self.__settings["UnusedIdentityAndNumber"])
        for i in range(length):
            self.__settings["UnusedIdentityAndNumber"][i].extend(unused_id_num[i])
        try:
            self.__update_file()
            # 对程序中正在使用中的数据进行更新
            for i in range(length):
                self.__unusedIdentityAndNumber[i] = self.__settings["UnusedIdentityAndNumber"][i]
            return ResetMessage.success
        except FileNotFoundError:
            for i in range(length):
                self.__settings["UnusedIdentityAndNumber"][i] = self.__unusedIdentityAndNumber[i]
            return ResetMessage.fileNotFound

    def __update_file(self):
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(self.__settings, file, indent=4)
