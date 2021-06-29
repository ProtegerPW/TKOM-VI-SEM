import sys
import tokenTKOM
from lexer import Lexer
from tokenTKOM import Token
from parserTKOM import Parser
from filterTKOM import Filter

def runProgram (fileName): 
    
    parser = Parser(fileName)
    parser.parse_email()

    filter = Filter(parser.parsedEmail)
    filter.analizeEmail()

if __name__ == "__main__":
    runProgram(sys.argv[1])
