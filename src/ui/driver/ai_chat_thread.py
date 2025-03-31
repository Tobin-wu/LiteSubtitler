# coding: utf8
import time

import openai
from PyQt6.QtCore import QThread, pyqtSignal


class AIChatThread(QThread):
    """处理AI聊天的子线程"""

    message_signal = pyqtSignal(str)  # 定义信号用于传递消息
    end_signal = pyqtSignal(str, str)  # 定义信号用于结束消息

    def __init__(self, ai_client, chat_msg, model: str, user_msg: str):
        super().__init__()
        self.is_running = True
        self.client: openai.OpenAI = ai_client
        self.chat_msg = chat_msg
        self.model = model
        self.user_msg = user_msg

    def init_client_msg(self, ai_client, chat_msg, model: str, user_msg: str):
        self.client = ai_client
        self.chat_msg = chat_msg
        self.model = model
        self.user_msg = user_msg

    def run(self):
        """线程执行方法"""
        self.is_running = True
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_msg,
                stream=True
            )

            ai_msg = ""

            if response.response.status_code == 200:
                for chunk in response:
                    if not self.is_running:
                        self.end_signal.emit(self.user_msg, ai_msg)
                        break
                    content = chunk.choices[0].delta.content
                    self.message_signal.emit(f"AI: {content.lstrip()}")
                    ai_msg = ai_msg + content.lstrip()
                    time.sleep(0.1)  # 控制响应速度
                self.end_signal.emit(self.user_msg, ai_msg)
            else:
                self.message_signal.emit(f"错误: 请求失败，状态码 {response.response.status_code}\n")
                self.end_signal.emit(self.user_msg, "")
        except Exception as e:
            self.message_signal.emit(f"错误: {str(e)}\n")
            self.end_signal.emit(self.user_msg, str(e))
        finally:
            self.is_running = False

    def stop(self):
        """停止线程"""
        self.is_running = False
        self.wait()
