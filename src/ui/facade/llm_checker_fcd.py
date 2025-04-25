# coding: utf8

import openai
from PyQt6.QtCore import pyqtSlot, QTime, QEventLoop
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor, QFont, QIcon
from PyQt6.QtWidgets import QDialog, QApplication

from config import ICON_REC
from core.asr.asr_data import ASRData
from core.asr.asr_data_builder import AsrDataBuilder
from core.base_object import BaseObject
from enums.language_enums import SubtitleLanguageEnum
from enums.supported_subtitle_enum import SupportedSubtitleEnum
from enums.translate_mode_enum import TranslateModeEnum
from service.translate_service import TranslateService
from ui.driver.ai_chat_thread import AIChatThread
from ui.driver.ai_translate_thread import AiTranslateThread
from ui.driver.gui_tool import GuiTool
from ui.gui.llm_checker_dlg import Ui_dlgLlmChecker
from utils.file_utils import FileUtils


class LlmCheckerFacade(BaseObject):
    """LLM工具的外观类。"""

    def __init__(self, func_write_log, config, icon: QIcon = None):
        """初始化实例。"""
        super().__init__(log_to_ui_func=func_write_log)

        self.translate_service = TranslateService(log_to_ui_func=func_write_log,
                                                  callback=self.update_to_cell)  # 翻译服务

        self.dialog = QDialog()
        self.ui_dialog = Ui_dlgLlmChecker()
        self.ui_dialog.setupUi(self.dialog)

        self.ui_dialog.btnRun.setIcon(GuiTool.build_icon(ICON_REC.get('run')))
        self.ui_dialog.btnSavePrompt.setIcon(GuiTool.build_icon(ICON_REC.get('save')))
        self.ui_dialog.btnSaveAs.setIcon(GuiTool.build_icon(ICON_REC.get('save-as')))
        self.ui_dialog.btnOpenDemo.setIcon(GuiTool.build_icon(ICON_REC.get('open')))
        self.ui_dialog.btnLlmRefresh.setIcon(GuiTool.build_icon(ICON_REC.get('refresh')))
        self.ui_dialog.btnSendMsg.setIcon(GuiTool.build_icon(ICON_REC.get('send')))

        # self.ui_dialog.btnRun.clicked.connect(self._on_run_translate_)
        self.ui_dialog.btnRun.clicked.connect(self._on_save_word_)

        self.ui_dialog.btnSavePrompt.clicked.connect(self._on_save_prompt_)
        self.ui_dialog.btnSaveAs.clicked.connect(self._on_save_as_prompt_)
        self.ui_dialog.btnOpenDemo.clicked.connect(self._on_open_subtitle_)
        self.ui_dialog.btnLlmRefresh.clicked.connect(self._on_refresh_llm_models_)
        self.ui_dialog.btnSendMsg.clicked.connect(self._on_send_chat_msg_)

        self.config_args = config
        self.asr_data: ASRData = None

        self.chat_thread = None  # 聊天线程
        self.current_chat_msgs = []  # 当前聊天记录
        self.history_chat_msgs = []  # 历史聊天记录

        # 输入提示
        self.ui_dialog.edtChatMsg.setPlaceholderText("输入您的问题...")
        self.ui_dialog.edtChatMsg.setFocus()

        self.ui_dialog.edtBaseUrl.setText(self.config_args["base_url"])
        self.ui_dialog.edtAPiKey.setText(self.config_args["api_key"])
        self.ui_dialog.edtBaseUrl.textChanged.connect(self._on_llm_changed_)
        self.ui_dialog.edtAPiKey.textChanged.connect(self._on_llm_changed_)

        self.client = self._build_new_client_()

        if "models" in self.config_args:
            GuiTool.init_combobox(combobox=self.ui_dialog.cbbLlmModel,
                                  values={item: item for item in self.config_args["models"]})

        GuiTool.init_combobox(combobox=self.ui_dialog.cbbPrompt,
                              values=self.config_args["PROMPT_FILES"],
                              on_combobox_changed=self._load_prompt_)
        self._load_prompt_()

        GuiTool.init_combobox(combobox=self.ui_dialog.cbbTargetLanguage,
                              values={val.value: val.name for val in SubtitleLanguageEnum})

        self.model = self._build_tableview_model_()

    def show(self) -> None:
        """显示。"""
        self.dialog.exec()

    def _on_llm_changed_(self):
        self.llm_changed = True

    def _build_new_client_(self):
        self.llm_changed = False
        return openai.OpenAI(
            base_url=self.ui_dialog.edtBaseUrl.text(),
            api_key=self.ui_dialog.edtAPiKey.text(),
            timeout=180
        )

    @pyqtSlot()
    def _on_send_chat_msg_(self):
        """发送消息并启动聊天线程"""
        user_input = self.ui_dialog.edtChatMsg.toPlainText().strip()
        if not user_input:
            return

        # 显示用户消息
        self._add_chat_message_(user_input, is_user=True)
        self.ui_dialog.edtChatMsg.clear()

        # 准备API请求
        user_message = {"role": "user", "content": user_input}
        self.current_chat_msgs.append(user_message)

        # 停止之前的线程（如果有）
        if self.chat_thread and self.chat_thread.is_running:
            self.chat_thread.stop()

        if self.ui_dialog.ckbHistory.isChecked():
            chat_msgs = self.current_chat_msgs[-(self.ui_dialog.spbHistoryNum.value() + 1):]
        else:
            chat_msgs = [user_message]
        prompt = self.ui_dialog.txtPrompt.toPlainText()
        if self.ui_dialog.ckbUsePrompt.isChecked() and prompt:
            chat_msgs.insert(
                0,
                {
                    "role": "system",
                    "content": prompt.replace("TargetLanguage", self.ui_dialog.cbbTargetLanguage.currentText())
                }
            )
        if self.llm_changed:
            self.client = self._build_new_client_()
        if not self.chat_thread:
            # 启动新线程
            self.chat_thread = AIChatThread(ai_client=self.client,
                                            chat_msg=chat_msgs,
                                            model=self.ui_dialog.cbbLlmModel.currentText(),
                                            user_msg=user_input)
            self.chat_thread.message_signal.connect(self.update_chat_display)
            self.chat_thread.end_signal.connect(self.when_chat_msg_end)
        else:
            self.chat_thread.init_client_msg(
                ai_client=self.client,
                chat_msg=chat_msgs,
                model=self.ui_dialog.cbbLlmModel.currentText(),
                user_msg=user_input)

        self._add_chat_message_(None, is_user=False)
        self.chat_thread.start()

    def _add_chat_message_(self, message, is_user=True):
        """添加消息到聊天记录"""
        # 添加时间戳
        timestamp = QTime.currentTime().toString("hh:mm")
        self._append_text_(f"[{timestamp}] \n", QColor(128, 128, 128))  # 灰色时间戳

        # 添加发言人标识
        speaker = "我" if is_user else "AI"
        color = QColor("purple") if is_user else QColor(255, 127, 0)  # 紫色为用户，橙色为AI
        self._append_text_(f"{speaker}: \n", color, bold=True)

        if message:
            # 添加消息内容
            self._append_text_(message + "\n\n", color)  # QColor(0, 0, 0)

    def _append_text_(self, text, color=QColor(0, 0, 0), bold=False):
        """辅助方法：追加带格式的文本"""
        cursor = self.ui_dialog.txtShowMsg.textCursor()
        txt_format = QTextCharFormat()
        txt_format.setForeground(color)
        if bold:
            txt_format.setFontWeight(QFont.Weight.Bold)
        cursor.mergeCharFormat(txt_format)
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text, txt_format)
        self.ui_dialog.txtShowMsg.setTextCursor(cursor)
        self.ui_dialog.txtShowMsg.ensureCursorVisible()

    @pyqtSlot(str, str)
    def when_chat_msg_end(self, user_msg: str, ai_msg: str):
        self.current_chat_msgs.append({"role": "assistant", "content": ai_msg})
        self.history_chat_msgs.extend([user_msg, ai_msg])

        self._append_text_(text=f"\n----------------------------------------\n")

    @pyqtSlot(str)
    def update_chat_display(self, message: str):
        if message.startswith("AI: "):
            self._append_text_(text=message[4:])
        else:
            self._append_text_(text=f"{message}\n")

    def closeEvent(self, event):
        """窗口关闭时停止线程"""
        if self.chat_thread and self.chat_thread.is_running:
            self.chat_thread.stop()
        event.accept()

    def _on_save_prompt_(self):
        FileUtils.write_text(
            file_path=self._read_prompt_file_path_(),
            text=self.ui_dialog.txtPrompt.toPlainText()
        )

    def _on_save_as_prompt_(self):
        file_path = GuiTool.save_dialog(parent=self.dialog,
                                        filter_str="Text Files (*.txt)")
        if file_path:
            FileUtils.write_text(
                file_path=file_path,
                text=self.ui_dialog.txtPrompt.toPlainText()
            )
            self.log_info(f"另存到：{file_path}")

    def _on_refresh_llm_models_(self) -> None:
        self._load_llm_models(
            base_url=self.ui_dialog.edtBaseUrl.text(),
            api_key=self.ui_dialog.edtAPiKey.text(),
            current_model=self.ui_dialog.cbbLlmModel.currentText()
        )

    def _load_llm_models(self, base_url: str, api_key: str, current_model: str) -> None:
        """加载LLM模型列表。

        Args:
            base_url (str): LLM API的基础URL。
            api_key (str): LLM API的密钥。
            current_model (str): 当前选中的模型。
        """
        try:
            cnt = GuiTool.load_llm_models(
                cbb_llm_model=self.ui_dialog.cbbLlmModel,
                base_url=base_url,
                api_key=api_key,
                current_model=current_model
            )
            if cnt > 0:
                self.log_info(f"读取LLM模型列表成功, 共 {cnt} 个模型。")
        except Exception as e:
            self.log_error(f"读取LLM模型列表发生异常", e)

    def _load_prompt_(self):
        self.ui_dialog.txtPrompt.setText(FileUtils.read_text(input_file_path=self._read_prompt_file_path_()))

    def _read_prompt_file_path_(self) -> str:
        return str(self.ui_dialog.cbbPrompt.currentData())

    def _on_open_subtitle_(self):
        subtitle_formats = SupportedSubtitleEnum.filter_formats()
        file_path, _ = GuiTool.select_file_dialog(parent=self.dialog, filter_str=f"字幕文件 ({subtitle_formats})")
        if file_path:
            self.asr_data = AsrDataBuilder.from_subtitle_file(file_path=str(file_path))
            self._reset_subtitle_tableview_()

    def _build_tableview_model_(self):
        data = [
            ['0', '*', '', '', '', '']
        ]
        headers = ['id', '源字幕', '直译', '精细', '深思', '-']
        sizes = [80, 400, 400, 400, 400]
        return GuiTool.build_tv_model(tv=self.ui_dialog.tbvDemo,
                                      data=data,
                                      headers=headers,
                                      sizes=sizes)

    def _reset_subtitle_tableview_(self):
        """构建表格视图模型。"""
        self.model.clear()
        if self.asr_data:
            for i, seg in enumerate(self.asr_data.segments):
                self.model.append_row([str(i), seg.text, '', '', '', ''])

    def _on_save_word_(self) -> None:
        file_path = GuiTool.save_dialog(parent=self.dialog,
                                        filter_str="Text Files (*.txt)")
        if file_path:
            result = []
            for n, seg in enumerate(self.asr_data.segments, 1):
                result.append(f'{seg.text}\n')

            FileUtils.write_text(
                file_path=file_path,
                text="\n".join(result)
            )
            self.log_info(f"另存到：{file_path}")

    def _on_run_translate_(self) -> None:
        import copy

        thread = AiTranslateThread(service=self.translate_service,
                                   asr_data=copy.deepcopy(self.asr_data),
                                   config={
                                       "need_translate": True,  # 是否翻译
                                       "translate_mode": "",
                                       "source_language": "",  # 源语言
                                       "target_language": self.ui_dialog.cbbTargetLanguage.currentText(),  # 目标语言
                                       "llm_api_url": self.ui_dialog.edtBaseUrl.text(),
                                       "llm_api_key": self.ui_dialog.edtAPiKey.text(),
                                       "llm_model": self.ui_dialog.cbbLlmModel.currentText(),
                                       "need_remove_punctuation": True  # 是否删除句子中的符号
                                   })
        thread.message_signal.connect(self._translate_msg_display_)
        # thread.end_signal.connect(self._write_to_tv_)

        thread.start()

    def _translate_msg_display_(self, msg: str):
        self.log_warning(f"AI翻译：{msg}")

    def _write_to_tv_(self, mode: TranslateModeEnum, asr_data: ASRData) -> None:
        if asr_data:
            for i, seg in enumerate(asr_data.segments):
                if "\n" in seg.transcript:
                    original, translated = seg.transcript.split("\n", 1)
                else:
                    original, translated = seg.transcript, ""
                self.update_to_cell(mode, str(i), translated if translated else original)

    def update_to_cell(self, mode: TranslateModeEnum, rowid: str, msg: str):
        if "\n" in msg:
            original, translated = msg.split("\n", 1)
        else:
            original, translated = msg, ""
        text = translated if translated else original

        if mode == TranslateModeEnum.FAST:
            self.model.update_cell(rowid, 2, text)
        elif mode == TranslateModeEnum.PRECISE:
            self.model.update_cell(rowid, 3, text)
        else:
            self.model.update_cell(rowid, 4, text)

        QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
