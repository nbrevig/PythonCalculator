# Frontend class by Andrew Eno
# Created on November 19, 2023

# BackendClass expects one argument, a string such as BackendClass('14 + 2')
# Converting it to string makes it return the answer
# Add parenthesis for sure
# Possibly square root and square, pehaps use unicode


from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide6.QtCore import QPropertyAnimation, Signal, Property
from PySide6.QtGui import QColor, QFocusEvent
import os
import sys

BACKEND_EXISTS = False

if os.path.exists('BackendClass.py'):
    BACKEND_EXISTS = True
    from BackendClass import BackendClass

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

    def __init__(self, text='button', red=False, calculator=None):
        super().__init__()
        self.setStyleSheet(self.DEFAULT_STYLE)
        if red:
            self.setStyleSheet(self.CE_STYLE)
        self.setText(text)
        self.calculator = calculator
        self.isSubmitButton = False if text != '=' else True
        self.isBackButton = False if text != '⌫' else True
        self.clicked.connect(self.wasPressed)
    def wasPressed(self):
        if self.calculator.needsToBeCleared:
            self.calculator.clearDisplay()
            self.calculator.needsToBeCleared = False
        if self.calculator != None:
            self.calculator.addText(self.text())
        if self.isSubmitButton:
            self.calculator.backspace(1)
            self.calculator.sendBackend()
        elif self.isBackButton:
            self.calculator.backspace()

class Calculator(QMainWindow):
    WINDOW_STYLE = '''QMainWindow { background-color:#3f3f3f; }'''
    DISPLAY_STYLE = '''QLineEdit { background-color:#2f2f2f; border-radius: 4px; border: #0f0f0f; min-height:16px; max-height: 128px; color: white; font: bold 14px; }'''
    def __init__(self, backend=False):
        super().__init__()
        self.needsToBeCleared = False

        self.setWindowTitle('Calculator')
        self.setStyleSheet(self.WINDOW_STYLE)

        self.display = QLineEdit()
        self.display.setReadOnly(False)
        self.display.setStyleSheet(self.DISPLAY_STYLE)

        # Row one is the display, don't need an HBox for that
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.row4 = QHBoxLayout()
        self.row5 = QHBoxLayout()
        self.row6 = QHBoxLayout()
        self.row7 = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        ceButton = CustomCalcButton("CE", True, calculator=self)
        cButton = CustomCalcButton('C', calculator=self)
        recipButton = CustomCalcButton('1/x', calculator=self)
        delButton = CustomCalcButton('⌫', calculator=self)

        divButton = CustomCalcButton('/', calculator=self)
        multButton = CustomCalcButton('*', calculator=self)
        addButton = CustomCalcButton('+', calculator=self)
        minusButton = CustomCalcButton('-', calculator=self)
        equalsButton = CustomCalcButton('=', calculator=self)
        dotButton = CustomCalcButton('.', calculator=self)

        sqrtButton = CustomCalcButton("√", calculator=self)
        sqrButton = CustomCalcButton("n²", calculator=self)
        leftParenButton = CustomCalcButton("(", calculator=self)
        rightParenButton = CustomCalcButton(")", calculator=self)

        num0 = CustomCalcButton('0', calculator=self)
        num1 = CustomCalcButton('1', calculator=self)
        num2 = CustomCalcButton('2', calculator=self)
        num3 = CustomCalcButton('3', calculator=self)
        num4 = CustomCalcButton('4', calculator=self)
        num5 = CustomCalcButton('5', calculator=self)
        num6 = CustomCalcButton('6', calculator=self)
        num7 = CustomCalcButton('7', calculator=self)
        num8 = CustomCalcButton('8', calculator=self)
        num9 = CustomCalcButton('9', calculator=self)

        self.mainLayout.addWidget(self.display)

        self.row2.addWidget(ceButton)
        self.row2.addWidget(cButton)
        self.row2.addWidget(recipButton)
        self.row2.addWidget(delButton)
        self.mainLayout.addLayout(self.row2)

        self.row3.addWidget(sqrtButton)
        self.row3.addWidget(sqrButton)
        self.row3.addWidget(leftParenButton)
        self.row3.addWidget(rightParenButton)
        self.mainLayout.addLayout(self.row3)

        self.row4.addWidget(num7)
        self.row4.addWidget(num8)
        self.row4.addWidget(num9)
        self.row4.addWidget(divButton)
        self.mainLayout.addLayout(self.row4)

        self.row5.addWidget(num4)
        self.row5.addWidget(num5)
        self.row5.addWidget(num6)
        self.row5.addWidget(multButton)
        self.mainLayout.addLayout(self.row5)

        self.row6.addWidget(num1)
        self.row6.addWidget(num2)
        self.row6.addWidget(num3)
        self.row6.addWidget(minusButton)
        self.mainLayout.addLayout(self.row6)

        self.row7.addWidget(dotButton)
        self.row7.addWidget(num0)
        self.row7.addWidget(equalsButton)
        self.row7.addWidget(addButton)
        self.mainLayout.addLayout(self.row7)

        mainWidget = QWidget()
        self.mainLayout.setSpacing(8)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)
    
    def addText(self, text):
        self.display.setText(self.display.text() + "" + text)

    def sendBackend(self):
        if BACKEND_EXISTS:
            x = BackendClass(self.display.text())
            self.display.setText(str(x))
        else:
            print("Woopsie, there doesn't seem to be a backend class at the moment... ")
        self.needsToBeCleared = True
    def clearDisplay(self):
        self.display.setText("")
    def backspace(self, charsToDel=2):
        self.display.setText(self.display.text()[:len(self.display.text()) - charsToDel]) # Chars to del defaults to 2 because it is also deleting the backspace character

app = QApplication(sys.argv)

window = Calculator(BACKEND_EXISTS)
window.show()

app.exec()