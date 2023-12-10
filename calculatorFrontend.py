# Frontend class by Andrew Eno
# Created on November 19, 2023
# Modified often enough that I got annoyed by forgetting to keep a log

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
import os
import sys

BACKEND_EXISTS = False

# This makes sure the backend exists
if os.path.exists('BackendClass.py'):
    BACKEND_EXISTS = True
    from BackendClass import BackendClass

class CustomCalcButton(QPushButton):
    ''' CustomCalcButton is a class of QPushButton that contains special methods and styles for the buttons on the calculator '''
    # These are the styles
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
    # The custom style is just a slightly modified default style
    CUSTOM_VALUES = {"background-color": "#bababa", "text-color": "black", "hover": "#aaaaaa", "pressed": "#9a9a9a"}
    CUSTOM_STYLE = DEFAULT_STYLE.replace("#343a40", CUSTOM_VALUES['background-color']).replace("white", CUSTOM_VALUES['text-color']).replace("#30373c", CUSTOM_VALUES['hover']).replace("#2d3339", CUSTOM_VALUES['pressed'])
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
    # Same for this custom style, but this style is different to make an accent button
    CUSTOM_SPECIAL = {"background-color": "#98ABCF", "text-color": "black", "hover": "#7289A5", "pressed": "#727980"}
    CUSTOM_RED = CE_STYLE.replace("#dc3545", CUSTOM_SPECIAL["background-color"]).replace("white", CUSTOM_SPECIAL["text-color"]).replace("#d93040", CUSTOM_SPECIAL["hover"]).replace("#d52030", CUSTOM_SPECIAL["pressed"])
    buttons = [] # This is where each button is added when they are initialized

    def __init__(self, text='button', red=False, calculator=None, functionality=None): # Functionality should be a function
        super().__init__()
        self.setStyleSheet(self.DEFAULT_STYLE)
        self.red = red
        if self.red:
            self.setStyleSheet(self.CE_STYLE)
        self.setText(text)
        self.calculator = calculator
        self.clicked.connect(self.wasPressed) # Connect the wasPressed method to the button's press
        self.functionality = functionality
        self.buttons.append(self) # Add self to the buttons list
    def wasPressed(self):
        '''executes when the button is pressed'''
        if self.calculator.needsToBeCleared:
            self.calculator.clearDisplay()
            self.calculator.needsToBeCleared = False
        if self.calculator != None and self.functionality == None:
            self.calculator.addText(self.text() if self.text() != 'n²' else "²")
        elif self.functionality != None: # If it has functionality more than just text
            self.functionality()
    def switchButtonsStyle(self):
        '''Switches the style of a button between default and custom'''
        for button in self.buttons: # This is where the buttons list comes in handy, goes through each and toggles their theme from default to custom or back again
            if button.styleSheet() == self.DEFAULT_STYLE or button.styleSheet() == self.CE_STYLE:
                button.setStyleSheet(self.CUSTOM_STYLE if not button.red else self.CUSTOM_RED)
            else:
                button.setStyleSheet(self.DEFAULT_STYLE if not button.red else self.CE_STYLE)

class Calculator(QMainWindow):
    ''' Calculator class of QMainWindow is the window for the calculator, provides all the methods and things that are available to the buttons since it is passed as an argument to them '''
    # Styles defined here again
    WINDOW_STYLE = '''QMainWindow { background-color:#3f3f3f;}
    QLineEdit { background-color:#2f2f2f; border-radius: 4px; border: #0f0f0f; min-height:16px; max-height: 128px; color: white; font: bold 14px; }'''
    CUSTOM_VALUES = {"window-background": "#EFEFEF", "label-background": "#CFCFCF", "label-text-color": "black"}
    CUSTOM_STYLE = WINDOW_STYLE.replace("#3f3f3f", CUSTOM_VALUES['window-background']).replace("#2f2f2f", CUSTOM_VALUES['label-background']).replace("white", CUSTOM_VALUES['label-text-color'])
    def __init__(self, backend=False):
        super().__init__()
        # Lots of variable initializing here
        self.needsToBeCleared = False

        self.setWindowTitle('Calculator')
        self.setStyleSheet(self.WINDOW_STYLE)

        self.display = QLineEdit()
        self.display.setReadOnly(False)

        # Row one is the display, don't need an HBox for that
        # This is all the layout stuff. Every button is added manually because that's how I started it and I don't want to refactor because it works fine :)
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.row4 = QHBoxLayout()
        self.row5 = QHBoxLayout()
        self.row6 = QHBoxLayout()
        self.row7 = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        ceButton = CustomCalcButton("Theme", True, calculator=self, functionality=self.changeTheme)
        self.cButton = CustomCalcButton('CE', calculator=self, functionality=self.clearDisplay)
        recipButton = CustomCalcButton('1/x', calculator=self, functionality=self.reciperical)
        delButton = CustomCalcButton('⌫', calculator=self, functionality=self.backspace)

        divButton = CustomCalcButton('/', calculator=self)
        multButton = CustomCalcButton('*', calculator=self)
        addButton = CustomCalcButton('+', calculator=self)
        minusButton = CustomCalcButton('-', calculator=self)
        equalsButton = CustomCalcButton('=', calculator=self, functionality=self.sendBackend)
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
        self.row2.addWidget(self.cButton)
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
        ''' Add text to the text of this calculator's display '''
        self.display.setText(self.display.text() + "" + text)

    def sendBackend(self):
        ''' Sends the display's text to the backend class to be processed, and display the value it returns '''
        if BACKEND_EXISTS:
            x = BackendClass(self.display.text())
            self.display.setText(str(x))
        else:
            print("Woopsie, there doesn't seem to be a backend class at the moment... ")
        self.needsToBeCleared = True
    def clearDisplay(self):
        ''' Clears the display of all text '''
        self.display.setText("")
    def backspace(self, charsToDel=2):
        ''' Takes one character out of the current text '''
        self.display.setText(self.display.text()[:len(self.display.text()) - charsToDel]) # Chars to del defaults to 2 because it is also deleting the backspace character
    def changeTheme(self):
        ''' Changes the theme of the window itself '''
        if self.styleSheet() == self.CUSTOM_STYLE:
            self.setStyleSheet(self.WINDOW_STYLE)
        else:
            self.setStyleSheet(self.CUSTOM_STYLE)
        self.cButton.switchButtonsStyle()
    def reciperical(self):
        ''' Replace the text of the display with it's reciperical '''
        self.display.setText(f"1/({self.display.text()})")

# Initialize all the things
app = QApplication(sys.argv)

window = Calculator(BACKEND_EXISTS)
window.show()

app.exec()