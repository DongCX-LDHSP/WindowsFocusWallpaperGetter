from FilenameManager.FilenameManager import FilenameManager
from FilenameManager.RecordLine import RecordLine

# todo 枚举变量抽离
from ImageAnalyser import ImageLayout
import re
import os


class TextFile(FilenameManager):
    """
    TextFile:继承自FilenameManager
    以纯文本文档的形式存储文件名
    """
    def __init__(self, storage_folder: str):
        self.__filename = os.path.join(storage_folder, "Filename_OldWithNew.txt")
        self.__reRecordLine = re.compile("\t")
        self.__tableHead = str()
        self.__recordLines = list()
        self.__generate_record_file()
        self.__get_all_old_filenames()

    def __generate_record_file(self):
        """
        生成记录文件，可对比数据库存储形式理解
        1. 判断记录文件是否存在
        2. 若存在则结束，否则跳转到3
        3. 新建文件并写入表头
        :return: 暂无
        """
        if os.path.exists(self.__filename) is False:
            with open(self.__filename, 'w') as file:
                file.write("id\tnum\told_name\t\t\t\t\t\t\t\tnew_name\tlayout\tdate")

    def __get_all_old_filenames(self):
        """
        该方法用于初始化时从文件中还原记录，与数据库相比，文本文件预先载入生成对象较易处理
        1. 读取文件中的所有行
        2. 移除表头信息
        3. 移除换行符
        4. 还原成RecordLine对象
        :return: 暂无
        """
        with open(self.__filename, "r") as file:
            old_filenames = file.readlines()
            old_filenames = self.__remove_line_feed(old_filenames)
            self.__tableHead = old_filenames.pop(0)    # 从列表中移除表头
            self.__restore_to_object(old_filenames)

    @staticmethod
    def __remove_line_feed(old_filenames: list):
        for i in range(len(old_filenames)):
            old_filenames[i] = old_filenames[i].rstrip('\n')
        return old_filenames

    def __restore_to_object(self, old_filenames: list):
        """
        将记录还原成对象
        1. 分割字符串
        2. 将必要的字符串转换成整型
        3. 还原成对象
        4. 添加到相应成员变量中
        :param old_filenames: 从文件中读取的已有文件名称
        :return: 暂无
        """
        for line in old_filenames:
            message = self.__reRecordLine.split(line)
            message = self.__str_to_int(message)
            record_line = RecordLine.get_from_storage(message)
            self.__recordLines.append(record_line)

    @staticmethod
    def __str_to_int(message: list):
        """
        某些数据的真实形式是整型，进行转化
        :param message: 分割字符串之后单行记录形成的列表
        :return: 元组
        """
        nums = [0, 1, 4]
        for num in nums:
            message[num] = int(message[num])
        return message

    def is_in_old_filenames(self, filename: str):
        """
        查询是否在已有文件中
        1. 执行search_by_old_name(filename)获取存在性
        :param filename: 待查询文件名
        :return: bool，查询结果
        """
        ret = self.search_by_old_name(filename)
        if len(ret) == 0:
            return False
        else:
            return True

    def search_by_id_num(self, keyword: int):
        """
        基于id和num查找记录
        :param keyword: 查找关键字
        :return: list<RecordLine>
        """
        tempRecordLines = list()
        for record_line in self.__recordLines:
            identity, num = record_line.get_id(), record_line.get_num()
            if keyword in [identity, num]:
                tempRecordLines.append(record_line)
        return tempRecordLines

    def search_by_old_name(self, filename: str):
        """
        查询现有记录中是旧名称是filename的项
        :param filename: 旧的文件名称
        :return: 搜索结果
        """
        tempRecordLines = list()
        for recordLine in self.__recordLines:
            if filename in recordLine.get_old_name():
                tempRecordLines.append(recordLine)
        return tempRecordLines

    def get_all_record_lines(self):
        """
        获取RecordLine形式的列表，用于存储方式转换
        :return: list<RecordLine>
        """
        return self.__recordLines

    def append_filenames(self, record_lines: list):
        """
        向文件中写入新增数据
        1. 逐个获取适合存储的元组
        2. 将元组信息转换成字符串，便于存储
        3. 写入文件
        :param record_lines: 新获取的RecordLine对象列表
        :return: 暂无
        """
        with open(self.__filename, "a") as file:
            for line in record_lines:
                self.__recordLines.append(line)
                message_tuple = line.return_storage_tuple()
                message_str = self.__message_tuple_to_str(message_tuple)
                file.write(message_str)

    @staticmethod
    def __message_tuple_to_str(message_tuple: tuple):
        """
        生成适合直接写入文件的字符串，并添加分隔符
        :param message_tuple: 从RecordLine对象获取的信息元组
        :return: 适合写入文件的字符串
        """
        message_str = '\n'
        for message in message_tuple:
            message_str += str(message) + '\t'
        else:
            message_str.rstrip('\t')
        return message_str

    def delete_filenames(self, identities: list):
        # 记录删除的数据
        unusedIdentityAndNumber = self.__generate_unused_id_num(identities)

        # 移除待删除元素
        for i in reversed(range(len(self.__recordLines))):
            identity = self.__recordLines[i].get_id()
            if identity in identities:
                del self.__recordLines[i]
        else:
            # 使用覆盖写模式更新文件
            with open(self.__filename, "w") as file:
                # 写入表头
                file.write(self.__tableHead)

                # 写入更新后数据
                for recordLine in self.__recordLines:
                    messageTuple = recordLine.return_storage_tuple()
                    messageStr = self.__message_tuple_to_str(messageTuple)
                    file.write(messageStr)

        # 返回统计到的已删除的identity和number，用于后续使用
        return unusedIdentityAndNumber

    def __generate_unused_id_num(self, identities: list):
        unusedIdentityAndNumber = [[], [], []]
        for recordLine in self.__recordLines:
            identity = recordLine.get_id()
            if identity in identities:
                unusedIdentityAndNumber[0].append(identity)
                number = recordLine.get_num()
                if recordLine.get_layout() is ImageLayout.horizontal:
                    unusedIdentityAndNumber[1].append(number)
                if recordLine.get_layout() is ImageLayout.vertical:
                    unusedIdentityAndNumber[2].append(number)
        return unusedIdentityAndNumber

    def delete_storage_file(self):
        os.remove(self.__filename)
