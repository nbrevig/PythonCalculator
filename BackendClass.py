# Calculator Backend Class
# Nasir Brevig
import re

class BackendClass():
    def __init__(self, equation : str):
        """
        example of terms str: '5+2+3'
        """
        self.i = 0
        operators = re.split('[0-9]', equation)
        operators.pop(0)
        operators.pop(-1)
        self.operators = ''.join(operators)

        self.terms = re.split('[+-/*//]', equation)
        #print(self.operators)
        #adds negative terms
        for term in self.terms:
            if term == '':
                index = self.terms.index(term)
                self.terms[index+1] = '-' + self.terms[index+1]
                self.terms.pop(index)
                if index > 0:
                    self.operators = self.operators[:index] + self.operators[index + 1:]

        
        
        #print(self.terms, self.operators)
        self.solveEquation(self.terms, self.operators)
    
    def __str__(self):
        return self.getSolution()
    
    def _newEquation(self, term : int, index) -> None:
        termFirstHalf = self.terms[:index]
        termFirstHalf.append(str(term))
        self.terms = termFirstHalf + self.terms[index + 2:]
        self.operators = self.operators[:index] + self.operators[index + 1:]

        self.solveEquation(self.terms, self.operators)

    def solveEquation(self, terms, operators):
        additionIndex = operators.find('+')
        subtractionIndex = operators.find('-')
        multiplicationIndex = operators.find('*')
        divisionIndex = operators.find('/')

        self.i += 1
        if self.i > 8:
            return

        #print(self.terms, self.operators)
        if multiplicationIndex != -1 or divisionIndex != -1:
            if multiplicationIndex < divisionIndex and multiplicationIndex != -1 or divisionIndex == -1:
                product = float(terms[multiplicationIndex]) * float(terms[multiplicationIndex + 1])

                self._newEquation(product, multiplicationIndex)
            elif divisionIndex != -1:
                divident = float(terms[divisionIndex]) / float(terms[divisionIndex + 1])

                self._newEquation(divident, divisionIndex)
            
        elif additionIndex != -1 or subtractionIndex != -1:
            if additionIndex < subtractionIndex and additionIndex != -1 or subtractionIndex == -1:
                sum = float(terms[additionIndex]) + float(terms[additionIndex + 1])
                self._newEquation(sum, additionIndex)
            else:
                difference = float(terms[subtractionIndex]) - float(terms[subtractionIndex + 1])
                self._newEquation(difference, subtractionIndex)

    def getSolution(self) -> str:
        return self.terms[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(BackendClass('-8--5+5*5/-3'))

    """
    tests
    '-8+-5'
    '-8*-5'
    '-8*-5/5'
    '-8--5+5*5/-3'
    """