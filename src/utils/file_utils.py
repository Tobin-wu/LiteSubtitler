# coding: utf8


class FileUtils:
    """文件工具类，提供文件相关的常用方法。"""

    @staticmethod
    def convert_to_unix_format(input_file_path: str, output_file_path: str) -> bool:
        """将文件的换行符从 Windows 格式（\r\n）转换为 Unix 格式（\n）。

        Args:
            input_file_path (str): 输入文件的路径。
            output_file_path (str): 输出文件的路径。

        Returns:
            bool: 转换是否成功。成功返回 True，失败返回 False。
        """
        try:
            # 读取输入文件内容
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()

            # 替换所有的 \r\n 为 \n
            unix_content = content.replace('\r\n', '\n')

            # 将转换后的内容写入输出文件
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(unix_content)

            return True
        except Exception as e:
            print(f"文件转换失败: {e}")
            return False
