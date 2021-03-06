import DatabaseManager
from PySide import QtGui
from CustomWidgets import SearchBox


class DelEmployeeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DelEmployeeWidget, self).__init__(parent)
        self.__parent = parent
        self.setWindowTitle("Delete Employee")
        self.idList = []

        nameList = DatabaseManager.db.getEmployeeNameList()
        self.name = SearchBox(self, nameList)
        self.name.setPlaceholderText("Enter Name")

        self.name.returnPressed.connect(self.setIdList)

        self.id = QtGui.QComboBox()
        self.id.currentIndexChanged.connect(lambda: self.updateInformation(self.id.currentText()))

        self.designation = QtGui.QLineEdit()
        self.designation.setReadOnly(True)
        self.joinDate = QtGui.QLineEdit()
        self.joinDate.setReadOnly(True)
        self.panNo = QtGui.QLineEdit()
        self.panNo.setReadOnly(True)

        self.remove = QtGui.QPushButton("Remove Employee")
        self.remove.clicked.connect(self.removeEmployee)
        self.remove.setObjectName("CancelButton")

        self.back = QtGui.QPushButton("Back")
        self.back.clicked.connect(self.goBack)
        self.back.setObjectName("OkButton")

        self.createWindowLayout()

    def loadNameList(self):
        self.name = SearchBox(self, DatabaseManager.db.getEmployeeNameList())


    def setIdList(self, name):
        self.id.clear()
        self.id.addItems(DatabaseManager.db.getIdListForName(name))

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def updateInformation(self, id):

        info = DatabaseManager.db.getEmployeeInfo(id)
        if info is None:
            self.designation.clear()
            self.joinDate.clear()
            self.panNo.clear()
        else:
            id, name, des, opa, opag, doj, pan = info
            self.designation.setText(des)
            self.joinDate.setText("%02d/%02d/%04d" % (doj.day, doj.month, doj.year))
            self.panNo.setText(pan)

    def createWindowLayout(self):

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)

        formLayout = QtGui.QFormLayout()
        formLayout.setSpacing(20)

        formLayout.addRow(QtGui.QLabel("Name"), self.name)
        formLayout.addRow(QtGui.QLabel("Employee ID"), self.id)
        formLayout.addRow(QtGui.QLabel("Designation"), self.designation)
        formLayout.addRow(QtGui.QLabel("Date of join"), self.joinDate)
        formLayout.addRow(QtGui.QLabel("Pan No"), self.panNo)

        mainLayout.addLayout(formLayout)

        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.back)
        bttnLayout.addWidget(self.remove)
        mainLayout.addLayout(bttnLayout)

        self.setLayout(mainLayout)

    def removeEmployee(self):

        if str(self.id.currentText()) == "":
            msg = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error!!!", "First enter all the information", parent=self)
            msg.exec_()
        else:
            choice = QtGui.QMessageBox.question(self, 'Remove Confirmation!!!',
                                                "Are you sure you want to delete this employee?\nName: " + str(
                                                    self.name.text()) + "\nID: " +
                                                    self.id.currentText() + "\nDesignation: " + str(
                                                    self.designation.text()),
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                try:
                    DatabaseManager.db.delEmployee(self.id.currentText(), self.name.text())
                    msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Deleted Successfully", parent=self)
                    msg.exec_()
                    # reload name list
                    self.name.clear()
                    nameList = DatabaseManager.db.getEmployeeNameList()
                    self.name.addItems(nameList)
                    self.name.setCurrentIndex(-1)

                except Exception as e:
                    raise e

