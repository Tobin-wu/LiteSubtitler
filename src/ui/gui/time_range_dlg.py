import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QLine
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)


class TimeRangeDialog(QDialog):

    def __init__(self, max_time, parent=None):
        super().__init__(parent)

        self.edtStart = None
        self.edtEnd = None

        self.result_str = None

        self.max_time = int(max_time)
        self.setWindowTitle("时间范围选择")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 最大时间提示
        max_time_label = QLabel(f"最大允许时间: {self.max_time}秒")
        layout.addWidget(max_time_label)

        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line1.setObjectName("line1")
        layout.addWidget(line1)

        # 开始时间输入
        start_label = QLabel("开始时间 (秒):")
        self.edtStart = QLineEdit()
        self.edtStart.setPlaceholderText("0")
        layout.addWidget(start_label)
        layout.addWidget(self.edtStart)

        # 结束时间输入
        end_label = QLabel("结束时间 (秒):")
        self.edtEnd = QLineEdit()
        self.edtEnd.setPlaceholderText(str(self.max_time))
        layout.addWidget(end_label)
        layout.addWidget(self.edtEnd)

        # 确认按钮
        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        # 获取输入值
        start_text = self.edtStart.text().strip()
        end_text = self.edtEnd.text().strip()

        # 处理空输入
        start_time = 0 if not start_text else start_text
        end_time = self.max_time if not end_text else end_text

        try:
            # 转换为整数
            start_time = int(start_time)
            end_time = int(end_time)

            # 验证范围
            if start_time < 0:
                raise ValueError("开始时间不能为负数")
            if end_time > self.max_time:
                raise ValueError(f"结束时间不能超过最大时间 {self.max_time}秒")
            if start_time > end_time:
                raise ValueError("开始时间不能大于结束时间")

            # 保存结果并关闭对话框
            self.result_str = f"between(t, {start_time}, {end_time})"
            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))

    @staticmethod
    def get_time_range(max_time, parent=None):
        dialog = TimeRangeDialog(max_time, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.result_str
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 示例使用，最大时间设为100秒
    result = TimeRangeDialog.get_time_range(100)
    if result:
        print("返回的字符串:", result)

    sys.exit(app.exec())