from PySide.QtGui import QComboBox, QStringListModel, QCompleter, QApplication, QShortcut, QKeySequence, QLineEdit
from PySide.QtCore import Qt, Signal
import sys

'''
Creates an input box which shows suggestions based on the list passed in the init function
'''

class SearchBox(QComboBox):
    returnPressed = Signal(str)

    def __init__(self, parent=None, list=[]):
        QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)

        self.addItems(list)
        autoCompleteModel = QStringListModel(list)
        completer = QCompleter()
        completer.setModel(autoCompleteModel)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.setCompleter(completer)

        self.setEditText("")

        self.__textChangeStatus = True
        self.editTextChanged.connect(self.__onTextChange)
        shortcut = QShortcut(QKeySequence(Qt.Key_Return), self, self.__onEnter)
        shortcut = QShortcut(QKeySequence(Qt.Key_Enter), self, self.__onEnter)

    def __onTextChange(self):
        self.__textChangeStatus = True

    def __onEnter(self):
        if self.__textChangeStatus:
            print "Enter", self.text()
            self.returnPressed.emit(self.text())
            self.__textChangeStatus = False

    def setPlaceholderText(self, text):
        self.findChild(QLineEdit).setPlaceholderText(text)

    def text(self):
        return self.currentText()

    def setList(self, list):
        self.clear()
        self.addItems(list)
        autoCompleteModel = QStringListModel(list)
        completer = QCompleter()
        completer.setModel(autoCompleteModel)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(completer)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SearchBox(None, ["hello", "hi"])
    def func(string):
        print string
    w.editTextChanged.connect(func)
    w.show()
    sys.exit(app.exec_())