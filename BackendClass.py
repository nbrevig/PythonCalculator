# Calculator Backend Class
# Nasir Brevig
# 2023-30-11 - Created class and added +-*/ functionality to the _newEquation recursive function
# 2023-7-12 - Added Parenthesis functionality and fixed previous bugs
# 2023-10-12 - added square root and squared functionality

import re

class BackendClass():
    def __init__(self, equation : str):
        """
        example of terms str: '5+2+3'
        """
        self.i = 0
        self.equation = equation

        self.solution = self._getSolution(equation)
        #print(self.solution)
        
        #self.solveEquation(self.terms, self.operators)
    
    def __str__(self):
        return self.solution
    
    def _getSolution(self, equation):
        openParenthesis = equation.find('(')
        closingParenthesis = equation.find(')')
        solution = ''

        while openParenthesis != -1:
            print('hasParenthesis')
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
        print(equation)
        
        terms = re.split('[+|-|*|/]', equation)

        equation = equation.replace('.', '')
        operators = re.split('[0-9]', equation)
        operators.pop(0)
        operators.pop(-1)
        operators = ''.join(operators)
        
        print(terms, operators)
        #adds negative terms and handles squares and square roots
        for index in range(len(terms)):
            #handles negative terms
            if terms[index] == '':
                terms[index+1] = '-' + terms[index+1]
                terms.pop(index)
                if index > 0:
                    operators = operators[:index] + operators[index + 1:]

            # handles squared terms
            if terms[index][-1] == '²':
                terms[index] = str(float(terms[index][:-1]) ** 2)
                operators = operators[:index] + operators[index + 1:]
            
            # handles square rooted terms
            if terms[index][0] == '√':
                terms[index] = str(float(terms[index][1:]) ** 0.5)
                operators = operators[:index] + operators[index + 1:]

        solved = self.solveEquation(terms, operators)
        print(solved)
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

       

        self.i += 1
        if self.i > 1000:
            return

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
    BackendClass('1.75²+2.54*5.25/√9')

    """
    tests
    '-8+-5'
    1.75²+2.54*5.25/√9
    '-8*-5'
    '-8*-5/5'
    '-8--5+5*5/-3'
    '(8+8+5)'
    '(8.5+8+5)'
    '((8+8+5))'
    '(8+8)+(8+2)+(8+1)'
    ((8+8+5))+(2+2)
    ((8+8+5)+2)+(2+2)
    ((8+8+5)+(2+2))+2
    ((8+8+5)+(2+5))+(2+2)
    23+5+((8+8+5)+(2+5))+(2+2)
    √5
    5²
    """