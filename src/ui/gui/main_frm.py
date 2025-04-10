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
        frmMain.resize(1200, 956)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        frmMain.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../resources/images/icons/logo-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        frmMain.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=frmMain)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vlytMain = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vlytMain.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.vlytMain.setObjectName("vlytMain")
        self.freSetting = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.freSetting.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freSetting.setObjectName("freSetting")
        self.vlytSetting = QtWidgets.QVBoxLayout(self.freSetting)
        self.vlytSetting.setContentsMargins(4, 2, 4, 2)
        self.vlytSetting.setSpacing(2)
        self.vlytSetting.setObjectName("vlytSetting")
        self.freTranslate = QtWidgets.QFrame(parent=self.freSetting)
        self.freTranslate.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.freTranslate.setObjectName("freTranslate")
        self.hlytTranslate = QtWidgets.QHBoxLayout(self.freTranslate)
        self.hlytTranslate.setContentsMargins(10, 4, 10, 4)
        self.hlytTranslate.setObjectName("hlytTranslate")
        self.ckbTranslate = QtWidgets.QCheckBox(parent=self.freTranslate)
        self.ckbTranslate.setObjectName("ckbTranslate")
        self.hlytTranslate.addWidget(self.ckbTranslate)
        self.lblTranslateMode = QtWidgets.QLabel(parent=self.freTranslate)
        self.lblTranslateMode.setObjectName("lblTranslateMode")
        self.hlytTranslate.addWidget(self.lblTranslateMode)
        self.cbbTranslateMode = QtWidgets.QComboBox(parent=self.freTranslate)
        self.cbbTranslateMode.setObjectName("cbbTranslateMode")
        self.hlytTranslate.addWidget(self.cbbTranslateMode)
        self.ckbClearPunctuation = QtWidgets.QCheckBox(parent=self.freTranslate)
        self.ckbClearPunctuation.setObjectName("ckbClearPunctuation")
        self.hlytTranslate.addWidget(self.ckbClearPunctuation)
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
        self.hlytTranslate.setStretch(7, 2)
        self.vlytSetting.addWidget(self.freTranslate)
        self.line = QtWidgets.QFrame(parent=self.freSetting)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.vlytSetting.addWidget(self.line)
        self.freSubtitle = QtWidgets.QFrame(parent=self.freSetting)
        self.freSubtitle.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.freSubtitle.setObjectName("freSubtitle")
        self.hlytSubtitle = QtWidgets.QHBoxLayout(self.freSubtitle)
        self.hlytSubtitle.setContentsMargins(10, 4, 10, 4)
        self.hlytSubtitle.setObjectName("hlytSubtitle")
        self.ckbEmbedSubtitle = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.ckbEmbedSubtitle.setObjectName("ckbEmbedSubtitle")
        self.hlytSubtitle.addWidget(self.ckbEmbedSubtitle)
        self.ckbSoftSubtitle = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.ckbSoftSubtitle.setObjectName("ckbSoftSubtitle")
        self.hlytSubtitle.addWidget(self.ckbSoftSubtitle)
        self.ckbRemoveTempFile = QtWidgets.QCheckBox(parent=self.freSubtitle)
        self.ckbRemoveTempFile.setObjectName("ckbRemoveTempFile")
        self.hlytSubtitle.addWidget(self.ckbRemoveTempFile)
        self.lblSubtitleLayout = QtWidgets.QLabel(parent=self.freSubtitle)
        self.lblSubtitleLayout.setObjectName("lblSubtitleLayout")
        self.hlytSubtitle.addWidget(self.lblSubtitleLayout)
        self.cbbSubtitleLayout = QtWidgets.QComboBox(parent=self.freSubtitle)
        self.cbbSubtitleLayout.setObjectName("cbbSubtitleLayout")
        self.hlytSubtitle.addWidget(self.cbbSubtitleLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hlytSubtitle.addItem(spacerItem)
        self.hlytSubtitle.setStretch(4, 1)
        self.hlytSubtitle.setStretch(5, 2)
        self.vlytSetting.addWidget(self.freSubtitle)
        self.vlytMain.addWidget(self.freSetting)
        self.freTools = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.freTools.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.freTools.setMidLineWidth(1)
        self.freTools.setObjectName("freTools")
        self.hlytTool = QtWidgets.QHBoxLayout(self.freTools)
        self.hlytTool.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.hlytTool.setContentsMargins(-1, 6, -1, 6)
        self.hlytTool.setObjectName("hlytTool")
        self.btnAddFile = QtWidgets.QToolButton(parent=self.freTools)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../resources/images/icons/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnAddFile.setIcon(icon1)
        self.btnAddFile.setAutoRepeatInterval(100)
        self.btnAddFile.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnAddFile.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnAddFile.setAutoRaise(False)
        self.btnAddFile.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnAddFile.setObjectName("btnAddFile")
        self.hlytTool.addWidget(self.btnAddFile)
        self.btnStart = QtWidgets.QToolButton(parent=self.freTools)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../resources/images/icons/启动.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnStart.setIcon(icon2)
        self.btnStart.setAutoRepeatInterval(100)
        self.btnStart.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnStart.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnStart.setAutoRaise(False)
        self.btnStart.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnStart.setObjectName("btnStart")
        self.hlytTool.addWidget(self.btnStart)
        self.btnStop = QtWidgets.QToolButton(parent=self.freTools)
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../resources/images/icons/暂停.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnStop.setIcon(icon3)
        self.btnStop.setAutoRepeatInterval(100)
        self.btnStop.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnStop.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnStop.setAutoRaise(False)
        self.btnStop.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnStop.setObjectName("btnStop")
        self.hlytTool.addWidget(self.btnStop)
        self.btnClearFile = QtWidgets.QToolButton(parent=self.freTools)
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../resources/images/icons/清空.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnClearFile.setIcon(icon4)
        self.btnClearFile.setAutoRepeatInterval(100)
        self.btnClearFile.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnClearFile.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnClearFile.setAutoRaise(False)
        self.btnClearFile.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.btnClearFile.setObjectName("btnClearFile")
        self.hlytTool.addWidget(self.btnClearFile)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.hlytTool.addLayout(self.horizontalLayout)
        self.vlytMain.addWidget(self.freTools)
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
        frmMain.setCentralWidget(self.verticalLayoutWidget)
        self.menubar = QtWidgets.QMenuBar(parent=frmMain)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTool = QtWidgets.QMenu(parent=self.menubar)
        self.menuTool.setObjectName("menuTool")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        frmMain.setMenuBar(self.menubar)
        self.actGitee = QtGui.QAction(parent=frmMain)
        self.actGitee.setObjectName("actGitee")
        self.actGithub = QtGui.QAction(parent=frmMain)
        self.actGithub.setObjectName("actGithub")
        self.actAbout = QtGui.QAction(parent=frmMain)
        self.actAbout.setObjectName("actAbout")
        self.actLlmChecker = QtGui.QAction(parent=frmMain)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../resources/images/icons/link.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actLlmChecker.setIcon(icon5)
        self.actLlmChecker.setObjectName("actLlmChecker")
        self.actAddFile = QtGui.QAction(parent=frmMain)
        self.actAddFile.setIcon(icon1)
        self.actAddFile.setObjectName("actAddFile")
        self.actClearFile = QtGui.QAction(parent=frmMain)
        self.actClearFile.setIcon(icon4)
        self.actClearFile.setObjectName("actClearFile")
        self.actExit = QtGui.QAction(parent=frmMain)
        self.actExit.setObjectName("actExit")
        self.actSetting = QtGui.QAction(parent=frmMain)
        self.actSetting.setObjectName("actSetting")
        self.actSubtitleEmbed = QtGui.QAction(parent=frmMain)
        self.actSubtitleEmbed.setObjectName("actSubtitleEmbed")
        self.actFeiShu = QtGui.QAction(parent=frmMain)
        self.actFeiShu.setObjectName("actFeiShu")
        self.menuFile.addAction(self.actAddFile)
        self.menuFile.addAction(self.actClearFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actSetting)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actExit)
        self.menuTool.addAction(self.actLlmChecker)
        self.menuTool.addAction(self.actSubtitleEmbed)
        self.menuHelp.addAction(self.actGitee)
        self.menuHelp.addAction(self.actGithub)
        self.menuHelp.addAction(self.actFeiShu)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(frmMain)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def retranslateUi(self, frmMain):
        _translate = QtCore.QCoreApplication.translate
        frmMain.setWindowTitle(_translate("frmMain", "千言字幕助手"))
        self.ckbTranslate.setText(_translate("frmMain", "是否翻译"))
        self.lblTranslateMode.setText(_translate("frmMain", "翻译模式"))
        self.ckbClearPunctuation.setText(_translate("frmMain", "消除标点符号"))
        self.lblSourceLanguage.setText(_translate("frmMain", "源语言"))
        self.lblTargetLanguage.setText(_translate("frmMain", "目标语言"))
        self.ckbEmbedSubtitle.setText(_translate("frmMain", "把字幕合成到视频中"))
        self.ckbSoftSubtitle.setText(_translate("frmMain", "使用软字幕"))
        self.ckbRemoveTempFile.setText(_translate("frmMain", "是否删除处理中产生的文件"))
        self.lblSubtitleLayout.setText(_translate("frmMain", "字幕排布（原文和译文的布局）"))
        self.btnAddFile.setText(_translate("frmMain", " 添加文件"))
        self.btnStart.setText(_translate("frmMain", " 开始"))
        self.btnStop.setText(_translate("frmMain", " 停止"))
        self.btnClearFile.setText(_translate("frmMain", " 清空文件"))
        self.txtLog.setHtml(_translate("frmMain", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.menuFile.setTitle(_translate("frmMain", "文件"))
        self.menuTool.setTitle(_translate("frmMain", "工具"))
        self.menuHelp.setTitle(_translate("frmMain", "帮助"))
        self.actGitee.setText(_translate("frmMain", "Gitee仓库"))
        self.actGithub.setText(_translate("frmMain", "Github仓库"))
        self.actAbout.setText(_translate("frmMain", "关于..."))
        self.actLlmChecker.setText(_translate("frmMain", "提示语调整工具..."))
        self.actAddFile.setText(_translate("frmMain", "添加文件..."))
        self.actClearFile.setText(_translate("frmMain", "清空文件"))
        self.actExit.setText(_translate("frmMain", "退出"))
        self.actSetting.setText(_translate("frmMain", "配置..."))
        self.actSubtitleEmbed.setText(_translate("frmMain", "字幕合成工具.."))
        self.actFeiShu.setText(_translate("frmMain", "飞书下载..."))
