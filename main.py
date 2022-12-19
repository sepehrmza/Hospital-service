from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys, sqlite3, time

# #
from Login2 import Login, PatientLogin, doctors
from PyQt5 import QtCore, QtGui, QtWidgets

import os


class StartDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(StartDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(310)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        self.setWindowTitle("Start")
        self.QBtn = QPushButton()
        self.QBtn2 = QPushButton()
        self.QBtn3 = QPushButton()
        self.QBtn.setText("Dentist")
        self.QBtn2.setText("Radiologist")
        self.QBtn3.setText("Patient")
        self.QBtn.clicked.connect(self.login)
        self.QBtn2.clicked.connect(self.login2)
        self.QBtn3.clicked.connect(self.login3)

        title = QLabel("Welcome, select your identify!")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.QBtn)
        layout.addWidget(self.QBtn2)
        layout.addWidget(self.QBtn3)
        self.setLayout(layout)

    def login(self):
        passdlg = Login()
        if passdlg.exec_() == QDialog.Accepted:
            name = passdlg.name
            self.close()
            self.window = MainWindow()
            self.window.init(name)
            self.window.set_name(name)
            self.window.show()
            self.window.loaddata()

    def login2(self):
        passdlg = Login()
        if passdlg.exec_() == QDialog.Accepted:
            name = passdlg.name
            self.close()
            self.window = MainWindow2()
            self.window.init(name)
            self.window.set_name(name)
            self.window.show()
            self.window.loaddata()

    def login3(self):
        passdlg = PatientLogin()
        if passdlg.exec_() == QDialog.Accepted:
            name = passdlg.name
            self.close()
            self.window = MainWindow3()
            self.window.init(name)
            self.window.set_name(name)
            self.window.show()
            self.window.loaddata()


class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

    def init(self, _name):
        self.name = _name
        self.QBtn = QPushButton()
        self.QBtn.setText("Register")

        self.setWindowTitle("Add Patient")
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.check_empty)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.idinput = QLineEdit()
        self.idinput.setPlaceholderText("ID No")
        self.onlyInt = QIntValidator()
        self.idinput.setValidator(self.onlyInt)
        layout.addWidget(self.idinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("Complete exams, x-rays, and dental cleanings")
        self.branchinput.addItem("Fillings, root canals, and extractions")
        self.branchinput.addItem(
            "Cosmetic dentistry, such as whitening, porcelain and composite veneers"
        )
        self.branchinput.addItem("Implants - placement and restoration")
        self.branchinput.addItem("Crowns, bridges, full and partial dentures")
        self.branchinput.addItem("Orthodontics")
        self.branchinput.addItem("Oral appliances for control of sleep apnea")
        self.branchinput.addItem(
            "Preventive care, periodontal therapy, and nutritional counseling"
        )
        self.branchinput.addItem("Relaxation techniques using nitrous oxide sedation")
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItem("8:00  - 9:00")
        self.seminput.addItem("9:00  - 10:00")
        self.seminput.addItem("10:00 - 11:00")
        self.seminput.addItem("11:00 - 12:00")
        self.seminput.addItem("13:00 - 14:00")
        self.seminput.addItem("14:00 - 15:00")
        self.seminput.addItem("15:00 - 16:00")
        layout.addWidget(self.seminput)

        self.dayinput = QLineEdit()
        self.dayinput.setPlaceholderText("Day")
        self.onlyIntInRange = QIntValidator(1, 31)
        self.dayinput.setValidator(self.onlyIntInRange)
        layout.addWidget(self.dayinput)

        self.monthinput = QComboBox()
        self.monthinput.addItem("January")
        self.monthinput.addItem("February")
        self.monthinput.addItem("March")
        self.monthinput.addItem("April")
        self.monthinput.addItem("May")
        self.monthinput.addItem("June")
        self.monthinput.addItem("July")
        self.monthinput.addItem("August")
        self.monthinput.addItem("September")
        self.monthinput.addItem("October")
        self.monthinput.addItem("November")
        self.monthinput.addItem("December")
        layout.addWidget(self.monthinput)

        self.mobileinput = QLineEdit()
        rx = QtCore.QRegExp("[0-9,+]{14}")
        val = QtGui.QRegExpValidator(rx)
        self.mobileinput.setValidator(val)

        self.mobileinput.setPlaceholderText("Mobile")
        # self.mobileinput.setInputMask("99999 99999")
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Address")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # check out emptyness of name
    def check_empty(self):
        Hour, Day, Month = (
            str(self.seminput.currentText()),
            str(self.dayinput.text()),
            str(self.monthinput.currentText()),
        )
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        result = c.execute("SELECT * from " + str(self.name))
        rows = result.fetchall()
        reserv = False
        for row in rows:
            if row[4] == Hour and str(row[5]) == Day and row[6] == Month:
                QMessageBox.warning(self, "Error", "This Time Is Reserved Before !")
                reserv = True

        if self.nameinput.text() == "":
            QMessageBox.warning(self, "Error", "Empty name!")
        elif not reserv:
            # self.accept()
            self.addpatient()

    def addpatient(self):

        name = ""
        idno = ""
        branch = ""
        sem = -1
        day = ""
        month = ""
        mobile = ""
        address = ""

        name = self.nameinput.text()
        idno = self.idinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        sem = self.seminput.itemText(self.seminput.currentIndex())
        day = self.dayinput.text()
        month = self.monthinput.itemText(self.monthinput.currentIndex())
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute(
                # "INSERT INTO patients (name,branch,sem,Mobile,address) VALUES (?,?,?,?,?)",
                # (name, branch, sem, mobile, address),
                "INSERT INTO "
                + str(self.name)
                + " (name,id,branch,sem,day,month,Mobile,address) VALUES (?,?,?,?,?,?,?,?)",
                (name, idno, branch, sem, day, month, mobile, address),
            )
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(),
                "Successful",
                "Patient is added successfully to the database.",
            )
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not add patient to the database."
            )


class InsertDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog2, self).__init__(*args, **kwargs)

    def init(self, _name):
        self.name = _name
        self.QBtn = QPushButton()
        self.QBtn.setText("Register")

        self.setWindowTitle("Add Patient")
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.check_empty)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.idinput = QLineEdit()
        self.idinput.setPlaceholderText("ID No")
        self.onlyInt = QIntValidator()
        self.idinput.setValidator(self.onlyInt)
        layout.addWidget(self.idinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("Complete exams, x-rays, and dental cleanings")
        self.branchinput.addItem("Fillings, root canals, and extractions")
        self.branchinput.addItem(
            "Cosmetic dentistry, such as whitening, porcelain and composite veneers"
        )
        self.branchinput.addItem("Implants - placement and restoration")
        self.branchinput.addItem("Crowns, bridges, full and partial dentures")
        self.branchinput.addItem("Orthodontics")
        self.branchinput.addItem("Oral appliances for control of sleep apnea")
        self.branchinput.addItem(
            "Preventive care, periodontal therapy, and nutritional counseling"
        )
        self.branchinput.addItem("Relaxation techniques using nitrous oxide sedation")
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItem("8:00  - 9:00")
        self.seminput.addItem("9:00  - 10:00")
        self.seminput.addItem("10:00 - 11:00")
        self.seminput.addItem("11:00 - 12:00")
        self.seminput.addItem("13:00 - 14:00")
        self.seminput.addItem("14:00 - 15:00")
        self.seminput.addItem("15:00 - 16:00")
        layout.addWidget(self.seminput)

        self.dayinput = QLineEdit()
        self.dayinput.setPlaceholderText("Day")
        self.onlyIntInRange = QIntValidator(1, 31)
        self.dayinput.setValidator(self.onlyIntInRange)
        layout.addWidget(self.dayinput)

        self.monthinput = QComboBox()
        self.monthinput.addItem("January")
        self.monthinput.addItem("February")
        self.monthinput.addItem("March")
        self.monthinput.addItem("April")
        self.monthinput.addItem("May")
        self.monthinput.addItem("June")
        self.monthinput.addItem("July")
        self.monthinput.addItem("August")
        self.monthinput.addItem("September")
        self.monthinput.addItem("October")
        self.monthinput.addItem("November")
        self.monthinput.addItem("December")
        layout.addWidget(self.monthinput)

        self.mobileinput = QLineEdit()
        rx = QtCore.QRegExp("[0-9,+]{14}")
        val = QtGui.QRegExpValidator(rx)
        self.mobileinput.setValidator(val)

        self.mobileinput.setPlaceholderText("Mobile")
        # self.mobileinput.setInputMask("99999 99999")
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Address")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # check out emptyness of name
    def check_empty(self):
        Hour, Day, Month = (
            str(self.seminput.currentText()),
            str(self.dayinput.text()),
            str(self.monthinput.currentText()),
        )
        conn = sqlite3.connect("database2.db")
        c = conn.cursor()
        result = c.execute("SELECT * from " + str(self.name))
        rows = result.fetchall()
        reserv = False
        for row in rows:
            if row[4] == Hour and str(row[5]) == Day and row[6] == Month:
                QMessageBox.warning(self, "Error", "This Time Is Reserved Before !")
                reserv = True

        if self.nameinput.text() == "":
            QMessageBox.warning(self, "Error", "Empty name!")
        elif not reserv:
            # self.accept()
            self.addpatient()

    def addpatient(self):

        name = ""
        idno = ""
        branch = ""
        sem = -1
        day = ""
        month = ""
        mobile = ""
        address = ""

        name = self.nameinput.text()
        idno = self.idinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        sem = self.seminput.itemText(self.seminput.currentIndex())
        day = self.dayinput.text()
        month = self.monthinput.itemText(self.monthinput.currentIndex())
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("database2.db")
            self.c = self.conn.cursor()
            self.c.execute(
                # "INSERT INTO patients (name,branch,sem,Mobile,address) VALUES (?,?,?,?,?)",
                # (name, branch, sem, mobile, address),
                "INSERT INTO "
                + str(self.name)
                + " (name,id,branch,sem,day,month,Mobile,address) VALUES (?,?,?,?,?,?,?,?)",
                (name, idno, branch, sem, day, month, mobile, address),
            )
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(),
                "Successful",
                "Patient is added successfully to the database.",
            )
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not add patient to the database."
            )


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search patient")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchpatient)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("ID No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchpatient(self):
        searchid = ""
        searchid = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute(
                "SELECT * from " + str(self.name) + " WHERE id=" + str(searchid)
            )
            # row = result.fetchone()
            rows = result.fetchall()
            searchresult = (
                "Rollno : "
                + str(rows[0][0])
                + "\n"
                + "Name : "
                + str(rows[0][1])
                + "\n"
                + "ID No : "
                + str(rows[0][2])
                + "\n"
                + "Service : "
                + str(rows[0][3])
                + "\n"
                + "Reservation Time : "
                + str(rows[0][4])
                + "\n"
                + "Day : "
                + str(rows[0][5])
                + "\n"
                + "Month : "
                + str(rows[0][6])
                + "\n"
                + "Mobile : "
                + str(rows[0][7])
                + "\n"
                + "Address : "
                + str(rows[0][8])
            )
            # QMessageBox.information(QMessageBox(), "Successful", searchresult)
            dlg = SearchInformationDialog()
            dlg.init(self.name)
            dlg.add(searchresult, searchid)
            dlg.exec_()
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not Find patient from the database."
            )


class SearchDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog2, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search patient")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchpatient)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("ID No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchpatient(self):
        searchid = ""
        searchid = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("database2.db")
            self.c = self.conn.cursor()
            result = self.c.execute(
                "SELECT * from " + str(self.name) + " WHERE id=" + str(searchid)
            )
            # row = result.fetchone()
            rows = result.fetchall()
            searchresult = (
                "Rollno : "
                + str(rows[0][0])
                + "\n"
                + "Name : "
                + str(rows[0][1])
                + "\n"
                + "ID No : "
                + str(rows[0][2])
                + "\n"
                + "Service : "
                + str(rows[0][3])
                + "\n"
                + "Reservation Time : "
                + str(rows[0][4])
                + "\n"
                + "Day : "
                + str(rows[0][5])
                + "\n"
                + "Month : "
                + str(rows[0][6])
                + "\n"
                + "Mobile : "
                + str(rows[0][7])
                + "\n"
                + "Address : "
                + str(rows[0][8])
            )
            # QMessageBox.information(QMessageBox(), "Successful", searchresult)
            dlg = SearchInformationDialog2()
            dlg.init(self.name)
            dlg.add(searchresult, searchid)
            dlg.exec_()
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not Find patient from the database."
            )


class SearchInformationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchInformationDialog, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.setWindowTitle("Successful")
        # self.searchresult = ""
        # self.rows = None
        # self.setFixedWidth(300)
        # self.setFixedHeight(100)

        self.LabelInformation = QLabel()
        # self.LabelInformation.setText(self.searchresult)

        self.QBtn = QPushButton()
        self.QBtn.setText("More")
        self.QBtn.clicked.connect(self.patientinforamtion)

        layout = QVBoxLayout()
        layout.addWidget(self.LabelInformation)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def patientinforamtion(self):
        dlg = SearchMoreInformationDialog()
        dlg.init(self.name)
        dlg.loaddata(self.searchid)
        dlg.exec_()

    def add(self, searchresult, searchid):
        self.searchresult = searchresult
        self.searchid = searchid
        self.LabelInformation.setText(self.searchresult)


class SearchInformationDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchInformationDialog2, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.setWindowTitle("Successful")
        # self.searchresult = ""
        # self.rows = None
        # self.setFixedWidth(300)
        # self.setFixedHeight(100)

        self.LabelInformation = QLabel()
        # self.LabelInformation.setText(self.searchresult)

        self.QBtn = QPushButton()
        self.QBtn.setText("More")
        self.QBtn.clicked.connect(self.patientinforamtion)

        layout = QVBoxLayout()
        layout.addWidget(self.LabelInformation)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def patientinforamtion(self):
        dlg = SearchMoreInformationDialog2()
        dlg.init(self.name)
        dlg.loaddata(self.searchid)
        dlg.exec_()

    def add(self, searchresult, searchid):
        self.searchresult = searchresult
        self.searchid = searchid
        self.LabelInformation.setText(self.searchresult)


class SearchMoreInformationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchMoreInformationDialog, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.setWindowTitle("More Information!")

        self.tableWidget = QTableWidget()
        # self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Roll No.",
                "Name",
                "ID No",
                "Service",
                "Reservation Time",
                "Day",
                "Month",
                "Mobile Number",
                "Address",
            )
        )

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setMinimumSize(1000, 150)

    def loaddata(self, searchid):
        self.setWindowTitle("More Information about ID No: " + str(searchid))
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * from " + str(self.name) + " WHERE id=" + str(searchid)
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        self.connection.close()


class SearchMoreInformationDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchMoreInformationDialog2, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.setWindowTitle("More Information!")

        self.tableWidget = QTableWidget()
        # self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Roll No.",
                "Name",
                "ID No",
                "Service",
                "Reservation Time",
                "Day",
                "Month",
                "Mobile Number",
                "Address",
            )
        )

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setMinimumSize(1000, 150)

    def loaddata(self, searchid):
        self.setWindowTitle("More Information about ID No: " + str(searchid))
        self.connection = sqlite3.connect("database2.db")
        query = "SELECT * from " + str(self.name) + " WHERE id=" + str(searchid)
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        self.connection.close()


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")
        self.QBtn2 = QPushButton()
        self.QBtn2.setText("Delete All")

        self.setWindowTitle("Delete Patient")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletepatient)
        self.QBtn2.clicked.connect(self.deleteallpatient)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Roll No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        layout.addWidget(self.QBtn2)
        self.setLayout(layout)

    def deletepatient(self):

        delrol = ""
        delrol = self.deleteinput.text()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        result = c.execute("SELECT * from " + str(self.name))
        rows = result.fetchall()

        found = False
        for roll in rows:
            if str(roll[0]) == str(delrol):
                found = True

        if found:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute(
                "DELETE from " + str(self.name) + " WHERE roll=" + str(delrol)
            )

            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), "Successful", "Deleted From Table Successful"
            )
            self.close()
        else:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not Delete student from the database."
            )

    def deleteallpatient(self):

        """
        Delete all rows in the tasks table
        :param conn: Connection to the SQLite database
        :return:
        """
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM " + str(self.name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(
            QMessageBox(), "Successful", "All patients deleted From Table Successful"
        )
        self.close()


