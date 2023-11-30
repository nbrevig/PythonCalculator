from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide6.QtCore import QPropertyAnimation, Signal, Property
from PySide6.QtGui import QColor, QFocusEvent
import os
import sys

BACKEND_EXISTS = False

if os.path.exists('BackendClass.py'):
    BACKEND_EXISTS = True
    import BackendClass
    MainBackend = BackendClass()

class CustomCalcButton(QPushButton):
    DEFAULT_STYLE = '''QPushButton { 
    background-color:#343a40;
    border-style: outset;
    font-size: 1rem;
    border-width: 0px;
    border-radius: 4px;
    font: bold 14px;
    min-width: 16px;
    min-height: 16px;
    max-height: 256px;
    padding: 6px;
    margin: 0px;
    color: white; }
    QPushButton:hover {background-color:#30373c}
    QPushButton:pressed {background-color:#2d3339}'''
    CE_STYLE = '''QPushButton { 
    background-color:#dc3545;
    border-style: outset;
    border-width: 0px;
    border-radius: 4px;
    font: bold 14px;
    margin: 0px;
    min-width: 16px;
    min-height: 16px;
    max-height: 256px;
    padding: 6px; 
    color: white; }
    QPushButton:hover {background-color:#d93040}
    QPushButton:pressed {background-color:#d52030}'''

    # BackendClass expects one argument, a string such as BackendClass('14 + 2')
    # Converting it to string makes it return the answer
    # Add parenthesis for sure
    # Possibly square root and square, pehaps use unicode

    def __init__(self, text='button', red=False, backend=False, displayToUpdate=None):
        super().__init__()
        self.setStyleSheet(self.DEFAULT_STYLE)
        if red:
            self.setStyleSheet(self.CE_STYLE)
        self.setText(text)
        self.hasBackend = backend
        self.displayToUpdate = displayToUpdate
        self.clicked.connect(displayToUpdate.setDisplayText(self.text))
    def wasPressed(self):
        if self.hasBackend:
            global MainBackendClass
            MainBackendClass.sendPress(self.text) # Backend class has method sendPress to send the button pressed (sends the text of the button pressed, i.e. '1', '2', '3', etc.)
            if self.displayToUpdate != None:
                self.displayToUpdate.setText(MainBackendClass.getText()) # Backend class has method getText() to get the text to be put on the label

class Calculator(QMainWindow):
    WINDOW_STYLE = '''QMainWindow { background-color:#3f3f3f; }'''
    DISPLAY_STYLE = '''QLineEdit { background-color:#2f2f2f; border-radius: 4px; border: #0f0f0f; min-height:16px; max-height: 128px; color: white; font: bold 14px; }'''
    def __init__(self, backend=False):
        super().__init__()

        self.setWindowTitle('Calculator')
        self.setStyleSheet(self.WINDOW_STYLE)

        # Row one is the display, don't need an HBox for that
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.row4 = QHBoxLayout()
        self.row5 = QHBoxLayout()
        self.row6 = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        ceButton = CustomCalcButton("CE", True, backend)
        cButton = CustomCalcButton('C', backend)
        recipButton = CustomCalcButton('1/x', backend)
        delButton = CustomCalcButton('⌫', backend)

        divButton = CustomCalcButton('/', backend)
        multButton = CustomCalcButton('*', backend)
        addButton = CustomCalcButton('+', backend)
        minusButton = CustomCalcButton('-', backend)
        equalsButton = CustomCalcButton('=', backend)
        dotButton = CustomCalcButton('.', backend)

        num0 = CustomCalcButton('0', backend)
        num1 = CustomCalcButton('1', backend)
        num2 = CustomCalcButton('2', backend)
        num3 = CustomCalcButton('3', backend)
        num4 = CustomCalcButton('4', backend)
        num5 = CustomCalcButton('5', backend)
        num6 = CustomCalcButton('6', backend)
        num7 = CustomCalcButton('7', backend)
        num8 = CustomCalcButton('8', backend)
        num9 = CustomCalcButton('9', backend)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setText('0123456789876543210')
        self.display.setStyleSheet(self.DISPLAY_STYLE)

        self.mainLayout.addWidget(self.display)

        self.row2.addWidget(ceButton)
        self.row2.addWidget(cButton)
        self.row2.addWidget(recipButton)
        self.row2.addWidget(delButton)
        self.mainLayout.addLayout(self.row2)

        self.row3.addWidget(num7)
        self.row3.addWidget(num8)
        self.row3.addWidget(num9)
        self.row3.addWidget(divButton)
        self.mainLayout.addLayout(self.row3)

        self.row4.addWidget(num4)
        self.row4.addWidget(num5)
        self.row4.addWidget(num6)
        self.row4.addWidget(multButton)
        self.mainLayout.addLayout(self.row4)

        self.row5.addWidget(num1)
        self.row5.addWidget(num2)
        self.row5.addWidget(num3)
        self.row5.addWidget(minusButton)
        self.mainLayout.addLayout(self.row5)

        self.row6.addWidget(dotButton)
        self.row6.addWidget(num0)
        self.row6.addWidget(equalsButton)
        self.row6.addWidget(addButton)
        self.mainLayout.addLayout(self.row6)

        mainWidget = QWidget()
        self.mainLayout.setSpacing(8)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)
    
    def setDisplayText(self, text):
        self.display.setText(text)

app = QApplication(sys.argv)

window = Calculator()
window.show()

app.exec()