# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/niko/workspace/easyP2P/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 455)
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
        self.groupBox_platforms = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_platforms.setObjectName("groupBox_platforms")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_platforms)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_bondora = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_bondora.setObjectName("checkBox_bondora")
        self.gridLayout.addWidget(self.checkBox_bondora, 0, 0, 1, 1)
        self.checkBox_grupeer = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_grupeer.setObjectName("checkBox_grupeer")
        self.gridLayout.addWidget(self.checkBox_grupeer, 2, 0, 1, 1)
        self.checkBox_dofinance = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_dofinance.setObjectName("checkBox_dofinance")
        self.gridLayout.addWidget(self.checkBox_dofinance, 1, 0, 1, 1)
        self.checkBox_iuvo = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_iuvo.setObjectName("checkBox_iuvo")
        self.gridLayout.addWidget(self.checkBox_iuvo, 4, 0, 1, 1)
        self.checkBox_peerberry = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_peerberry.setObjectName("checkBox_peerberry")
        self.gridLayout.addWidget(self.checkBox_peerberry, 1, 1, 1, 1)
        self.checkBox_mintos = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_mintos.setObjectName("checkBox_mintos")
        self.gridLayout.addWidget(self.checkBox_mintos, 0, 1, 1, 1)
        self.checkBox_robocash = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_robocash.setObjectName("checkBox_robocash")
        self.gridLayout.addWidget(self.checkBox_robocash, 2, 1, 1, 1)
        self.checkBox_estateguru = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_estateguru.setObjectName("checkBox_estateguru")
        self.gridLayout.addWidget(self.checkBox_estateguru, 3, 0, 1, 1)
        self.checkBox_swaper = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_swaper.setObjectName("checkBox_swaper")
        self.gridLayout.addWidget(self.checkBox_swaper, 3, 1, 1, 1)
        self.checkBox_twino = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_twino.setObjectName("checkBox_twino")
        self.gridLayout.addWidget(self.checkBox_twino, 4, 1, 1, 1)
        self.checkBox_select_all = QtWidgets.QCheckBox(self.groupBox_platforms)
        self.checkBox_select_all.setObjectName("checkBox_select_all")
        self.gridLayout.addWidget(self.checkBox_select_all, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox_platforms)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox_start_month = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_start_month.setObjectName("comboBox_start_month")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.comboBox_start_month.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_start_month)
        self.comboBox_start_year = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_start_year.setObjectName("comboBox_start_year")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.comboBox_start_year.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_start_year)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBox_end_month = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_end_month.setObjectName("comboBox_end_month")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.comboBox_end_month.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_end_month)
        self.comboBox_end_year = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_end_year.setObjectName("comboBox_end_year")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.comboBox_end_year.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_end_year)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_output_file = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_output_file.setReadOnly(True)
        self.lineEdit_output_file.setObjectName("lineEdit_output_file")
        self.horizontalLayout_6.addWidget(self.lineEdit_output_file)
        self.pushButton_file_chooser = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_file_chooser.setObjectName("pushButton_file_chooser")
        self.horizontalLayout_6.addWidget(self.pushButton_file_chooser)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout.addWidget(self.pushButton_start)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "easyP2P"))
        self.groupBox_platforms.setTitle(_translate("MainWindow", "Für welche P2P-Plattformen sollen Ergebnisse geladen werden?"))
        self.checkBox_bondora.setText(_translate("MainWindow", "Bondora"))
        self.checkBox_grupeer.setText(_translate("MainWindow", "Grupeer"))
        self.checkBox_dofinance.setText(_translate("MainWindow", "DoFinance"))
        self.checkBox_iuvo.setText(_translate("MainWindow", "Iuvo"))
        self.checkBox_peerberry.setText(_translate("MainWindow", "PeerBerry"))
        self.checkBox_mintos.setText(_translate("MainWindow", "Mintos"))
        self.checkBox_robocash.setText(_translate("MainWindow", "Robocash"))
        self.checkBox_estateguru.setText(_translate("MainWindow", "Estateguru"))
        self.checkBox_swaper.setText(_translate("MainWindow", "Swaper"))
        self.checkBox_twino.setText(_translate("MainWindow", "Twino"))
        self.checkBox_select_all.setText(_translate("MainWindow", "Alle aus-/abwählen"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Startdatum"))
        self.comboBox_start_month.setItemText(0, _translate("MainWindow", "Jan"))
        self.comboBox_start_month.setItemText(1, _translate("MainWindow", "Feb"))
        self.comboBox_start_month.setItemText(2, _translate("MainWindow", "Mrz"))
        self.comboBox_start_month.setItemText(3, _translate("MainWindow", "Apr"))
        self.comboBox_start_month.setItemText(4, _translate("MainWindow", "Mai"))
        self.comboBox_start_month.setItemText(5, _translate("MainWindow", "Jun"))
        self.comboBox_start_month.setItemText(6, _translate("MainWindow", "Jul"))
        self.comboBox_start_month.setItemText(7, _translate("MainWindow", "Aug"))
        self.comboBox_start_month.setItemText(8, _translate("MainWindow", "Sep"))
        self.comboBox_start_month.setItemText(9, _translate("MainWindow", "Okt"))
        self.comboBox_start_month.setItemText(10, _translate("MainWindow", "Nov"))
        self.comboBox_start_month.setItemText(11, _translate("MainWindow", "Dez"))
        self.comboBox_start_year.setItemText(0, _translate("MainWindow", "2010"))
        self.comboBox_start_year.setItemText(1, _translate("MainWindow", "2011"))
        self.comboBox_start_year.setItemText(2, _translate("MainWindow", "2012"))
        self.comboBox_start_year.setItemText(3, _translate("MainWindow", "2013"))
        self.comboBox_start_year.setItemText(4, _translate("MainWindow", "2014"))
        self.comboBox_start_year.setItemText(5, _translate("MainWindow", "2015"))
        self.comboBox_start_year.setItemText(6, _translate("MainWindow", "2016"))
        self.comboBox_start_year.setItemText(7, _translate("MainWindow", "2017"))
        self.comboBox_start_year.setItemText(8, _translate("MainWindow", "2018"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Enddatum"))
        self.comboBox_end_month.setItemText(0, _translate("MainWindow", "Jan"))
        self.comboBox_end_month.setItemText(1, _translate("MainWindow", "Feb"))
        self.comboBox_end_month.setItemText(2, _translate("MainWindow", "Mrz"))
        self.comboBox_end_month.setItemText(3, _translate("MainWindow", "Apr"))
        self.comboBox_end_month.setItemText(4, _translate("MainWindow", "Mai"))
        self.comboBox_end_month.setItemText(5, _translate("MainWindow", "Jun"))
        self.comboBox_end_month.setItemText(6, _translate("MainWindow", "Jul"))
        self.comboBox_end_month.setItemText(7, _translate("MainWindow", "Aug"))
        self.comboBox_end_month.setItemText(8, _translate("MainWindow", "Sep"))
        self.comboBox_end_month.setItemText(9, _translate("MainWindow", "Okt"))
        self.comboBox_end_month.setItemText(10, _translate("MainWindow", "Nov"))
        self.comboBox_end_month.setItemText(11, _translate("MainWindow", "Dez"))
        self.comboBox_end_year.setItemText(0, _translate("MainWindow", "2010"))
        self.comboBox_end_year.setItemText(1, _translate("MainWindow", "2011"))
        self.comboBox_end_year.setItemText(2, _translate("MainWindow", "2012"))
        self.comboBox_end_year.setItemText(3, _translate("MainWindow", "2013"))
        self.comboBox_end_year.setItemText(4, _translate("MainWindow", "2014"))
        self.comboBox_end_year.setItemText(5, _translate("MainWindow", "2015"))
        self.comboBox_end_year.setItemText(6, _translate("MainWindow", "2016"))
        self.comboBox_end_year.setItemText(7, _translate("MainWindow", "2017"))
        self.comboBox_end_year.setItemText(8, _translate("MainWindow", "2018"))
        self.groupBox_5.setTitle(_translate("MainWindow", "In welcher Datei sollen die Ergebnisse gespeichert werden?"))
        self.pushButton_file_chooser.setText(_translate("MainWindow", "Datei wählen"))
        self.pushButton_start.setText(_translate("MainWindow", "Starte Auswertung"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

