from abc import ABCMeta, abstractmethod


class FilenameManager:
    """
    FilenameManager:文件名称管理类，两个子类
    1. 数据库
    2. 纯文本文件
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __generate_record_file(self):
        pass

    @abstractmethod
    def is_in_old_filenames(self, filename: str):
        pass

    @abstractmethod
    def append_filenames(self, record_lines: list):
        pass

    @abstractmethod
    def get_all_record_lines(self):
        pass

    @abstractmethod
    def search_by_id_num(self, keyword: int):
        pass

    # 基于原始名称查找
    @abstractmethod
    def search_by_old_name(self, filename: str):
        pass

    @abstractmethod
    def delete_filenames(self, identities: list):
        pass

    @abstractmethod
    def delete_storage_file(self):
        pass
