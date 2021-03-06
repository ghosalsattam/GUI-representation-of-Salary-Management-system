from PySide.QtGui import QWidget, QApplication, QPushButton, QLabel,\
        QLineEdit, QComboBox, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QFrame, QFileDialog, QSpinBox, QGroupBox
from datetime import datetime
import DatabaseManager
from CustomWidgets import SearchBox, ValueBox
from ShowMySqlError import ShowMysqlError

class CalculateSalaryWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.setWindowTitle("Calculate Salary")

        t = datetime.now()
        self.month = QComboBox()
        self.month.addItems(["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                             "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"])
        self.month.setCurrentIndex(t.month - 1)
        self.year = QSpinBox()
        self.year.setRange(1900, 3000)
        self.year.setValue(t.year)


        self.name = SearchBox(self)
        self.name.setPlaceholderText("Enter Name")

        self.name.returnPressed.connect(self.setIDList)
        self.nameList = []
        self.nameList = DatabaseManager.db.getEmployeeNameList()
        self.name.setList(self.nameList)
        self.name.setCurrentIndex(-1)

        self.id = QComboBox()
        self.id.currentIndexChanged.connect(lambda: self.loadInfo(self.id.currentText()))


        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        self.originalPay = QLineEdit()
        self.originalPay.setReadOnly(True)
        self.originalPayGrade = QLineEdit()
        self.originalPayGrade.setReadOnly(True)
        self.DOJ = QLineEdit()
        self.DOJ.setReadOnly(True)
        self.pan = QLineEdit()
        self.pan.setReadOnly(True)

        self.presentPay = QLineEdit()
        self.presentPay.setReadOnly(True)
        self.da_percent = ValueBox()
        self.hra_percent = ValueBox()
        self.ta_percent = ValueBox()
        self.it_percent = ValueBox()
        self.pt_percent = ValueBox()

        self.name.editTextChanged.connect(self.clearInfo)

        self.bttnCalculate = QPushButton("Calculate")
        self.bttnCalculate.clicked.connect(self.calculate)
        self.bttnCancel = QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnCalculate.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")

        self.setupUI()


    def calculate(self):
        if "" in (self.id.currentText(),
                  self.name.text(),
                  self.designation.text(),
                  self.originalPay.text(),
                  self.originalPayGrade.text(),
                  self.DOJ.text(),
                  self.pan.text(),
                  self.da_percent.text(),
                  self.hra_percent.text(),
                  self.ta_percent.text(),
                  self.it_percent.text(),
                  self.pt_percent.text()):
            msg = QMessageBox(QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:
            if self.__parent is not None:
                self.__parent.gotoPage("Result", (self.id.currentText(),
                                      self.name.text(),
                                      self.designation.text(),
                                      self.originalPay.text(),
                                      self.originalPayGrade.text(),
                                      self.DOJ.text(),
                                      self.pan.text(),
                                      self.da_percent.text(),
                                      self.hra_percent.text(),
                                      self.ta_percent.text(),
                                      self.it_percent.text(),
                                      self.pt_percent.text(),
                                      self.month.currentText(),
                                      self.year.text()))

    def clearInfo(self):
        self.id.setCurrentIndex(-1)
        self.designation.clear()
        self.originalPay.clear()
        self.originalPayGrade.clear()
        self.DOJ.clear()
        self.pan.clear()
        self.da_percent.clear()
        self.hra_percent.clear()
        self.ta_percent.clear()
        self.it_percent.clear()
        self.pt_percent.clear()

    def loadInfo(self, id):
        print "id =", id, "...", len(id)
        if id != '':
            info = DatabaseManager.db.getEmployeeInfo(id)
            _, _, designation, originalPay, originalPayGrade, doj, pan = info
            self.designation.setText(str(designation))
            self.originalPay.setText(str(originalPay))
            self.originalPayGrade.setText(str(originalPayGrade))
            self.DOJ.setText("%02d/%02d/%4d" % (doj.day, doj.month, doj.year))
            self.pan.setText(str(pan))

            _, da, hra, ta, it, pt = DatabaseManager.db.getDesignationInfo(designation)

            self.da_percent.setText(str(da))
            self.hra_percent.setText(str(hra))
            self.ta_percent.setText(str(ta))
            self.it_percent.setText(str(it))
            self.pt_percent.setText(str(pt))

    def setIDList(self, name):
        self.id.clear()
        self.id.addItems(DatabaseManager.db.getIdListForName(name))

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        datelayout = QHBoxLayout()
        datelayout.addWidget(QLabel("Salary for month of "))
        datelayout.addWidget(self.month)
        datelayout.addWidget(self.year)
        datelayout.addStretch()
        layout.addLayout(datelayout)

        form = QFormLayout()
        form.setSpacing(10)
        form.addRow(QLabel("Name"), self.name)
        form.addRow(QLabel("ID No."), self.id)
        form.addRow(QLabel("Designation"), self.designation)
        form.addRow(QLabel("Original Pay"), self.originalPay)
        form.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form.addRow(QLabel("Date of joining"), self.DOJ)
        form.addRow(QLabel("Pan No."), self.pan)

        infoGroup = QGroupBox("Basic Info")
        infoGroup.setLayout(form)
        layout.addWidget(infoGroup)

        leftForm = QFormLayout()
        leftForm.addRow(QLabel("Dearness Allowance"), self.da_percent)
        leftForm.addRow(QLabel("Housing Rent Allowance"),self.hra_percent)
        leftForm.addRow(QLabel("Transport Allowance"), self.ta_percent)

        leftGroup = QGroupBox("Allowances")
        leftGroup.setLayout(leftForm)

        rightForm = QFormLayout()
        rightForm.addRow(QLabel("Income Tax"), self.it_percent)
        rightForm.addRow(QLabel("Profession Tax"), self.pt_percent)

        rightGroup = QGroupBox("Deductions")
        rightGroup.setLayout(rightForm)

        table = QHBoxLayout()
        table.addWidget(leftGroup)
        table.addWidget(rightGroup)

        layout.addLayout(table)


        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnCalculate)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)
