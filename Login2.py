from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QMainWindow,
    QMessageBox,
)
from PyQt5 import QtGui, QtPrintSupport

import sys, sqlite3

doctors = ["Jahanshahi", "Amini", "Ghobari", "Ghodsifar"]

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.name = "none"
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.doctors = doctors

        username = QLabel("Username")
        pw = QLabel("Password")

        self.buttonRegister = QPushButton("Register", self)
        self.buttonRegister.clicked.connect(self.handleRegister)

        self.buttonLogin = QPushButton("Login", self)
        # self.buttonLogin.clicked.connect(self.handleLogin)

        loginbox = QGridLayout(self)
        loginbox.setSpacing(10)

        loginbox.addWidget(username, 1, 0)
        loginbox.addWidget(self.textName, 1, 1)

        loginbox.addWidget(pw, 2, 0)
        loginbox.addWidget(self.textPass, 2, 1)

        loginbox.addWidget(self.buttonRegister, 3, 0)
        loginbox.addWidget(self.buttonLogin, 3, 1)

        self.setWindowTitle("Login")

        self.buttonLogin.clicked.connect(self.login)

    def handleRegister(self):
        self.doctors.append(self.textName.text())

    def login(self):
        self.name = self.textName.text()
        name = False
        for doctor in self.doctors:
            if self.textName.text() == doctor and self.textPass.text() == "AP1399":
                name = True
                self.accept()
        if not name:
            QMessageBox.warning(self, "Error", "Wrong Password Or Undefined Name!")


class PatientLogin(QDialog):
    def __init__(self, parent=None):
        super(PatientLogin, self).__init__(parent)

        self.name = "No body"
        self.label = QLabel(self)
        self.label.setText("Notify that your password is your ID number!")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)

        # patients as users

        username = QLabel("Username")
        pw = QLabel("Password")

        self.buttonLogin = QPushButton("Login", self)

        loginbox = QGridLayout(self)
        loginbox.setSpacing(10)

        loginbox.addWidget(username, 1, 0)
        loginbox.addWidget(self.textName, 1, 1)
        loginbox.addWidget(self.label, 0, 0)

        loginbox.addWidget(pw, 2, 0)
        loginbox.addWidget(self.textPass, 2, 1)

        loginbox.addWidget(self.buttonLogin, 3, 1)

        self.setWindowTitle("Login")

        self.buttonLogin.clicked.connect(self.login)

    def login(self):
        self.username = self.textName.text()
        self.name = self.username
        self.password = ""

        count1 = 0
        count2 = 0
        for dr in doctors:
            try:
                self.conn = sqlite3.connect("database.db")
                self.curser = self.conn.cursor()
                result = self.curser.execute(
                    "SELECT * from " + str(dr) + f" WHERE name='{str(self.username)}'"
                )
                row = result.fetchone()
                self.password = row[2]
            except:
                count1 = count1 + 1
            try:
                self.conn2 = sqlite3.connect("database2.db")
                self.curser2 = self.conn2.cursor()
                result2 = self.curser2.execute(
                    "SELECT * from " + str(dr) + f" WHERE name='{str(self.username)}'"
                )
                row = result2.fetchone()
                self.password = row[2]
            except:
                count2 = count2 + 1

        if count1 == len(doctors) and count2 == len(doctors):
            QMessageBox.warning(self, "Error", "Undefined Name!")
        else:
            if self.textPass.text() == self.password:
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Wrong Password!")


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())