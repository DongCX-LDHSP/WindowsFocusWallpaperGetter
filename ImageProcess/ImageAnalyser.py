from Enumerations import ImageFormat, ImageLayout
from PIL import Image


class ImageAnalyser:
    """
    ImageAnalyser:图片分析类
    用于分析图片版式及图片格式
    """
    def __init__(self):
        pass

    @staticmethod
    def __open_image(image_location: str):
        """
        打开图片，并获取图片宽度和格式
        1. 使用Pillow库中的Image模块打开图片
        2. 若打开成功则获取图片宽度和格式，否则跳转到4
        3. 返回结果
        4. 返回异常结果
        :param image_location: 图片的存储路径
        :return: 元组，(int, str) (宽度，格式)
        """
        try:
            with Image.open(image_location) as image:
                width = image.width
                image_format = image.format
                return width, image_format
        except OSError:
            return 0, ''

    @staticmethod
    def __convert_format_to_enum(format_string: str):
        """
        将某一格式的字符串转换成枚举类型并返回
        :param format_string: 格式的字符串
        :return: ImageFormat
        """
        format_string = format_string.lower()
        if format_string == 'jpg' or format_string == 'jpeg':
            return ImageFormat.jpg
        if format_string == 'png':
            return ImageFormat.png
        if format_string == 'gif':
            return ImageFormat.gif
        if format_string == 'bmp':
            return ImageFormat.bmp
        return ImageFormat.unknown

    @staticmethod
    def distinguish_image(image_location: str):
        """
        辨识图片版式和图片格式并返回
        1. 获取图片宽度及格式
        2. 基于宽度进行处理
        3. 返回处理结果
        :param image_location: 图片的存储路径
        :return: 元组，(ImageLayout, ImageFormat) (图片版式，图片格式)
        """
        width, image_format = ImageAnalyser.__open_image(image_location)
        if width != 0:
            image_format_enum = ImageAnalyser.__convert_format_to_enum(image_format)
            if width == 1920 or width == 2000:
                return ImageLayout.horizontal, image_format_enum
            if width == 1080:
                return ImageLayout.vertical, image_format_enum
            return ImageLayout.unknown, image_format_enum
        return ImageLayout.invalidFile, ImageFormat.other
