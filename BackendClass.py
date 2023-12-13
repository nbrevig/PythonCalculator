# Calculator Backend Class
# Nasir Brevig
# 2023-30-11 - Created class and added +-*/ functionality to the _newEquation recursive function
# 2023-7-12 - Added Parenthesis functionality and fixed previous bugs
# 2023-10-12 - added square root and squared functionality Have not yet added error messages, 
# 2023-11-12 - added testing, fixed negative numbers bug, added error messages
# 2023-11-12 - Actually fixed the negative numbers bug, added some doctests

import re

class BackendClass():
    def __init__(self, equation : str):
        """
        >>> print(BackendClass('5+5'))
        10.0
        >>> print(BackendClass('-5--5'))
        0.0
        >>> print(BackendClass('2*3+4'))
        10.0
        >>> print(BackendClass('(2+3)*4'))
        20.0
        >>> print(BackendClass('3²'))
        9.0
        >>> print(BackendClass('√9'))
        3.0
        >>> print(BackendClass('2--(2*2)'))
        6.0
        >>> print(BackendClass('1.75²+2.54*5.25/√9'))
        7.5075
        >>> print(BackendClass('23+5+((8+8+5)+(2+5))+(2+2)'))
        60.0
        >>> print(BackendClass('2.5+1.5'))
        4.0
        >>> print(BackendClass('1.25*3'))
        3.75
        >>> print(BackendClass('(2.5+3.5)*2'))
        12.0
        >>> print(BackendClass('-2--2--2--2--2+-2'))
        4.0
        >>> print(BackendClass('aa+(2.5+3.5)*2'))
        An Unexpected Error Has Occured
        >>> print(BackendClass('three time three'))
        An Unexpected Error Has Occured
        >>> print(BackendClass('2***5'))
        An Unexpected Error Has Occured
        """
        self.recursionLimit = 0
        self.equation = equation

        errorMessages = self._errorHandler(equation)


        if errorMessages == '':
            try:
                self.solution = self._getSolution(equation)
            except:
                self.solution = 'An Unexpected Error Has Occured'
        else:
            self.solution = errorMessages
    
    def _errorHandler(self, equation):
        if equation.count('(') != equation.count(')'):
            return 'Parenthesis not closed properly'
        
        return ''
        
    
    def __str__(self):
        return self.solution
    
    def _getSolution(self, equation):
        """Finds the solution of an equation, as long as its formated correctly
        >>> backendClass = BackendClass("8+8")
        >>> print(backendClass)
        16.0
        """
        openParenthesis = equation.find('(')
        closingParenthesis = equation.find(')')
        solution = ''

        while openParenthesis != -1:
            parenthesisCount = 0
            for index in range(openParenthesis, len(equation)):

                if equation[index] == '(':
                    parenthesisCount += 1
                elif equation[index] == ')':
                    parenthesisCount -= 1
                
                if parenthesisCount == 0:
                    closingParenthesis = index
                    break

            newEquation = equation[openParenthesis + 1:closingParenthesis]
            solution = self._getSolution(newEquation)
            equation = equation[:openParenthesis] + solution + equation[closingParenthesis+1:]
            openParenthesis = equation.find('(')
        
        equation = equation.replace('--','+')
        equation = equation.replace('+-','-')
        terms = re.split('[+|\-|*|/]', equation)

        

        equation = equation.replace('.', '')

        operators = re.split('[0-9]', equation)
        operators.pop(0)
        operators.pop(-1)
        operators = ''.join(operators)

        if terms[0] == '':
            terms[1] = '-' + terms[1]
            terms.pop(0)

        

        # handles squares and square roots
        for index in range(len(terms)):
            # handles squared terms
            if terms[index][-1] == '²':
                terms[index] = str(float(terms[index][:-1]) ** 2)
                operators = operators[:index] + operators[index + 1:]
                
            # handles square rooted terms
            if terms[index][0] == '√':
                terms[index] = str(float(terms[index][1:]) ** 0.5)
                operators = operators[:index] + operators[index + 1:]

        
        solved = self.solveEquation(terms, operators)
        return solved

    def _newEquation(self, terms, operators, newTerm : int, index : int) -> None:
        termFirstHalf = terms[:index]
        termFirstHalf.append(str(newTerm))
        terms = termFirstHalf + terms[index + 2:]

        return self.solveEquation(terms, operators)

    def solveEquation(self, terms, operators):
        additionIndex = operators.find('+')
        subtractionIndex = operators.find('-')
        multiplicationIndex = operators.find('*')
        divisionIndex = operators.find('/')

        self.recursionLimit += 1
        if self.recursionLimit > 100000000:
            return 'Reached Recursion Limit'

        #print(terms, operators)

        if multiplicationIndex != -1 or divisionIndex != -1:
            if multiplicationIndex < divisionIndex and multiplicationIndex != -1 or divisionIndex == -1:
                product = float(terms[multiplicationIndex]) * float(terms[multiplicationIndex + 1])
                operators = operators[:multiplicationIndex] + operators[multiplicationIndex + 1:]
                return self._newEquation(terms, operators, product, multiplicationIndex)
                
            elif divisionIndex != -1:
                divident = float(terms[divisionIndex]) / float(terms[divisionIndex + 1])
                operators = operators[:divisionIndex] + operators[divisionIndex + 1:]
                return self._newEquation(terms, operators, divident, divisionIndex)
                
            
        elif additionIndex != -1 or subtractionIndex != -1:
            if additionIndex < subtractionIndex and additionIndex != -1 or subtractionIndex == -1:
                sum = float(terms[additionIndex]) + float(terms[additionIndex + 1])
                operators = operators[:additionIndex] + operators[additionIndex + 1:]
                return self._newEquation(terms, operators, sum, additionIndex)
                
            else:
                difference = float(terms[subtractionIndex]) - float(terms[subtractionIndex + 1])
                operators = operators[:subtractionIndex] + operators[subtractionIndex + 1:]
                return self._newEquation(terms, operators, difference, subtractionIndex)
        return terms[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #print(BackendClass('-5--5'))