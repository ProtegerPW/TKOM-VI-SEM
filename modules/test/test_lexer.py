import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(module_path)

# from lexer import Lexer
from tokenTKOM import Token
from lexer import Lexer, KeyWords

def test_all_tokens():

    tokens = [ 
        Token("TWO_DIGITS"),
        Token("FOUR_DIGITS"),
        Token("BANK_ACCOUNT_NUM"),
        Token("PERSONAL"),
        Token("SIX_ALPHA"),
        Token("IDENTIFIER")
    ] + [
        Token(t) for t in KeyWords.values()
    ] 

    lexer = Lexer("./modules/test/lexer/all_tokens.txt")

    while(lexer.current_char != "EOF"):
        lexer.AnalizeNextChar()

    for exp_token, lex_token in zip(tokens, lexer.tokenList):
        assert exp_token.type == lex_token.type
        

def test_random_chars():
    lexer = Lexer("./modules/test/lexer/random_tokens.txt")

    smallDict = [
        "TWO_DIGITS",
        "FOUR_DIGITS",
        "BANK_ACCOUNT_NUM",
        "PERSONAL",
        "SIX_ALPHA",
        "IDENTIFIER"
    ]

    while(lexer.current_char != "EOF"):
        lexer.AnalizeNextChar()

    for lex_token in lexer.tokenList:
        if lex_token.type in smallDict:
            assert True
        else:
            assert False

def test_error_chars():
    lexer = Lexer("./modules/test/lexer/error_tokens.txt")

    while(lexer.current_char != "EOF"):
        lexer.AnalizeNextChar()

    for lex_token in lexer.tokenList:
        print(lex_token)
        assert lex_token.type == "ERROR"



