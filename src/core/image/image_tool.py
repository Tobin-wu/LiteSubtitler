# coding: utf8
from PIL import Image, ImageDraw


class ImageTool:

    @staticmethod
    def resize_image(input_image_path, output_image_path, size):
        """
        重新设置图片的大小。

        :param input_image_path: 输入图像文件的路径
        :param output_image_path: 输出图像文件的路径
        :param size: 输出尺寸，格式为(length, width)
        """
        try:
            # 打开图像文件
            with Image.open(input_image_path) as img:
                # 保存截取后的图像
                resized_img = img.resize(size)
                resized_img.save(output_image_path)
                print(f"图像已成功重置尺寸并保存到 {output_image_path}")
        except Exception as e:
            print(f"处理图像时发生错误: {e}")

    @staticmethod
    def crop_resize_image(input_image_path, output_image_path, crop_box, size):
        """
        从图像文件中截取一部分并重置尺寸之后保存。

        :param input_image_path: 输入图像文件的路径
        :param output_image_path: 输出截取后图像文件的路径
        :param crop_box: 截取区域，格式为(left, upper, right, lower)
        :param size: 输出尺寸，格式为(length, width)
        """
        try:
            # 打开图像文件
            with Image.open(input_image_path) as img:
                # 截取图像的一部分
                cropped_img = img.crop(crop_box)
                out_img = cropped_img.resize(size)
                # 保存截取后的图像
                out_img.save(output_image_path)
                print(f"图像已成功截取并重置大小之后保存到 {output_image_path}")
        except Exception as e:
            print(f"处理图像时发生错误: {e}")

    @staticmethod
    def crop_image(input_image_path, output_image_path, crop_box):
        """
        从图像文件中截取一部分并保存。

        :param input_image_path: 输入图像文件的路径
        :param output_image_path: 输出截取后图像文件的路径
        :param crop_box: 截取区域，格式为(left, upper, right, lower)
        """
        try:
            # 打开图像文件
            with Image.open(input_image_path) as img:
                # 截取图像的一部分
                cropped_img = img.crop(crop_box)
                # 保存截取后的图像
                cropped_img.save(output_image_path)
                print(f"图像已成功截取并保存到 {output_image_path}")
        except Exception as e:
            print(f"处理图像时发生错误: {e}")

    @staticmethod
    def make_rounded_corners(image_path, output_path, radius):
        """
        将方形图片的四个角变成圆角。

        :param image_path: 输入方形图片文件的路径
        :param output_path: 输出圆角方形图片文件的路径
        :param radius: 圆角的半径大小
        """
        try:
            # 打开原始图片
            with Image.open(image_path) as img:
                # 创建一个与原始图片大小相同的白色蒙版
                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                # 在蒙版上画一个圆角矩形，填充为白色（255）
                draw.rounded_rectangle((0, 0) + img.size, radius, fill=255)
                # 将原始图片与蒙版进行合成，只保留圆角部分
                img.putalpha(mask)

                # 如果没有alpha通道，则需要创建一个带alpha通道的新图片并粘贴原始图片和蒙版
                # 如果原始图片已经有alpha通道，上面的putalpha调用就足够了
                # 但为了通用性，这里展示如何创建一个新的带alpha通道的图片
                # background = Image.new('RGBA', img.size, (255, 255, 255, 0))  # 透明背景
                # background.paste(img, (0, 0), img)
                # img = background.convert('RGB')  # 如果不需要透明背景，可以转换回RGB模式

                # 保存结果图片，注意格式需要支持透明度（如PNG）
                img.save(output_path, 'PNG')
                print(f"圆角方形图片已成功保存到 {output_path}")
        except Exception as e:
            print(f"处理图片时发生错误: {e}")

    @staticmethod
    def overlay_image_center(base_image_path, overlay_image_path, output_image_path):
        """
        将覆盖图像放置在基础图像的最中间区域并保存结果。

        :param base_image_path: 基础图像文件的路径
        :param overlay_image_path: 覆盖图像文件的路径
        :param output_image_path: 输出图像的路径
        """
        try:
            # 打开基础图像
            base_image = Image.open(base_image_path)
            base_width, base_height = base_image.size

            # 打开覆盖图像
            overlay_image = Image.open(overlay_image_path)
            overlay_width, overlay_height = overlay_image.size

            # 计算覆盖图像应该放置的左上角坐标
            left = (base_width - overlay_width) // 2
            top = (base_height - overlay_height) // 2
            right = left + overlay_width
            bottom = top + overlay_height

            # 将覆盖图像粘贴到基础图像上
            base_image.paste(overlay_image, (left, top), overlay_image)

            # 保存结果图像
            base_image.save(output_image_path)
            print(f"图像已成功覆盖并保存到 {output_image_path}")
        except Exception as e:
            print(f"处理图像时发生错误: {e}")

#
# base_image_path = '使用群.jpg'  # 基础图像文件路径
# overlay_image_path = 'logo.png'  # 覆盖图像文件路径
#
# # 1、从原图片中截取出二维码，并调整尺寸；
# # 截取区域 (left, upper, right, lower)
# crop_box = (174, 576, 905, 1307)  # 二维码（周边多出一个像素， 731 * 731）
# size = (201, 201)
# resize_qrcode_path = '使用群_resize.png'  # 输出图像文件路径
# ImageTool.crop_resize_image(base_image_path, resize_qrcode_path, crop_box, size)
#
# # 2、把logo的尺寸调整为二维码中间的微信图标大小；
# resize_image_path = 'logo_resize.png'
# ImageTool.resize_image(overlay_image_path, resize_image_path, (49, 49))
#
# # 3、把调整大小的logo进行圆角处理；
# logo_image_path = 'logo.png'
# ImageTool.make_rounded_corners(resize_image_path, logo_image_path, 9)
#
# # 4、把圆角logo覆盖到二维码的中间, 并输出处理后的图片；
# qrcode_image_path = '使用群.png'
# ImageTool.overlay_image_center(resize_qrcode_path, logo_image_path, qrcode_image_path)
