from PySide import QtGui
from PySide.QtCore import Qt, QRegExp
import sys
import mysql.connector
from ShowMySqlError import ShowMysqlError
import DatabaseManager

class LoginWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        self._parent = parent

        self.logo = QtGui.QLabel()
        self.logo.setPixmap("Resources/iiitk.png")

        self.username = QtGui.QLineEdit(self)
        self.username.setPlaceholderText("Enter username")

        self.password = QtGui.QLineEdit(self)
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QtGui.QLineEdit.Password)

        reg_ex = QRegExp("[a-zA-Z0-9-_]+")
        username_validator = QtGui.QRegExpValidator(reg_ex, self.username)
        self.username.setValidator(username_validator)

        self.password.returnPressed.connect(self.doLogin)

        self.showPass = QtGui.QCheckBox("Show Password")
        self.showPass.stateChanged.connect(self.handleShowPassword)
        self.bttnLogin = QtGui.QPushButton("Login", self)
        self.bttnLogin.setObjectName("BigButton")
        self.bttnLogin.clicked.connect(self.doLogin)

        self.setupUI()

    def handleShowPassword(self):
        if self.showPass.isChecked():
            self.password.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtGui.QLineEdit.Password)

    def doLogin(self):
        try:
            if DatabaseManager.db.checkLogin(self.username.text(), self.password.text()):
                if self._parent is not None:
                    self._parent.gotoPage("Home")
            else:
                QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')
        except mysql.connector.Error as e:
            ShowMysqlError(e,self)

    def setupUI(self):

        layout = QtGui.QVBoxLayout()

        self.setContentsMargins(20, 10, 20, 5)
        banner = QtGui.QHBoxLayout()
        banner.addStretch()
        banner.addWidget(self.logo)
        bannerText = QtGui.QVBoxLayout()
        text = QtGui.QLabel("Salary Management System")
        text.setStyleSheet("font-size: 30px;")
        bannerText.addWidget(text)
        bannerText.setAlignment(text, Qt.AlignBottom)
        text2 = QtGui.QLabel("Indian Institute of Information Technology Kalyani")
        text2.setStyleSheet("font-size: 20px;")
        bannerText.addWidget(text2)
        bannerText.setAlignment(text2, Qt.AlignTop)
        banner.addLayout(bannerText)
        banner.addStretch()
        layout.addLayout(banner)
        layout.addSpacing(30)

        loginGroup = QtGui.QGroupBox("Login")
        loginGroup.setMinimumWidth(300)
        loginLayout = QtGui.QVBoxLayout()
        form = QtGui.QFormLayout()
        form.addRow(QtGui.QLabel("Username"), self.username)
        form.addRow(QtGui.QLabel("Password"), self.password)
        loginLayout.addLayout(form)
        loginLayout.addSpacing(10)
        loginLayout.addWidget(self.showPass)
        loginLayout.addSpacing(30)

        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnLogin)
        loginLayout.addLayout(bttnLayout)
        loginGroup.setLayout(loginLayout)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(loginGroup)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addStretch()
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    w = LoginWidget()
    w.show()

    sys.exit(app.exec_())

