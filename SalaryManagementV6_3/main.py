from PySide.QtGui import QApplication, QMainWindow, QStackedWidget, QMessageBox, QPixmap, QSplashScreen, QIcon
from PySide.QtCore import Qt, QFile, QIODevice
import sys

import mysql.connector

import DatabaseManager

from Home import HomeWidget
from AddEmployee import AddEmployeeWidget
from DelEmployee import DelEmployeeWidget
from EditEmployee import EditEmployeeWidget
from ShowEmployee import ShowEmployeeWidget
from AddDesignation import AddDesignationWidget
from ShowDesignation import ShowDesigationWidget
from CalculateSalary import CalculateSalaryWidget
from ShowPaySlip import ShowPaySlipWidget
from Login import LoginWidget

from ShowMySqlError import ShowMysqlError

# import resources

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("Salary Manager")
        self.setGeometry(50,50, 800, 600)

        self.setWindowIcon(QIcon("Resources/rupee.png"))

        self.widgetStack = QStackedWidget()
        self.setCentralWidget(self.widgetStack)

        self.pages = {
            "Login": LoginWidget,
            "Home": HomeWidget,
            "Add Employee": AddEmployeeWidget,
            "Del Employee": DelEmployeeWidget,
            "Edit Employee": EditEmployeeWidget,
            "Show Employee": ShowEmployeeWidget,
            "Add Designation": AddDesignationWidget,
            "Show Designation": ShowDesigationWidget,
            "Calc Salary": CalculateSalaryWidget,
            "Result": ShowPaySlipWidget
        }

        self.gotoPage("Login")

    def gotoPage(self, name, args=()):
        print "Goto page", name, ";   args=", args
        try:
            if len(args) == 0:
                newPage = self.pages[name](self)
            else:
                newPage = self.pages[name](self, *args)
            self.widgetStack.addWidget(newPage)
            self.widgetStack.setCurrentWidget(newPage)
        except mysql.connector.Error as e:
            ShowMysqlError(e, self)

    def goBack(self):
        print "Going Back"
        try:
            currentIndex = self.widgetStack.currentIndex()
            if currentIndex > 0:
                currentPage = self.widgetStack.currentWidget()
                self.widgetStack.setCurrentIndex(currentIndex-1)

                currentPage.deleteLater()
                self.widgetStack.removeWidget(currentPage)

        except mysql.connector.Error as e:
            ShowMysqlError(e, self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:

        splash_pix = QPixmap("Resources/splash.png")
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        # DatabaseManager.db = DatabaseManager.DatabaseManager(host="localhost",
        #                                                      databaseName="salaryManagement_test_1",
        #                                                      username="root",
        #                                                      password="root")

        DatabaseManager.db = DatabaseManager.DatabaseManager(host="sql12.freemysqlhosting.net",
                                                             username="sql12269310",
                                                             password="sc4Jm8WSRj",
                                                             databaseName="sql12269310")

        w = MainWindow()

        styleSheetFile = QFile("styleSheet/lightStyleSheet.css")
        styleSheetFile.open(QIODevice.ReadOnly)
        w.setStyleSheet(str(styleSheetFile.readAll()))

        w.show()

        splash.finish(w)

    except mysql.connector.Error as e:
        splash.close()
        ShowMysqlError(e)
        sys.exit()

    # except Exception as e:
    #     splash.close()
    #     msg = QMessageBox(QMessageBox.Critical, "Error", "Unexpected error occured!\n" + str(e))
    #     msg.exec_()
    #     sys.exit()

    sys.exit(app.exec_())