class DeleteDialog2(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog2, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")
        self.QBtn2 = QPushButton()
        self.QBtn2.setText("Delete All")

        self.setWindowTitle("Delete Patient")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletepatient)
        self.QBtn2.clicked.connect(self.deleteallpatient)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Roll No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        layout.addWidget(self.QBtn2)
        self.setLayout(layout)

    def deletepatient(self):

        delrol = ""
        delrol = self.deleteinput.text()
        conn = sqlite3.connect("database2.db")
        c = conn.cursor()
        result = c.execute("SELECT * from " + str(self.name))
        rows = result.fetchall()

        found = False
        for roll in rows:
            if str(roll[0]) == str(delrol):
                found = True

        if found:
            self.conn = sqlite3.connect("database2.db")
            self.c = self.conn.cursor()
            self.c.execute(
                "DELETE from " + str(self.name) + " WHERE roll=" + str(delrol)
            )

            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), "Successful", "Deleted From Table Successful"
            )
            self.close()
        else:
            QMessageBox.warning(
                QMessageBox(), "Error", "Could not Delete student from the database."
            )

    def deleteallpatient(self):

        """
        Delete all rows in the tasks table
        :param conn: Connection to the SQLite database
        :return:
        """
        self.conn = sqlite3.connect("database2.db")
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM " + str(self.name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(
            QMessageBox(), "Successful", "All patients deleted From Table Successful"
        )
        self.close()


class MassengerDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(MassengerDialog, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.setWindowTitle("Massenger")

        self.contactlabel = QLabel("Send message to:")
        self.contactinput = QLineEdit()
        self.contactinput.setPlaceholderText("Patient ID")
        self.onlyInt = QIntValidator()
        self.contactinput.setValidator(self.onlyInt)
        self.messagelabel = QLabel("Your message:")
        self.messageinput = QTextEdit()
        self.messageinput.setMinimumSize(400, 100)
        self.QBtn = QPushButton()
        self.QBtn.setText("Submit!")
        self.QBtn.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.contactlabel)
        layout.addWidget(self.contactinput)
        layout.addWidget(self.messagelabel)
        layout.addWidget(self.messageinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def send_message(self):

        self.close()


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("PMSDC")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap("stuff/picture3.jpg")
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Version 1.0.0"))
        layout.addWidget(QLabel("Copyright 2020 AP1399."))
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS "
            + str(self.name)
            + "(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,id TEXT,branch TEXT,sem INTEGER,day INTEGER,month TEXT,mobile INTEGER,address TEXT)"
        )
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")

        self.setWindowTitle("Patient Management System for Dental Clinic")

        self.setMinimumSize(1000, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Roll No.",
                "Name",
                "ID No",
                "Service",
                "Reservation Time",
                "Day",
                "Month",
                "Mobile Number",
                "Address",
            )
        )

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Patient", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Patient")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        # #
        btn_ac_massenger = QAction(QIcon("icon/massenger.png"), "Massenger", self)
        btn_ac_massenger.triggered.connect(self.massenger)
        btn_ac_massenger.setStatusTip("Massenger")
        toolbar.addAction(btn_ac_massenger)

        adduser_action = QAction(QIcon("icon/add.png"), "Insert Patient", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Search Patient", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        about_action = QAction(QIcon("icon/info.png"), "Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM " + str(self.name)
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.init(self.name)
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.init(self.name)
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.init(self.name)
        dlg.exec_()

    def massenger(self):
        dlg = MassengerDialog()
        dlg.init(self.name)
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def set_name(self, name):
        self.name = name
        print(self.name)
        self.setWindowTitle(
            "Patient Management System for Dental Clinic for " + str(self.name)
        )


class MainWindow2(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow2, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name
        self.conn = sqlite3.connect("database2.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS "
            + str(self.name)
            + "(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,id TEXT,branch TEXT,sem INTEGER,day INTEGER,month TEXT,mobile INTEGER,address TEXT)"
        )
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")

        self.setWindowTitle("Patient Management System for Dental Clinic")

        self.setMinimumSize(1000, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Roll No.",
                "Name",
                "ID No",
                "Service",
                "Reservation Time",
                "Day",
                "Month",
                "Mobile Number",
                "Address",
            )
        )

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Patient", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Patient")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.png"), "Insert Patient", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Search Patient", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        about_action = QAction(QIcon("icon/info.png"), "Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database2.db")
        query = "SELECT * FROM " + str(self.name)
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def search(self):
        dlg = SearchDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def set_name(self, name):
        self.name = name
        print(self.name)
        self.setWindowTitle(
            "Patient Management System for Dental Clinic for " + str(self.name)
        )


