from PySide.QtGui import QWidget, QPushButton, QDateEdit, QHBoxLayout, QCalendarWidget, QMenu, QWidgetAction, QLineEdit
from PySide import QtCore

'''
datePicker is a widget to select a date from a QDateEdit Input box
or from a QCalenderWidget that drops down on clicking a button

getDate() return the selected date
'''

class DatePicker(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._dateEdit = QDateEdit()

        self._dateEdit.setDisplayFormat("dd/MM/yyyy")
        self._bttn = QPushButton("")
        self._bttn.setObjectName("MenuBttn")

        menu = QMenu(self._bttn)
        cal = QCalendarWidget()
        action = QWidgetAction(self._bttn)
        action.setDefaultWidget(cal)
        menu.addAction(action)
        self._bttn.setMenu(menu)
        cal.clicked[QtCore.QDate].connect(self._dateEdit.setDate)

        self.setupUI()

    def clear(self):
        # self._dateEdit.clear()
        self._dateEdit.findChild(QLineEdit).setText('')

    def setReadOnly(self, val=True):
        self._dateEdit.findChild(QLineEdit).setReadOnly(val)

    def setDate(self, date):
        self._dateEdit.setDate(date)

    def setupUI(self):

        self._bttn.setMaximumWidth(20)
        layout = QHBoxLayout()
        layout.addWidget(self._dateEdit)
        layout.addWidget(self._bttn)
        layout.addStretch()
        self.setLayout(layout)

    def getDate(self):
        return self._dateEdit.date()
