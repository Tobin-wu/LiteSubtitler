# Form implementation generated from reading ui file 'main_frm.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_frmMain(object):
    def setupUi(self, frmMain):
        frmMain.setObjectName("frmMain")
        frmMain.resize(1307, 967)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        frmMain.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../resources/images/icons/logo-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        frmMain.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=frmMain)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1307, 971))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vlytMain = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vlytMain.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.vlytMain.setContentsMargins(0, 0, 0, 0)
        self.vlytMain.setObjectName("vlytMain")
        self.freSetting = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.freSetting.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freSetting.setObjectName("freSetting")
        self.vlytSetting = QtWidgets.QVBoxLayout(self.freSetting)
        self.vlytSetting.setContentsMargins(4, 2, 4, 2)
        self.vlytSetting.setSpacing(2)
        self.vlytSetting.setObjectName("vlytSetting")
        self.freVad = QtWidgets.QFrame(parent=self.freSetting)
        self.freVad.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freVad.setObjectName("freVad")
        self.hlytVad = QtWidgets.QHBoxLayout(self.freVad)
        self.hlytVad.setContentsMargins(10, 6, 10, 6)
        self.hlytVad.setObjectName("hlytVad")
        self.btnDownTool = QtWidgets.QPushButton(parent=self.freVad)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../resources/images/icons/下载.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnDownTool.setIcon(icon1)
        self.btnDownTool.setObjectName("btnDownTool")
        self.hlytVad.addWidget(self.btnDownTool)
        self.lblWhisperExe = QtWidgets.QLabel(parent=self.freVad)
        self.lblWhisperExe.setObjectName("lblWhisperExe")
        self.hlytVad.addWidget(self.lblWhisperExe)
        self.edtWhisperExe = QtWidgets.QLineEdit(parent=self.freVad)
        self.edtWhisperExe.setObjectName("edtWhisperExe")
        self.hlytVad.addWidget(self.edtWhisperExe)
        self.btnWhisperExe = QtWidgets.QPushButton(parent=self.freVad)
        self.btnWhisperExe.setMaximumSize(QtCore.QSize(50, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../resources/images/icons/可执行文件.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnWhisperExe.setIcon(icon2)
        self.btnWhisperExe.setObjectName("btnWhisperExe")
        self.hlytVad.addWidget(self.btnWhisperExe)
        self.chbVad = QtWidgets.QCheckBox(parent=self.freVad)
        self.chbVad.setObjectName("chbVad")
        self.hlytVad.addWidget(self.chbVad)
        self.lblVadMethod = QtWidgets.QLabel(parent=self.freVad)
        self.lblVadMethod.setObjectName("lblVadMethod")
        self.hlytVad.addWidget(self.lblVadMethod)
        self.cbbVadMethod = QtWidgets.QComboBox(parent=self.freVad)
        self.cbbVadMethod.setObjectName("cbbVadMethod")
        self.hlytVad.addWidget(self.cbbVadMethod)
        self.lblVadValue = QtWidgets.QLabel(parent=self.freVad)
        self.lblVadValue.setMinimumSize(QtCore.QSize(20, 0))
        self.lblVadValue.setMaximumSize(QtCore.QSize(70, 20))
        self.lblVadValue.setObjectName("lblVadValue")
        self.hlytVad.addWidget(self.lblVadValue)
        self.spbVadValue = QtWidgets.QDoubleSpinBox(parent=self.freVad)
        self.spbVadValue.setObjectName("spbVadValue")
        self.hlytVad.addWidget(self.spbVadValue)
        self.hlytVad.setStretch(2, 6)
        self.hlytVad.setStretch(6, 2)
        self.hlytVad.setStretch(8, 1)
        self.vlytSetting.addWidget(self.freVad)
        self.freWhisper = QtWidgets.QFrame(parent=self.freSetting)
        self.freWhisper.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freWhisper.setObjectName("freWhisper")
        self.hlytWhister = QtWidgets.QHBoxLayout(self.freWhisper)
        self.hlytWhister.setContentsMargins(10, 4, 10, 4)
        self.hlytWhister.setObjectName("hlytWhister")
        self.chbHumanVoice = QtWidgets.QCheckBox(parent=self.freWhisper)
        self.chbHumanVoice.setObjectName("chbHumanVoice")
        self.hlytWhister.addWidget(self.chbHumanVoice)
        self.lblRunDevice = QtWidgets.QLabel(parent=self.freWhisper)
        self.lblRunDevice.setObjectName("lblRunDevice")
        self.hlytWhister.addWidget(self.lblRunDevice)
        self.cbbRunDevice = QtWidgets.QComboBox(parent=self.freWhisper)
        self.cbbRunDevice.setObjectName("cbbRunDevice")
        self.hlytWhister.addWidget(self.cbbRunDevice)
        self.lblWhisperModel = QtWidgets.QLabel(parent=self.freWhisper)
        self.lblWhisperModel.setObjectName("lblWhisperModel")
        self.hlytWhister.addWidget(self.lblWhisperModel)
        self.cbbWhisperModel = QtWidgets.QComboBox(parent=self.freWhisper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbbWhisperModel.sizePolicy().hasHeightForWidth())
        self.cbbWhisperModel.setSizePolicy(sizePolicy)
        self.cbbWhisperModel.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cbbWhisperModel.setSizeIncrement(QtCore.QSize(200, 0))
        self.cbbWhisperModel.setObjectName("cbbWhisperModel")
        self.hlytWhister.addWidget(self.cbbWhisperModel)
        self.btnDownModel = QtWidgets.QPushButton(parent=self.freWhisper)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../resources/images/icons/下载模型.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnDownModel.setIcon(icon3)
        self.btnDownModel.setObjectName("btnDownModel")
        self.hlytWhister.addWidget(self.btnDownModel)
        self.lblWhisterDir = QtWidgets.QLabel(parent=self.freWhisper)
        self.lblWhisterDir.setObjectName("lblWhisterDir")
        self.hlytWhister.addWidget(self.lblWhisterDir)
        self.edtWhisperDir = QtWidgets.QLineEdit(parent=self.freWhisper)
        self.edtWhisperDir.setObjectName("edtWhisperDir")
        self.hlytWhister.addWidget(self.edtWhisperDir)
        self.btnWhisperDir = QtWidgets.QPushButton(parent=self.freWhisper)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../resources/images/icons/文件夹.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnWhisperDir.setIcon(icon4)
        self.btnWhisperDir.setObjectName("btnWhisperDir")
        self.hlytWhister.addWidget(self.btnWhisperDir)
        self.vlytSetting.addWidget(self.freWhisper)
        self.freTranslate = QtWidgets.QFrame(parent=self.freSetting)
        self.freTranslate.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freTranslate.setObjectName("freTranslate")
        self.hlytTranslate = QtWidgets.QHBoxLayout(self.freTranslate)
        self.hlytTranslate.setContentsMargins(10, 4, 10, 4)
        self.hlytTranslate.setObjectName("hlytTranslate")
        self.chbTranslate = QtWidgets.QCheckBox(parent=self.freTranslate)
        self.chbTranslate.setObjectName("chbTranslate")
        self.hlytTranslate.addWidget(self.chbTranslate)
        self.lblTranslateMode = QtWidgets.QLabel(parent=self.freTranslate)
        self.lblTranslateMode.setObjectName("lblTranslateMode")
        self.hlytTranslate.addWidget(self.lblTranslateMode)
        self.cbbTranslateMode = QtWidgets.QComboBox(parent=self.freTranslate)
        self.cbbTranslateMode.setObjectName("cbbTranslateMode")
        self.hlytTranslate.addWidget(self.cbbTranslateMode)
        self.chbClearPunctuation = QtWidgets.QCheckBox(parent=self.freTranslate)
        self.chbClearPunctuation.setObjectName("chbClearPunctuation")
        self.hlytTranslate.addWidget(self.chbClearPunctuation)
        self.lblSourceLanguage = QtWidgets.QLabel(parent=self.freTranslate)
        self.lblSourceLanguage.setObjectName("lblSourceLanguage")
        self.hlytTranslate.addWidget(self.lblSourceLanguage)
        self.cbbSourceLanguage = QtWidgets.QComboBox(parent=self.freTranslate)
        self.cbbSourceLanguage.setObjectName("cbbSourceLanguage")
        self.hlytTranslate.addWidget(self.cbbSourceLanguage)
        self.lblTargetLanguage = QtWidgets.QLabel(parent=self.freTranslate)
        self.lblTargetLanguage.setObjectName("lblTargetLanguage")
        self.hlytTranslate.addWidget(self.lblTargetLanguage)
        self.cbbTargetLanguage = QtWidgets.QComboBox(parent=self.freTranslate)
        self.cbbTargetLanguage.setObjectName("cbbTargetLanguage")
        self.hlytTranslate.addWidget(self.cbbTargetLanguage)
        self.hlytTranslate.setStretch(2, 1)
        self.hlytTranslate.setStretch(5, 1)
        self.hlytTranslate.setStretch(7, 1)
        self.vlytSetting.addWidget(self.freTranslate)
        self.freLLM = QtWidgets.QFrame(parent=self.freSetting)
        self.freLLM.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freLLM.setObjectName("freLLM")
        self.hlytLLM = QtWidgets.QHBoxLayout(self.freLLM)
        self.hlytLLM.setContentsMargins(10, 4, 10, 4)
        self.hlytLLM.setObjectName("hlytLLM")
        self.lblLLM = QtWidgets.QLabel(parent=self.freLLM)
        self.lblLLM.setObjectName("lblLLM")
        self.hlytLLM.addWidget(self.lblLLM)
        self.btnLlmApi = QtWidgets.QPushButton(parent=self.freLLM)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../resources/images/icons/注册.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnLlmApi.setIcon(icon5)
        self.btnLlmApi.setObjectName("btnLlmApi")
        self.hlytLLM.addWidget(self.btnLlmApi)
        self.lblApiKey = QtWidgets.QLabel(parent=self.freLLM)
        self.lblApiKey.setObjectName("lblApiKey")
        self.hlytLLM.addWidget(self.lblApiKey)
        self.edtAPiKey = QtWidgets.QLineEdit(parent=self.freLLM)
        self.edtAPiKey.setObjectName("edtAPiKey")
        self.hlytLLM.addWidget(self.edtAPiKey)
        self.lblBaseUrl = QtWidgets.QLabel(parent=self.freLLM)
        self.lblBaseUrl.setObjectName("lblBaseUrl")
        self.hlytLLM.addWidget(self.lblBaseUrl)
        self.edtBaseUrl = QtWidgets.QLineEdit(parent=self.freLLM)
        self.edtBaseUrl.setObjectName("edtBaseUrl")
        self.hlytLLM.addWidget(self.edtBaseUrl)
        self.btnLlmRefresh = QtWidgets.QPushButton(parent=self.freLLM)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../../resources/images/icons/更新.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnLlmRefresh.setIcon(icon6)
        self.btnLlmRefresh.setObjectName("btnLlmRefresh")
        self.hlytLLM.addWidget(self.btnLlmRefresh)
        self.lblLlmModel = QtWidgets.QLabel(parent=self.freLLM)
        self.lblLlmModel.setObjectName("lblLlmModel")
        self.hlytLLM.addWidget(self.lblLlmModel)
        self.cbbLlmModel = QtWidgets.QComboBox(parent=self.freLLM)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.cbbLlmModel.sizePolicy().hasHeightForWidth())
        self.cbbLlmModel.setSizePolicy(sizePolicy)
        self.cbbLlmModel.setObjectName("cbbLlmModel")
        self.cbbLlmModel.addItem("")
        self.hlytLLM.addWidget(self.cbbLlmModel)
        self.btnCheckApi = QtWidgets.QPushButton(parent=self.freLLM)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../../resources/images/icons/link.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnCheckApi.setIcon(icon7)
        self.btnCheckApi.setObjectName("btnCheckApi")
        self.hlytLLM.addWidget(self.btnCheckApi)
        self.hlytLLM.setStretch(3, 3)
        self.hlytLLM.setStretch(5, 2)
        self.hlytLLM.setStretch(8, 2)
        self.vlytSetting.addWidget(self.freLLM)
        self.freSubtitle = QtWidgets.QFrame(parent=self.freSetting)
        self.freSubtitle.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freSubtitle.setObjectName("freSubtitle")
        self.hlytSubtitle = QtWidgets.QHBoxLayout(self.freSubtitle)
        self.hlytSubtitle.setContentsMargins(10, 4, 10, 4)
        self.hlytSubtitle.setObjectName("hlytSubtitle")
        self.chbEmbedSubtitle = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.chbEmbedSubtitle.setObjectName("chbEmbedSubtitle")
        self.hlytSubtitle.addWidget(self.chbEmbedSubtitle)
        self.chbSoftSubtitle = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.chbSoftSubtitle.setObjectName("chbSoftSubtitle")
        self.hlytSubtitle.addWidget(self.chbSoftSubtitle)
        self.chbRemoveTempFile = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.chbRemoveTempFile.setObjectName("chbRemoveTempFile")
        self.hlytSubtitle.addWidget(self.chbRemoveTempFile)
        self.lblSubtitleLayout = QtWidgets.QLabel(parent=self.freSubtitle)
        self.lblSubtitleLayout.setObjectName("lblSubtitleLayout")
        self.hlytSubtitle.addWidget(self.lblSubtitleLayout)
        self.cbbSubtitleLayout = QtWidgets.QComboBox(parent=self.freSubtitle)
        self.cbbSubtitleLayout.setObjectName("cbbSubtitleLayout")
        self.hlytSubtitle.addWidget(self.cbbSubtitleLayout)
        self.lblSubtitleVH = QtWidgets.QLabel(parent=self.freSubtitle)
        self.lblSubtitleVH.setObjectName("lblSubtitleVH")
        self.hlytSubtitle.addWidget(self.lblSubtitleVH)
        self.spbSubtitleVH = QtWidgets.QSpinBox(parent=self.freSubtitle)
        self.spbSubtitleVH.setObjectName("spbSubtitleVH")
        self.hlytSubtitle.addWidget(self.spbSubtitleVH)
        self.hlytSubtitle.setStretch(4, 1)
        self.hlytSubtitle.setStretch(6, 1)
        self.vlytSetting.addWidget(self.freSubtitle)
        self.freMainSubtitle = QtWidgets.QFrame(parent=self.freSetting)
        self.freMainSubtitle.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freMainSubtitle.setObjectName("freMainSubtitle")
        self.hlytSubtitleMain = QtWidgets.QHBoxLayout(self.freMainSubtitle)
        self.hlytSubtitleMain.setContentsMargins(10, 4, 10, 4)
        self.hlytSubtitleMain.setObjectName("hlytSubtitleMain")
        self.lblSubtitleMain = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblSubtitleMain.setObjectName("lblSubtitleMain")
        self.hlytSubtitleMain.addWidget(self.lblSubtitleMain)
        self.lblMainFont = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblMainFont.setObjectName("lblMainFont")
        self.hlytSubtitleMain.addWidget(self.lblMainFont)
        self.cbbMainFont = QtWidgets.QFontComboBox(parent=self.freMainSubtitle)
        self.cbbMainFont.setObjectName("cbbMainFont")
        self.hlytSubtitleMain.addWidget(self.cbbMainFont)
        self.lblMainSize = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblMainSize.setObjectName("lblMainSize")
        self.hlytSubtitleMain.addWidget(self.lblMainSize)
        self.spbMainSize = QtWidgets.QSpinBox(parent=self.freMainSubtitle)
        self.spbMainSize.setObjectName("spbMainSize")
        self.hlytSubtitleMain.addWidget(self.spbMainSize)
        self.lblMainSpacing = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblMainSpacing.setObjectName("lblMainSpacing")
        self.hlytSubtitleMain.addWidget(self.lblMainSpacing)
        self.spbMainSpacing = QtWidgets.QSpinBox(parent=self.freMainSubtitle)
        self.spbMainSpacing.setObjectName("spbMainSpacing")
        self.hlytSubtitleMain.addWidget(self.spbMainSpacing)
        self.lblMainColor = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblMainColor.setObjectName("lblMainColor")
        self.hlytSubtitleMain.addWidget(self.lblMainColor)
        self.freMainColor = QtWidgets.QFrame(parent=self.freMainSubtitle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freMainColor.sizePolicy().hasHeightForWidth())
        self.freMainColor.setSizePolicy(sizePolicy)
        self.freMainColor.setMinimumSize(QtCore.QSize(50, 20))
        self.freMainColor.setMaximumSize(QtCore.QSize(50, 20))
        self.freMainColor.setStyleSheet("background-color: #5aff65; border: 1px solid black;")
        self.freMainColor.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freMainColor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.freMainColor.setObjectName("freMainColor")
        self.hlytSubtitleMain.addWidget(self.freMainColor)
        self.btnMainColor = QtWidgets.QPushButton(parent=self.freMainSubtitle)
        self.btnMainColor.setMaximumSize(QtCore.QSize(50, 16777215))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../../resources/images/icons/color.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnMainColor.setIcon(icon8)
        self.btnMainColor.setObjectName("btnMainColor")
        self.hlytSubtitleMain.addWidget(self.btnMainColor)
        self.lblMainOutlineColor = QtWidgets.QLabel(parent=self.freMainSubtitle)
        self.lblMainOutlineColor.setObjectName("lblMainOutlineColor")
        self.hlytSubtitleMain.addWidget(self.lblMainOutlineColor)
        self.freMainOutlineColor = QtWidgets.QFrame(parent=self.freMainSubtitle)
        self.freMainOutlineColor.setMinimumSize(QtCore.QSize(50, 20))
        self.freMainOutlineColor.setMaximumSize(QtCore.QSize(50, 20))
        self.freMainOutlineColor.setStyleSheet("QWidget { background-color: rgb(5, 7, 13); border: 1px solid black; }")
        self.freMainOutlineColor.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freMainOutlineColor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.freMainOutlineColor.setObjectName("freMainOutlineColor")
        self.hlytSubtitleMain.addWidget(self.freMainOutlineColor)
        self.btnMainOutlineColor = QtWidgets.QPushButton(parent=self.freMainSubtitle)
        self.btnMainOutlineColor.setMinimumSize(QtCore.QSize(50, 0))
        self.btnMainOutlineColor.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btnMainOutlineColor.setIcon(icon8)
        self.btnMainOutlineColor.setObjectName("btnMainOutlineColor")
        self.hlytSubtitleMain.addWidget(self.btnMainOutlineColor)
        self.hlytSubtitleMain.setStretch(4, 1)
        self.hlytSubtitleMain.setStretch(6, 1)
        self.vlytSetting.addWidget(self.freMainSubtitle)
        self.freSecondSubtitle = QtWidgets.QFrame(parent=self.freSetting)
        self.freSecondSubtitle.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.freSecondSubtitle.setObjectName("freSecondSubtitle")
        self.hlytSubtitleSecond = QtWidgets.QHBoxLayout(self.freSecondSubtitle)
        self.hlytSubtitleSecond.setContentsMargins(10, 4, 10, 4)
        self.hlytSubtitleSecond.setObjectName("hlytSubtitleSecond")
        self.lblSubtitleSecond = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSubtitleSecond.setObjectName("lblSubtitleSecond")
        self.hlytSubtitleSecond.addWidget(self.lblSubtitleSecond)
        self.lblSecondFont = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSecondFont.setObjectName("lblSecondFont")
        self.hlytSubtitleSecond.addWidget(self.lblSecondFont)
        self.cbbSecondFont = QtWidgets.QFontComboBox(parent=self.freSecondSubtitle)
        self.cbbSecondFont.setObjectName("cbbSecondFont")
        self.hlytSubtitleSecond.addWidget(self.cbbSecondFont)
        self.lblSecondSize = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSecondSize.setObjectName("lblSecondSize")
        self.hlytSubtitleSecond.addWidget(self.lblSecondSize)
        self.spbSecondSize = QtWidgets.QSpinBox(parent=self.freSecondSubtitle)
        self.spbSecondSize.setObjectName("spbSecondSize")
        self.hlytSubtitleSecond.addWidget(self.spbSecondSize)
        self.lblSecondSpacing = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSecondSpacing.setObjectName("lblSecondSpacing")
        self.hlytSubtitleSecond.addWidget(self.lblSecondSpacing)
        self.spbSecondSpacing = QtWidgets.QSpinBox(parent=self.freSecondSubtitle)
        self.spbSecondSpacing.setObjectName("spbSecondSpacing")
        self.hlytSubtitleSecond.addWidget(self.spbSecondSpacing)
        self.lblSecondColor = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSecondColor.setObjectName("lblSecondColor")
        self.hlytSubtitleSecond.addWidget(self.lblSecondColor)
        self.freSecondColor = QtWidgets.QFrame(parent=self.freSecondSubtitle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freSecondColor.sizePolicy().hasHeightForWidth())
        self.freSecondColor.setSizePolicy(sizePolicy)
        self.freSecondColor.setMinimumSize(QtCore.QSize(50, 20))
        self.freSecondColor.setMaximumSize(QtCore.QSize(50, 20))
        self.freSecondColor.setStyleSheet("QWidget { background-color: rgb(255, 255, 255); border: 1px solid black; }")
        self.freSecondColor.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freSecondColor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.freSecondColor.setObjectName("freSecondColor")
        self.hlytSubtitleSecond.addWidget(self.freSecondColor)
        self.btnSecondColor = QtWidgets.QPushButton(parent=self.freSecondSubtitle)
        self.btnSecondColor.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btnSecondColor.setIcon(icon8)
        self.btnSecondColor.setObjectName("btnSecondColor")
        self.hlytSubtitleSecond.addWidget(self.btnSecondColor)
        self.lblSecondOutlineColor = QtWidgets.QLabel(parent=self.freSecondSubtitle)
        self.lblSecondOutlineColor.setObjectName("lblSecondOutlineColor")
        self.hlytSubtitleSecond.addWidget(self.lblSecondOutlineColor)
        self.freSecondOutlineColor = QtWidgets.QFrame(parent=self.freSecondSubtitle)
        self.freSecondOutlineColor.setMinimumSize(QtCore.QSize(50, 20))
        self.freSecondOutlineColor.setMaximumSize(QtCore.QSize(50, 20))
        self.freSecondOutlineColor.setAutoFillBackground(False)
        self.freSecondOutlineColor.setStyleSheet("QWidget { background-color: rgb(5, 7, 13); border: 1px solid black; }")
        self.freSecondOutlineColor.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freSecondOutlineColor.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.freSecondOutlineColor.setObjectName("freSecondOutlineColor")
        self.hlytSubtitleSecond.addWidget(self.freSecondOutlineColor)
        self.btnSecondOutlineColor = QtWidgets.QPushButton(parent=self.freSecondSubtitle)
        self.btnSecondOutlineColor.setMinimumSize(QtCore.QSize(50, 0))
        self.btnSecondOutlineColor.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btnSecondOutlineColor.setIcon(icon8)
        self.btnSecondOutlineColor.setObjectName("btnSecondOutlineColor")
        self.hlytSubtitleSecond.addWidget(self.btnSecondOutlineColor)
        self.hlytSubtitleSecond.setStretch(2, 1)
        self.hlytSubtitleSecond.setStretch(4, 1)
        self.hlytSubtitleSecond.setStretch(6, 1)
        self.vlytSetting.addWidget(self.freSecondSubtitle)
        self.vlytMain.addWidget(self.freSetting)
        self.freTop = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.freTop.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freTop.setMidLineWidth(1)
        self.freTop.setObjectName("freTop")
        self.hlytTool = QtWidgets.QHBoxLayout(self.freTop)
        self.hlytTool.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.hlytTool.setContentsMargins(-1, 6, -1, 6)
        self.hlytTool.setObjectName("hlytTool")
        self.btnAddFile = QtWidgets.QToolButton(parent=self.freTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddFile.sizePolicy().hasHeightForWidth())
        self.btnAddFile.setSizePolicy(sizePolicy)
        self.btnAddFile.setMinimumSize(QtCore.QSize(0, 30))
        self.btnAddFile.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnAddFile.setSizeIncrement(QtCore.QSize(0, 0))
        self.btnAddFile.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        self.btnAddFile.setFont(font)
        self.btnAddFile.setToolTipDuration(-1)
        self.btnAddFile.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../../resources/images/icons/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnAddFile.setIcon(icon9)
        self.btnAddFile.setAutoRepeatInterval(100)
        self.btnAddFile.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnAddFile.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnAddFile.setAutoRaise(False)
        self.btnAddFile.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnAddFile.setObjectName("btnAddFile")
        self.hlytTool.addWidget(self.btnAddFile)
        self.btnStart = QtWidgets.QToolButton(parent=self.freTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy)
        self.btnStart.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        self.btnStart.setFont(font)
        self.btnStart.setToolTipDuration(-1)
        self.btnStart.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btnStart.setStyleSheet("color: rgb(255, 170, 0)")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../../resources/images/icons/启动.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnStart.setIcon(icon10)
        self.btnStart.setAutoRepeatInterval(100)
        self.btnStart.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnStart.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnStart.setAutoRaise(False)
        self.btnStart.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnStart.setObjectName("btnStart")
        self.hlytTool.addWidget(self.btnStart)
        self.btnStop = QtWidgets.QToolButton(parent=self.freTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy)
        self.btnStop.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        self.btnStop.setFont(font)
        self.btnStop.setToolTipDuration(-1)
        self.btnStop.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btnStop.setStyleSheet("color: red")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("../../resources/images/icons/暂停.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnStop.setIcon(icon11)
        self.btnStop.setAutoRepeatInterval(100)
        self.btnStop.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnStop.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnStop.setAutoRaise(False)
        self.btnStop.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnStop.setObjectName("btnStop")
        self.hlytTool.addWidget(self.btnStop)
        self.btnClearFile = QtWidgets.QToolButton(parent=self.freTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClearFile.sizePolicy().hasHeightForWidth())
        self.btnClearFile.setSizePolicy(sizePolicy)
        self.btnClearFile.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        self.btnClearFile.setFont(font)
        self.btnClearFile.setToolTipDuration(-1)
        self.btnClearFile.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("../../resources/images/icons/清空.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnClearFile.setIcon(icon12)
        self.btnClearFile.setAutoRepeatInterval(100)
        self.btnClearFile.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnClearFile.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnClearFile.setAutoRaise(False)
        self.btnClearFile.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnClearFile.setObjectName("btnClearFile")
        self.hlytTool.addWidget(self.btnClearFile)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.hlytTool.addLayout(self.horizontalLayout)
        self.btnSettingVisible = QtWidgets.QPushButton(parent=self.freTop)
        self.btnSettingVisible.setMinimumSize(QtCore.QSize(100, 30))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("../../resources/images/icons/隐藏.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnSettingVisible.setIcon(icon13)
        self.btnSettingVisible.setObjectName("btnSettingVisible")
        self.hlytTool.addWidget(self.btnSettingVisible)
        self.btnSetting = QtWidgets.QToolButton(parent=self.freTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetting.sizePolicy().hasHeightForWidth())
        self.btnSetting.setSizePolicy(sizePolicy)
        self.btnSetting.setMinimumSize(QtCore.QSize(100, 30))
        self.btnSetting.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        font.setBold(True)
        self.btnSetting.setFont(font)
        self.btnSetting.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("../../resources/images/icons/设置.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnSetting.setIcon(icon14)
        self.btnSetting.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnSetting.setObjectName("btnSetting")
        self.hlytTool.addWidget(self.btnSetting)
        self.vlytMain.addWidget(self.freTop)
        self.tbvTask = QtWidgets.QTableView(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbvTask.sizePolicy().hasHeightForWidth())
        self.tbvTask.setSizePolicy(sizePolicy)
        self.tbvTask.setBaseSize(QtCore.QSize(0, 0))
        self.tbvTask.setStyleSheet("")
        self.tbvTask.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.tbvTask.setObjectName("tbvTask")
        self.vlytMain.addWidget(self.tbvTask)
        self.txtLog = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.txtLog.setAutoFillBackground(False)
        self.txtLog.setStyleSheet("")
        self.txtLog.setFrameShape(QtWidgets.QFrame.Shape.WinPanel)
        self.txtLog.setObjectName("txtLog")
        self.vlytMain.addWidget(self.txtLog)
        self.vlytMain.setStretch(2, 1)
        self.vlytMain.setStretch(3, 1)

        self.retranslateUi(frmMain)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def retranslateUi(self, frmMain):
        _translate = QtCore.QCoreApplication.translate
        frmMain.setWindowTitle(_translate("frmMain", "千言字幕助手"))
        self.btnDownTool.setText(_translate("frmMain", "下载工具"))
        self.lblWhisperExe.setText(_translate("frmMain", "FasterWhisper工具"))
        self.btnWhisperExe.setText(_translate("frmMain", "选择"))
        self.chbVad.setText(_translate("frmMain", "静音过滤"))
        self.lblVadMethod.setText(_translate("frmMain", "静音过滤方法"))
        self.lblVadValue.setText(_translate("frmMain", "静音过滤阈值"))
        self.chbHumanVoice.setText(_translate("frmMain", "消除背景音乐"))
        self.lblRunDevice.setText(_translate("frmMain", "运行设备"))
        self.lblWhisperModel.setText(_translate("frmMain", "Whisper模型"))
        self.btnDownModel.setText(_translate("frmMain", "下载模型"))
        self.lblWhisterDir.setText(_translate("frmMain", "模型目录"))
        self.btnWhisperDir.setText(_translate("frmMain", "选择目录"))
        self.chbTranslate.setText(_translate("frmMain", "是否翻译"))
        self.lblTranslateMode.setText(_translate("frmMain", "翻译模式"))
        self.chbClearPunctuation.setText(_translate("frmMain", "消除标点符号"))
        self.lblSourceLanguage.setText(_translate("frmMain", "源语言（视频或者音频中所说的语言）"))
        self.lblTargetLanguage.setText(_translate("frmMain", "目标语言（需要翻译为的语言）"))
        self.lblLLM.setText(_translate("frmMain", "LLM 配置："))
        self.btnLlmApi.setText(_translate("frmMain", "免费注册"))
        self.lblApiKey.setText(_translate("frmMain", "API Key"))
        self.lblBaseUrl.setText(_translate("frmMain", "Base URL"))
        self.btnLlmRefresh.setText(_translate("frmMain", "更新模型"))
        self.lblLlmModel.setText(_translate("frmMain", "模型"))
        self.cbbLlmModel.setItemText(0, _translate("frmMain", "gemma2:latest"))
        self.btnCheckApi.setText(_translate("frmMain", "检查连接"))
        self.chbEmbedSubtitle.setText(_translate("frmMain", "把字幕合成到视频中"))
        self.chbSoftSubtitle.setText(_translate("frmMain", "使用软字幕"))
        self.chbRemoveTempFile.setText(_translate("frmMain", "是否删除处理中产生的文件"))
        self.lblSubtitleLayout.setText(_translate("frmMain", "字幕排布（原文和译文的布局）"))
        self.lblSubtitleVH.setText(_translate("frmMain", "字幕与视频底部间隔"))
        self.lblSubtitleMain.setText(_translate("frmMain", "主字幕（上面的字幕）样式："))
        self.lblMainFont.setText(_translate("frmMain", "字体"))
        self.lblMainSize.setText(_translate("frmMain", "字号"))
        self.lblMainSpacing.setText(_translate("frmMain", "字间距"))
        self.lblMainColor.setText(_translate("frmMain", "字颜色"))
        self.btnMainColor.setText(_translate("frmMain", "选取"))
        self.lblMainOutlineColor.setText(_translate("frmMain", "边框颜色"))
        self.btnMainOutlineColor.setText(_translate("frmMain", "选取"))
        self.lblSubtitleSecond.setText(_translate("frmMain", "副字幕（下面的字幕）样式："))
        self.lblSecondFont.setText(_translate("frmMain", "字体"))
        self.lblSecondSize.setText(_translate("frmMain", "字号"))
        self.lblSecondSpacing.setText(_translate("frmMain", "字间距"))
        self.lblSecondColor.setText(_translate("frmMain", "字颜色"))
        self.btnSecondColor.setText(_translate("frmMain", "选取"))
        self.lblSecondOutlineColor.setText(_translate("frmMain", "边框颜色"))
        self.btnSecondOutlineColor.setText(_translate("frmMain", "选取"))
        self.btnAddFile.setText(_translate("frmMain", " 添加文件"))
        self.btnStart.setText(_translate("frmMain", " 开始"))
        self.btnStop.setText(_translate("frmMain", " 停止"))
        self.btnClearFile.setText(_translate("frmMain", " 清空文件"))
        self.btnSettingVisible.setText(_translate("frmMain", "隐藏配置"))
        self.btnSetting.setText(_translate("frmMain", " 保存配置"))
        self.txtLog.setHtml(_translate("frmMain", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
