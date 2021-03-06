import DatabaseManager
from PySide import QtGui
from PySide.QtCore import Qt

import sys

class ShowEmployeeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent

        self.table = QtGui.QTableWidget(self)

        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.loadTable()

        self.bttnBack = QtGui.QPushButton("Back")
        self.bttnBack.clicked.connect(self.goBack)
        self.bttnBack.setObjectName("BigButton")

        self.setupUI()

    def loadTable(self):

        info = DatabaseManager.db.getAllEmployeeInfo()
        self.table.setRowCount(len(info))
        self.table.setColumnCount(len(info[0]))

        for i in range(len(info)):
            for j in range(len(info[0])):
                self.table.setItem(i, j, QtGui.QTableWidgetItem(str(info[i][j])))

        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Designation", "Original Pay", "Original Pay Grade", "DOJ", "PAN"])
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)

    def setupUI(self):
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        layout.addWidget(self.table)

        layout.addSpacing(50)
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnBack)


        layout.addLayout(bttnLayout)
        self.setLayout(layout)


    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()


if __name__ == "__main__":
    DatabaseManager.db = DatabaseManager.DatabaseManager(host="sql12.freemysqlhosting.net",
                                                         username="sql12269310",
                                                         password="sc4Jm8WSRj",
                                                         databaseName="sql12269310")
    app = QtGui.QApplication(sys.argv)

    w = ShowEmployeeWidget()
    w.show()

    sys.exit(app.exec_())