class MainWindow3(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow3, self).__init__(*args, **kwargs)

    def init(self, name):
        self.name = name

        # file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")

        self.setWindowTitle("Patient Management System for Dental Clinic")

        self.setMinimumSize(1000, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Roll No.",
                "Name",
                "ID No",
                "Service",
                "Reservation Time",
                "Day",
                "Month",
                "Mobile Number",
                "Address",
            )
        )

        toolbar = QToolBar()
        toolbar.setMovable(False)
        # self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Patient", self)
        # btn_ac_adduser.triggered.connect(self.insert)
        # btn_ac_adduser.setStatusTip("Add Patient")
        # toolbar.addAction(btn_ac_adduser)

        # btn_ac_refresh = QAction(QIcon("icon/refresh.png"), "Refresh", self)
        # btn_ac_refresh.triggered.connect(self.loaddata)
        # btn_ac_refresh.setStatusTip("Refresh Table")
        # toolbar.addAction(btn_ac_refresh)

        # btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        # btn_ac_search.triggered.connect(self.search)
        # btn_ac_search.setStatusTip("Search User")
        # toolbar.addAction(btn_ac_search)

        # btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        # btn_ac_delete.triggered.connect(self.delete)
        # btn_ac_delete.setStatusTip("Delete User")
        # toolbar.addAction(btn_ac_delete)

        # adduser_action = QAction(QIcon("icon/add.png"), "Insert Patient", self)
        # adduser_action.triggered.connect(self.insert)
        # file_menu.addAction(adduser_action)

        # searchuser_action = QAction(QIcon("icon/search.png"), "Search Patient", self)
        # searchuser_action.triggered.connect(self.search)
        # file_menu.addAction(searchuser_action)

        # deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        # deluser_action.triggered.connect(self.delete)
        # file_menu.addAction(deluser_action)

        about_action = QAction(QIcon("icon/info.png"), "Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.tableWidget.setRowCount(0)
        for dr in doctors:
            try:
                self.connection = sqlite3.connect("database.db")
                query = "SELECT * from " + str(dr) + f" WHERE name='{self.name}'"
                result = self.connection.execute(query)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(
                            row_number, column_number, QTableWidgetItem(str(data))
                        )
                self.connection.close()
            except:
                pass
            try:
                self.connection = sqlite3.connect("database2.db")
                query = "SELECT * from " + str(dr) + f" WHERE name='{self.name}'"
                result = self.connection.execute(query)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(
                            row_number, column_number, QTableWidgetItem(str(data))
                        )
                self.connection.close()
            except:
                pass

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def search(self):
        dlg = SearchDialog2()
        dlg.init(self.name)
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def set_name(self, name):
        self.name = name
        print(self.name)
        self.setWindowTitle(
            "Patient Management System for Dental Clinic for " + str(self.name)
        )


app = QApplication(sys.argv)
dlg = StartDialog()
dlg.exec_()
sys.exit(app.exec_())