from ImageProcess.ImageCopier import ImageCopier
from SettingsAnalyser import SettingsAnalyser
from FilenameManager.TextFile import TextFile
from FilenameManager.Database import Database
from Enumerations import SearchMode, ExecuteMessage, ResetMessage, StorageMethod


class Controller:
    @staticmethod
    def check_storage_folder():
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            storageFolder = settingsAnalyser.get_storage_folder()
            if storageFolder == "":
                return ExecuteMessage.success, "请设置存储路径以便开始使用程序！"
            else:
                return ExecuteMessage.success, ""
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def get_focus_wallpaper():
        """
        获取新的WindowsFocusWallpaper
        1. 载入设置
        2. 获取存储方式
        3. 基于存储方式实例化FilenameManager的子类
        4. 实例化ImageCopier对象，准备拷贝
        5. 拷贝文件，并获取新增的图片数量
        6. 更新设置文件中存储的图片数量
        7. 更新情况提示输出
        :return: 提示信息
        """
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            storageMethod = settingsAnalyser.get_storage_method()
            if storageMethod is not StorageMethod.unknown:
                filenameManager = Controller.generate_filename_manager(
                    storageMethod, settingsAnalyser.get_storage_folder())
                imageCopier = ImageCopier(settingsAnalyser.get_source_folder(),
                                          settingsAnalyser.get_storage_folder(),
                                          (settingsAnalyser.get_horizontal_number(),
                                           settingsAnalyser.get_vertical_number()),
                                          settingsAnalyser.get_unused_identity_and_number(),
                                          filenameManager)
                imageCounter, numCounter = imageCopier.copy_wallpaper()
                ret = settingsAnalyser.refresh_number(*numCounter)
                if ret is ResetMessage.success:
                    if imageCounter == [0, 0]:
                        return ExecuteMessage.success, "没有新增图片！"
                    else:
                        return ExecuteMessage.success, "新获取:\n{}张横版壁纸！\n" \
                                                       "{}张竖版壁纸！".format(*imageCounter)
                elif ret is ResetMessage.fileNotFound:
                    return ExecuteMessage.success, "但设置文件因未知原因找不到！\n未能更新设置文件！"
            else:
                return ExecuteMessage.failure, "未知的存储方式，请检查设置文件！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def generate_filename_manager(storage_method: StorageMethod, storage_folder: str):
        filenameManager = FilenameManager()
        if storage_method is StorageMethod.textFile:
            filenameManager = TextFile(storage_folder)
        elif storage_method is StorageMethod.database:
            filenameManager = Database()
        return filenameManager

    @staticmethod
    def look_record():
        """
        查看已有的记录
        :return: 若返回列表为空则意味着无记录，若返回值为None则是存储方式未知
        """
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            storageMethod = settingsAnalyser.get_storage_method()
            if storageMethod is not StorageMethod.unknown:
                filenameManager = Controller.generate_filename_manager(
                    storageMethod, settingsAnalyser.get_storage_folder())
                recordLines = filenameManager.get_all_record_lines()
                return ExecuteMessage.success, recordLines
            return ExecuteMessage.failure, "未知的存储方式！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def set_storage_folder(new_location: str, move_wallpaper: bool, init: bool = False):
        """
        用于完成一整套重设存储文件夹的流程
        :param init: 是否是被初始化存储路径调用的
        :param new_location: 新的存储路径
        :param move_wallpaper: 是否自动转移已有壁纸
        :return: 暂无
        """
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            oldStorageFolder = settingsAnalyser.get_storage_folder()
            ret = settingsAnalyser.set_storage_folder(new_location)
            if ret is ResetMessage.success:
                if init is False:
                    # 更新成功
                    if move_wallpaper is True:
                        # 用户期望自动转移壁纸，则转移
                        ImageCopier.move_wallpaper(oldStorageFolder, new_location)
                    elif settingsAnalyser.get_storage_method() is StorageMethod.textFile:
                        ImageCopier.move_filename_storage(oldStorageFolder, new_location)
                    # 用户不期望自动转移壁纸，则略过，目录结构会在必要时会自动建立
                    # 也不必更新设置文件中的图片已有数量
                return ExecuteMessage.success, "设置成功!"
            if ret is ResetMessage.fileNotFound:
                return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"
            if ret is ResetMessage.locationNotExist:
                return ExecuteMessage.failure, "路径不存在！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def get_storage_folder():
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            return ExecuteMessage.success, settingsAnalyser.get_storage_folder()
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def reset_source_folder():
        """
        重设壁纸源文件夹，因为这个路径是固定的，故不需提供参数
        :return: 提示信息
        """
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            ret = settingsAnalyser.reset_source_folder()
            if ret is ResetMessage.success:
                return ExecuteMessage.success, "重置成功！\n以后不要乱修改了哦~"
            if ret is ResetMessage.fileNotFound:
                return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def set_storage_method(new_method: StorageMethod, storage_folder: str):
        """
        设置文件名称存储方式
        1. 首先检测是否与现在的存储方式一致
        2. 若一致则跳转到5，否则跳转到3
        3. 更新存储方式
        4. 转换已有的存储信息到新的存储方式
        5. 结束
        :param storage_folder: 存储文件夹，用于初始化TextFile
        :param new_method: 新的文件名存储方式
        :return: 设置结果
        """
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            oldStorageMethod = settingsAnalyser.get_storage_method()
            # 对已经保存的存储信息进行转化
            if oldStorageMethod is not new_method:
                ret = settingsAnalyser.set_storage_method(new_method)
                if ret is ResetMessage.success:
                    Controller.convert_storage_method(new_method, storage_folder)
                    return ExecuteMessage.success, "成功设置为：{}".format(
                        "数据库" if new_method is StorageMethod.database else "纯文本文件")
                return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"
            return ExecuteMessage.failure, "你选择了当前设置！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def convert_storage_method(new_method: StorageMethod, storage_folder: str):
        oldMethod = FilenameManager()
        newMethod = FilenameManager()
        if new_method is StorageMethod.database:
            oldMethod = TextFile(storage_folder)
            newMethod = Database()
        elif new_method is StorageMethod.textFile:
            oldMethod = Database()
            newMethod = TextFile(storage_folder)
        recordLines = oldMethod.get_all_record_lines()
        newMethod.append_filenames(recordLines)

        # 删除旧方式使用的存储文件/数据库
        oldMethod.delete_storage_file()

    @staticmethod
    def get_storage_method():
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            return ExecuteMessage.success, settingsAnalyser.get_storage_method()
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def search_image(keyword: str, mode: SearchMode):
        """
        检索已有图片，供用户筛选操作
        :param mode: 搜索模式
        :param keyword: 检索关键字，可以是id，也可以是num
        :return: 待定
        """
        if keyword == "":
            return ExecuteMessage.failure, "关键词不能为空！"
        if mode is SearchMode.oldFilename:
            if len(keyword) > 64:
                return ExecuteMessage.failure, "在原始文件名称搜索模式下\n输入数据不能超出64位!"
        elif mode is SearchMode.idAndNum:
            if keyword.isdigit() is False:
                return ExecuteMessage.failure, "在id或编号搜索模式下\n输入数据只能包含数字!"
        # 基于存储方式生成相应对象的实例
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            storageMethod = settingsAnalyser.get_storage_method()
            if storageMethod is not StorageMethod.unknown:
                filenameManager = Controller.generate_filename_manager(
                    storageMethod, settingsAnalyser.get_storage_folder())
                if mode is SearchMode.oldFilename:
                    ret = filenameManager.search_by_old_name(keyword)
                elif mode is SearchMode.idAndNum:
                    ret = filenameManager.search_by_id_num(int(keyword))
                if len(ret) > 0:
                    return ExecuteMessage.success, ret
                else:
                    return ExecuteMessage.failure, "未找到任何记录！"
            return ExecuteMessage.failure, "未知的存储方式！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"

    @staticmethod
    def delete_image(identities: list):
        settingsAnalyser = SettingsAnalyser()
        initialResult = settingsAnalyser.get_initial_result()
        if initialResult is ResetMessage.success:
            storageMethod = settingsAnalyser.get_storage_method()
            storageFolder = settingsAnalyser.get_storage_folder()
            if storageMethod is not StorageMethod.unknown:
                filenameManager = Controller.generate_filename_manager(storageMethod, storageFolder)
                unusedIdentityAndNumber = filenameManager.delete_filenames(identities)
                ImageCopier.delete_wallpaper(storageFolder, unusedIdentityAndNumber[1:3])
                settingsAnalyser.add_unused_identity_and_number(unusedIdentityAndNumber)
                return ExecuteMessage.success, "删除了{}张壁纸！".format(len(identities))
            else:
                return ExecuteMessage.failure, "未知的存储方式！"
        elif initialResult is ResetMessage.fileNotFound:
            return ExecuteMessage.failure, "未找到设置文件！\n重新部署可能会解决该问题！"
