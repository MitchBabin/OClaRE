#########################################
#               Imports                 #
#########################################
import re

#########################################
#    Replace Math ( With [MATH])        #
#########################################
def _ReplaceMath(text: str):
    mathSignRegex = "\-|(?<=[^a-zA-Z])(−)(?=[^a-zA-Z])|\+|\*|\/|(?<=[^a-zA-Z])(x)(?=[^a-zA-Z])|(?<=[^a-zA-Z])(×)(?=[^a-zA-Z])|(?<=[^a-zA-Z])(X)(?=[^a-zA-Z])|\^"
    mathDecRegex = "\d+\.+\d+"
    mathNumber = "\d+"
    mathParentheses = "(\(( |\d+| \(\d+).*\))"
    #reg = "[\+\-]?(\w+(\^?\d?))+([\+\-\/\*]*(\w?\^?\d?))*"
    temp = re.sub(mathParentheses, '[MATH]', text)
    temp = re.sub(mathSignRegex,'[MATH]',temp)
    temp = re.sub(mathDecRegex, '[MATH]', temp)
    mathFreeText = re.sub(mathNumber, '[MATH]', temp)
    return mathFreeText

#########################################
#      Remove Commas From Numbers       #
#########################################

def _StripCommasFromNumbers(text: str):
    regex = "(?<=\d)(,)(?=\d)"
    commaFree = re.sub(regex, '', text)
    return commaFree

#########################################
#           Remove Extra(s)             #
#########################################
def _StripExtras(text: str):
    regex = "\f"
    temp = re.sub(regex,'',text)
    return temp

#########################################
#      Return Character Replacements    #
#########################################
def _ReplaceReturns(text: str) -> str:
    """Replaces newlines with space after replacing double new lines with ."""

    text = re.sub("(\n\n)|(\r\r)|(\r\n\r\n)", ". ", text)
    text = re.sub("\n", " ", text)

    return text

#print(_ReplaceMath("The area of the first square is given by (a+b)^2 or 4(1/2ab)+ a^2 + b^2. \nThe area of the second square is given by (a+b)^2 or 4(1/2ab) + c^2. \nSince the squares have equal areas we can set them equal to another and subtract equals. \nThe case (a+b)^2=(a+b)^2 is not interesting. \nLet's do the other case.4(1/2ab) + a^2 + b^2 = 4(1/2ab)+ c^2 Subtracting equals from both sides we have"))
#mytext = StripCommasFromNumbers("test , n1, n2  x^3-x^2+x \n-6x^2+6x+5 \n 5+5+x \n x+b-y \n -3X^5 \n (a+b) \ntresfgytres  2000,0000,000 ttxxxxyyXXXxxert, hey")

def LaunchKandy(text:str) -> str:
    """Launcher function to perform all of Kandy's strips"""

    text = _StripExtras(text)
    text = _StripCommasFromNumbers(text)
    text = _ReplaceMath(text)
    text = _ReplaceReturns(text)

    return text