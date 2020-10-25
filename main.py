# This project created by Enadream, enadream.com

class BasicOperations:
    def _addition(self, num1, num2):  # protected
        result = "error"
        try:
            result = str(float(num1) + float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    def _subtraction(self, num1, num2):
        result = "error"
        try:
            result = str(float(num1) - float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    def _multiplication(self, num1, num2):
        result = "error"
        try:
            result = str(float(num1) * float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    def _division(self, num1, num2):
        result = "error"
        try:
            result = str(float(num1) / float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    def _exponential(self, num1, num2):
        result = "error"
        try:
            result = str(float(num1) ** float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    def _modulus(self, num1, num2):
        result = "error"
        try:
            result = str(float(num1) % float(num2))
        except TypeError:
            Console.PrintError(2)
        return result

    @staticmethod
    def find_all(a_str, sub_str):  # Find all substring position
        start = 0
        subList = []
        while start < len(a_str):
            start = a_str.find(sub_str, start)
            if start == -1:
                return
            subList.append(start)
            start += len(sub_str)  # use start += 1 to find overlapping matches
        return subList


class Console:
    errorStatus = False

    @staticmethod
    def PrintError(errorCode, add_txt=""):
        Console.errorStatus = True
        print("[ERROR]: ", end="")

        if errorCode == 0:
            print("The string contains undefined characters")
        elif errorCode == 1:
            print("The string syntax is wrong")
        elif errorCode == 2:
            print("The string contains inconvenient operation order")
        elif errorCode == 3:
            pass

    @staticmethod
    def PrintWarning(warningCode, add_text=""):
        print("[Warning]: ", end="")
        if warningCode == 0:
            print("Unknown letter found in the string")
        elif warningCode == 1:
            print("You made a parentheses mistake please fix it")
        elif warningCode == 2:
            pass
        elif warningCode == 3:
            pass


class Calculator(BasicOperations):
    def __init__(self):  # default constructor
        self.MainStr = ""
        self.Result = 0.0

    def GetString(self):
        Console.errorStatus = False
        print("\nEnter the operation you want to calculate: ")
        self.MainStr = str(input())
        self.__checkString(self.MainStr)

    # Editing string and checking
    def __checkString(self, mainStr):  # private
        ALLOWEDCHARS = "0123456789.*/+-^%()[]"
        # ALLOWEDNAMES = ("sin", "cos", "tan", "cot") if the trigonometric operator allowed

        # Remove the spaces and make lower
        mainStr = mainStr.replace(" ", "")
        mainStr = mainStr.lower()

        # Check String
        tempStr = mainStr

        # for names in ALLOWEDNAMES: tempStr = tempStr.replace(names, "")
        for char in tempStr:
            if not (char in ALLOWEDCHARS):
                Console.PrintError(0)
                self.GetString()
                return 0

        self.__mainSplitter(mainStr)

    # Parentheses Splitter
    def __mainSplitter(self, fullString):
        indexOfPar = []  # This is for to save of the indexes of initial parentheses
        tempStr = ""
        stepNum = 1
        i = 0
        while i < len(fullString):  # Remove all parentheses
            if fullString[i] == "(":
                indexOfPar.append(i)
                i += 1
            elif fullString[i] == ")":
                if len(indexOfPar) > 0:
                    self.__printString(fullString, stepNum)
                    stepNum += 1
                    tempStr = fullString[(indexOfPar[-1] + 1):i]
                    tempStr = self.__calculator(tempStr)
                    fullString = fullString[0:indexOfPar[-1]] + tempStr + fullString[i + 1:]
                    i = indexOfPar[-1]
                    indexOfPar.pop(-1)
                else:
                    Console.PrintWarning(1)
                    break
            else:
                i += 1

        if len(indexOfPar) == 0:  # check the list to be sure about that parentheses list is empty
            self.__printString(fullString, stepNum)
            self.Result = self.__calculator(fullString)
        else:
            Console.PrintWarning(1)
        if not Console.errorStatus:
            print("\n[RESULT] : " + str(self.Result))
        else:
            print("\n[RESULT] : error")
            Console.errorStatus = False

    # Finding operations and numbers in the string
    def __extraction(self, subString):
        i = 0
        tempList = []
        numbers = []
        operators = []
        tempNum = ""
        DIGITS = "0123456789."
        OPERATIONS = "*/+-^%"

        while i < len(subString):
            if subString[i] in DIGITS:
                tempNum += subString[i]
            elif subString[i] in OPERATIONS:
                if tempNum != "":  # Check the tempNum for empty then add it to numbers list
                    tempList.append(tempNum)
                    numbers.append(tempNum)
                    tempNum = ""
                if subString[i] in "+-":  # Is the symbol sign or operation ?
                    if len(tempList) > 0:
                        if tempList[-1] in OPERATIONS:  # Is the last item an Operation ?
                            tempNum += subString[i]
                        else:
                            tempList.append(subString[i])
                            operators.append(subString[i])
                    else:
                        tempNum += subString[i]
                else:
                    tempList.append(subString[i])
                    operators.append(subString[i])
            elif subString[i] == "e":  # When the number is scientific
                tempNum += subString[i] + subString[i + 1]
                i += 1
            else:  # When the char is neither Digits nor operations
                Console.PrintError(0)
            i += 1
        else:  # The last number has to be still in the tempNum
            tempList.append(tempNum)
            numbers.append(tempNum)
            tempStr = ""
        return numbers, operators

    # Calculating math operations
    def __calculator(self, subString):
        i = 0
        numbers, operators = self.__extraction(subString)
        self.__printSteps(numbers, operators)
        isFirst, isSecond, isThird = False, False, False

        # Calculating exponential and modulus operations [first part]
        while i < len(operators):
            if operators[i] == "^":
                numbers[i] = self._exponential(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isFirst = True
            elif operators[i] == "%":
                numbers[i] = self._modulus(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isFirst = True
            else:
                i += 1
        i = 0
        if isFirst:
            self.__printSteps(numbers, operators)

        # Calculating multiplication and division operations [second part]
        while i < len(operators):
            if operators[i] == "*":
                numbers[i] = self._multiplication(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isSecond = True
            elif operators[i] == "/":
                numbers[i] = self._division(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isSecond = True
            else:
                i += 1
        i = 0
        if isSecond:
            self.__printSteps(numbers, operators)

        # Calculating addition and subtraction operations [third part]
        while i < len(operators):
            if operators[i] == "+":
                numbers[i] = self._addition(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isThird = True
            elif operators[i] == "-":
                numbers[i] = self._subtraction(numbers[i], numbers[i + 1])
                if numbers[i] == "error":
                    break
                operators.pop(i)
                numbers.pop(i + 1)
                isThird = True
            else:
                i += 1
        if isThird:
            self.__printSteps(numbers, operators)

        return numbers[0]

    # Printing calculation steps
    def __printSteps(self, numbers, operators):
        print("==>", end="")
        for index, num in enumerate(numbers):
            print(" " + num, end="")
            if int(index) < len(operators):
                print(" " + operators[int(index)], end="")
        print("\n", end="")

    # Printing current string
    def __printString(self, string, stepNo):
        DIGITS = "0123456789.()"
        OPERATIONS = "*/+-^%"
        tempStr = ""

        i = 0
        while i < len(string):
            if string[i] in DIGITS:
                tempStr += string[i]
            elif string[i] in OPERATIONS:
                if i == 0:
                    tempStr += string[i] + " "
                elif tempStr[-1] == " ":  # check for the last char was operations
                    tempStr += string[i]
                elif tempStr[-1] == "(":  # check for the last char was parentheses
                    tempStr += string[i]
                else:
                    tempStr += " " + string[i] + " "
            elif string[i] == "e":
                tempStr += string[i] + string[i + 1]
                i += 1
            else:
                Console.PrintWarning(0)
            i += 1
        print("\n[STEP " + str(stepNo) + "]")
        print("[CURRENT STRING] : " + tempStr)


print("\n________ WELCOME TO THE ADVANCED CALCULATOR ________")
print("------------------------------------------------")
print("This calculator can handle difficult algebraic equations. You are able")
print("to use those operators; '*' for multiply, '/' for divide, '+' for sum,")
print("'-' for subtraction, '%' for mod, '^' for exponential. Also you are able")
print("to use parentheses to explain your calculation well. And the spaces in")
print("the string are not important.")
print("Ex. string : (((5+6)*45)^3/77 + 17 - (4.5 * -4)+ 174) / (5^4 % 7)")
print("------------------------------------------------")

newCalc = Calculator()

while True:
    newCalc.GetString()
    print("__________________________________________________")
    print("\nDo you want to do a new calculation ? (\"y\":yes, \"n\":no) : ", end="")
    cont = str(input())
    if cont == "y" or cont == "Y" or cont == "yes":
        pass
    else:
        break
