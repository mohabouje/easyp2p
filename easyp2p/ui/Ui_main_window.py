# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/niko/workspace/easyp2p/easyp2p/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(736, 462)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group_box_platform_top = QtWidgets.QGroupBox(self.groupBox)
        self.group_box_platform_top.setAlignment(QtCore.Qt.AlignCenter)
        self.group_box_platform_top.setObjectName("group_box_platform_top")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_box_platform_top)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.group_box_platforms = QtWidgets.QGroupBox(self.group_box_platform_top)
        self.group_box_platforms.setTitle("")
        self.group_box_platforms.setObjectName("group_box_platforms")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.group_box_platforms)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.check_box_bondora = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_bondora.setText("Bondora")
        self.check_box_bondora.setShortcut("")
        self.check_box_bondora.setObjectName("check_box_bondora")
        self.gridLayout_2.addWidget(self.check_box_bondora, 0, 0, 1, 1)
        self.check_box_mintos = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_mintos.setText("Mintos")
        self.check_box_mintos.setShortcut("")
        self.check_box_mintos.setObjectName("check_box_mintos")
        self.gridLayout_2.addWidget(self.check_box_mintos, 0, 1, 1, 1)
        self.check_box_dofinance = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_dofinance.setText("DoFinance")
        self.check_box_dofinance.setShortcut("")
        self.check_box_dofinance.setObjectName("check_box_dofinance")
        self.gridLayout_2.addWidget(self.check_box_dofinance, 2, 0, 1, 1)
        self.check_box_peerberry = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_peerberry.setText("PeerBerry")
        self.check_box_peerberry.setShortcut("")
        self.check_box_peerberry.setObjectName("check_box_peerberry")
        self.gridLayout_2.addWidget(self.check_box_peerberry, 2, 1, 1, 1)
        self.check_box_estateguru = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_estateguru.setText("Estateguru")
        self.check_box_estateguru.setShortcut("")
        self.check_box_estateguru.setObjectName("check_box_estateguru")
        self.gridLayout_2.addWidget(self.check_box_estateguru, 4, 0, 1, 1)
        self.check_box_robocash = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_robocash.setText("Robocash")
        self.check_box_robocash.setShortcut("")
        self.check_box_robocash.setObjectName("check_box_robocash")
        self.gridLayout_2.addWidget(self.check_box_robocash, 4, 1, 1, 1)
        self.check_box_grupeer = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_grupeer.setText("Grupeer")
        self.check_box_grupeer.setShortcut("")
        self.check_box_grupeer.setObjectName("check_box_grupeer")
        self.gridLayout_2.addWidget(self.check_box_grupeer, 6, 0, 1, 1)
        self.check_box_swaper = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_swaper.setText("Swaper")
        self.check_box_swaper.setShortcut("")
        self.check_box_swaper.setObjectName("check_box_swaper")
        self.gridLayout_2.addWidget(self.check_box_swaper, 6, 1, 1, 1)
        self.check_box_iuvo = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_iuvo.setText("Iuvo")
        self.check_box_iuvo.setShortcut("")
        self.check_box_iuvo.setObjectName("check_box_iuvo")
        self.gridLayout_2.addWidget(self.check_box_iuvo, 7, 0, 1, 1)
        self.check_box_twino = QtWidgets.QCheckBox(self.group_box_platforms)
        self.check_box_twino.setText("Twino")
        self.check_box_twino.setShortcut("")
        self.check_box_twino.setObjectName("check_box_twino")
        self.gridLayout_2.addWidget(self.check_box_twino, 7, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.group_box_platforms, 1, 0, 1, 2)
        self.check_box_select_all = QtWidgets.QCheckBox(self.group_box_platform_top)
        self.check_box_select_all.setObjectName("check_box_select_all")
        self.gridLayout.addWidget(self.check_box_select_all, 2, 0, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.group_box_platform_top)
        self.horizontalLayout_date_range = QtWidgets.QHBoxLayout()
        self.horizontalLayout_date_range.setObjectName("horizontalLayout_date_range")
        self.groupBox_start_date = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_start_date.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_start_date.setObjectName("groupBox_start_date")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_start_date)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.combo_box_start_month = QtWidgets.QComboBox(self.groupBox_start_date)
        self.combo_box_start_month.setObjectName("combo_box_start_month")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.combo_box_start_month.addItem("")
        self.horizontalLayout_3.addWidget(self.combo_box_start_month)
        self.combo_box_start_year = QtWidgets.QComboBox(self.groupBox_start_date)
        self.combo_box_start_year.setObjectName("combo_box_start_year")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.combo_box_start_year.addItem("")
        self.horizontalLayout_3.addWidget(self.combo_box_start_year)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_date_range.addWidget(self.groupBox_start_date)
        self.groupBox_end_date = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_end_date.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_end_date.setObjectName("groupBox_end_date")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_end_date)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.combo_box_end_month = QtWidgets.QComboBox(self.groupBox_end_date)
        self.combo_box_end_month.setObjectName("combo_box_end_month")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.combo_box_end_month.addItem("")
        self.horizontalLayout_4.addWidget(self.combo_box_end_month)
        self.combo_box_end_year = QtWidgets.QComboBox(self.groupBox_end_date)
        self.combo_box_end_year.setObjectName("combo_box_end_year")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.combo_box_end_year.addItem("")
        self.horizontalLayout_4.addWidget(self.combo_box_end_year)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_date_range.addWidget(self.groupBox_end_date)
        self.verticalLayout.addLayout(self.horizontalLayout_date_range)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.line_edit_output_file = QtWidgets.QLineEdit(self.groupBox_5)
        self.line_edit_output_file.setReadOnly(True)
        self.line_edit_output_file.setObjectName("line_edit_output_file")
        self.horizontalLayout_6.addWidget(self.line_edit_output_file)
        self.push_button_file_chooser = QtWidgets.QPushButton(self.groupBox_5)
        self.push_button_file_chooser.setObjectName("push_button_file_chooser")
        self.horizontalLayout_6.addWidget(self.push_button_file_chooser)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.push_button_start = QtWidgets.QPushButton(self.groupBox)
        self.push_button_start.setObjectName("push_button_start")
        self.verticalLayout.addWidget(self.push_button_start)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "easyp2p"))
        self.group_box_platform_top.setTitle(_translate("MainWindow", "Für welche P2P-Plattformen sollen Ergebnisse geladen werden?"))
        self.check_box_select_all.setText(_translate("MainWindow", "Alle aus-/abwählen"))
        self.groupBox_start_date.setTitle(_translate("MainWindow", "Startdatum"))
        self.combo_box_start_month.setItemText(0, _translate("MainWindow", "Jan"))
        self.combo_box_start_month.setItemText(1, _translate("MainWindow", "Feb"))
        self.combo_box_start_month.setItemText(2, _translate("MainWindow", "Mrz"))
        self.combo_box_start_month.setItemText(3, _translate("MainWindow", "Apr"))
        self.combo_box_start_month.setItemText(4, _translate("MainWindow", "Mai"))
        self.combo_box_start_month.setItemText(5, _translate("MainWindow", "Jun"))
        self.combo_box_start_month.setItemText(6, _translate("MainWindow", "Jul"))
        self.combo_box_start_month.setItemText(7, _translate("MainWindow", "Aug"))
        self.combo_box_start_month.setItemText(8, _translate("MainWindow", "Sep"))
        self.combo_box_start_month.setItemText(9, _translate("MainWindow", "Okt"))
        self.combo_box_start_month.setItemText(10, _translate("MainWindow", "Nov"))
        self.combo_box_start_month.setItemText(11, _translate("MainWindow", "Dez"))
        self.combo_box_start_year.setItemText(0, _translate("MainWindow", "2010"))
        self.combo_box_start_year.setItemText(1, _translate("MainWindow", "2011"))
        self.combo_box_start_year.setItemText(2, _translate("MainWindow", "2012"))
        self.combo_box_start_year.setItemText(3, _translate("MainWindow", "2013"))
        self.combo_box_start_year.setItemText(4, _translate("MainWindow", "2014"))
        self.combo_box_start_year.setItemText(5, _translate("MainWindow", "2015"))
        self.combo_box_start_year.setItemText(6, _translate("MainWindow", "2016"))
        self.combo_box_start_year.setItemText(7, _translate("MainWindow", "2017"))
        self.combo_box_start_year.setItemText(8, _translate("MainWindow", "2018"))
        self.combo_box_start_year.setItemText(9, _translate("MainWindow", "2019"))
        self.groupBox_end_date.setTitle(_translate("MainWindow", "Enddatum"))
        self.combo_box_end_month.setItemText(0, _translate("MainWindow", "Jan"))
        self.combo_box_end_month.setItemText(1, _translate("MainWindow", "Feb"))
        self.combo_box_end_month.setItemText(2, _translate("MainWindow", "Mrz"))
        self.combo_box_end_month.setItemText(3, _translate("MainWindow", "Apr"))
        self.combo_box_end_month.setItemText(4, _translate("MainWindow", "Mai"))
        self.combo_box_end_month.setItemText(5, _translate("MainWindow", "Jun"))
        self.combo_box_end_month.setItemText(6, _translate("MainWindow", "Jul"))
        self.combo_box_end_month.setItemText(7, _translate("MainWindow", "Aug"))
        self.combo_box_end_month.setItemText(8, _translate("MainWindow", "Sep"))
        self.combo_box_end_month.setItemText(9, _translate("MainWindow", "Okt"))
        self.combo_box_end_month.setItemText(10, _translate("MainWindow", "Nov"))
        self.combo_box_end_month.setItemText(11, _translate("MainWindow", "Dez"))
        self.combo_box_end_year.setItemText(0, _translate("MainWindow", "2010"))
        self.combo_box_end_year.setItemText(1, _translate("MainWindow", "2011"))
        self.combo_box_end_year.setItemText(2, _translate("MainWindow", "2012"))
        self.combo_box_end_year.setItemText(3, _translate("MainWindow", "2013"))
        self.combo_box_end_year.setItemText(4, _translate("MainWindow", "2014"))
        self.combo_box_end_year.setItemText(5, _translate("MainWindow", "2015"))
        self.combo_box_end_year.setItemText(6, _translate("MainWindow", "2016"))
        self.combo_box_end_year.setItemText(7, _translate("MainWindow", "2017"))
        self.combo_box_end_year.setItemText(8, _translate("MainWindow", "2018"))
        self.combo_box_end_year.setItemText(9, _translate("MainWindow", "2019"))
        self.groupBox_5.setTitle(_translate("MainWindow", "In welcher Datei sollen die Ergebnisse gespeichert werden?"))
        self.push_button_file_chooser.setText(_translate("MainWindow", "Datei wählen"))
        self.push_button_start.setText(_translate("MainWindow", "Starte Auswertung"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

