import string
import sys
from tokenTKOM import Token

KeyWords = {
    "prosze":"INTRO_ACC_CONTSR",
    "informuje":"INTRO_PRO_CONTSR",
    "chcialbym":"INTRO_CLI_CONTSR",
    "zamowic":"CLI_VERB_BUY",
    "zwrocic":"CLI_VERB_RET",
    "material":"MATERIAL",
    "posiadamy":"POSIADAMY",
    "opoznienie":"OPOZNIENIE",
    "wystapilo":"WYSTAPILO",
    "dojdzie":"DOJDZIE",

    "materialu":"MATERIALU",
    "dostawa":"DOSTAWA",
    "Dostawa":"DOSTAWA_UC",
    "towar":"TOWAR",
    "Prosze":"PROSZE_UC",
    "zwrot":"ZWROT",
    "pieniedzy":"PIENIEDZY",
    "przyczyny":"PRZYCZYNY",
    "zgubienie":"ZGUBIENIE",
    "uszkodzenie":"USZKODZENIE",

    "usterka":"USTERKA",
    "podatki":"PODATKI",
    "oplacic":"OPLACIC",
    "naleznosc":"NALEZNOSC",
    "uregulowac":"UREGULOWAC",
    "zaplacic":"ZAPLACIC",
    "przelew":"PRZELEW",
    "wykonac":"WYKONAC",
    "Dzien":"DZIEN_UC",
    "dobry":"DOBRY",

    "Szanowni":"SZANOWNI_UC",
    "Panstwo":"PANSTWO_UC",
    "powazaniem":"POWAZANIEM",
    "Pozdrawiam":"POZDRAWIAM_UC",
    "Zamowienie":"ZAMOWIENIE_UC",
    "Pytanie":"PYTANIE_UC",
    "Reklamacja":"REKLAMACJA_UC",
    "Opoznienie":"OPOZNIENIE_UC",
    "Material":"MATERIAL_UC",
    "reklamacji":"REKLAMACJI",
    "przekazania":"PRZEKAZANIA",
    "towaru":"TOWARU",
    "Formularz":"FORMULARZ_UC",
    "faktura":"FAKTURA",
    "Faktura":"FAKTURA_UC",
    "fakture":"FAKTURE",

    "gmail":"MAIL_DOMAIN",
    "o2":"MAIL_DOMAIN",
    "wp":"MAIL_DOMAIN",
    "onet":"MAIL_DOMAIN",
    "www":"WWW",
    "pl":"COUNTRY_DOMAIN",
    "de":"COUNTRY_DOMAIN",
    "ru":"COUNTRY_DOMAIN",
    "uk":"COUNTRY_DOMAIN",

    "pdf":"FILE_FORMAT",
    "docx":"FILE_FORMAT",
    "o":"O",
    "z":"Z",
    "Z":"Z",
    "za":"ZA",
    "ze":"ZE",
    "r":"YEAR",
    ":":"COLON",
    "/":"SLESH",
    "-":"DASH",
    ",":"COMMA",
    ".":"DOT",
    "@":"AT_SIGN",
    "EOF":"EOF"
}

class Source:
    def __init__(self, fileName):
        self.file = open(fileName, "rb")
        self.current_char = None
        self.line = 1
        self.column = 0

    def moveToNextChar(self):
        self.current_char = self.file.read(1)
        
        if(self.current_char.decode("utf-8") == ""):
            self.current_char = KeyWords.get("EOF")
            return

        self.column += 1

        if self.current_char.decode("utf-8") == "\r" or self.current_char.decode("utf-8") == "\t":
            self.current_char = self.file.read(1)            

    def undoChar(self):
        self.file.seek(-1, 1)
        self.column -= 1

    def setToNextLine(self):
        self.column = 0
        self.line += 1

class Lexer(Source):
    def __init__(self, fileName):
        self.tokenList = []
        self.elementsOfToken = []
        self.currentToken = -1
        super().__init__(fileName)

        while(self.current_char != "EOF"):
            self.analizeNextChar()

    def analizeNextChar(self):
        self.moveToNextChar()

        if self.current_char == "EOF":
            if(len(self.elementsOfToken) > 0):
                self.buildToken()
                self.undoChar()
            return

        charToAnalize = self.current_char.decode("utf-8")
        
        if charToAnalize.isalnum():
            self.elementsOfToken.append(charToAnalize)
            return
        
                        
        if charToAnalize == " " or charToAnalize == "\n":
            if(len(self.elementsOfToken) > 0):
                self.undoChar()
                self.buildToken()
            else:
                if(charToAnalize == "\n"):
                    self.setToNextLine()
            return

        if (len(self.elementsOfToken) > 0):
            self.undoChar()
            self.buildToken()
        else:
            self.elementsOfToken = charToAnalize
            self.buildToken()

    def buildToken(self, elementsToBuild = None):
        if(elementsToBuild is None):
            self.elementsOfToken = "".join(self.elementsOfToken)

        length = len(self.elementsOfToken)
        if(self.elementsOfToken.isdigit()):

            if(length == 2):
                self.createToken("TWO_DIGITS")
                return

            if(length == 4):
                self.createToken("FOUR_DIGITS")
                return

            if(length == 26):
                self.createToken("BANK_ACCOUNT_NUM")
                return

        checkDict = KeyWords.get(self.elementsOfToken, "Error")
        if(checkDict != "Error"):
            self.createToken(checkDict)
        else:

            if(self.elementsOfToken[0].isupper() and self.elementsOfToken[1:].islower() and self.elementsOfToken.isalpha()):
                self.createToken("PERSONAL")
                return 

            if(self.elementsOfToken[0].isdigit() and length == 6):
                self.createToken("SIX_ALPHA")
                return

            if(self.elementsOfToken[0].islower() and self.elementsOfToken[0].isalpha()):
                self.createToken("IDENTIFIER")
                return

            self.createToken("ERROR")
            

    def createToken(self, passType = None):
        if(passType is None):
            newType = self.elementsOfToken
        else:
            newType = passType

        newValue = self.elementsOfToken
        newPosition = (self.line, self.column)
        newToken = Token(newType, newValue, newPosition)
        self.tokenList.append(newToken)
        self.elementsOfToken = []

    def getNextToken(self):
        self.currentToken += 1
        if(self.currentToken < len(self.tokenList)):
            return self.tokenList[self.currentToken]
        else:
            return None

    def getToken(self):
        return self.tokenList[self.currentToken]

    def getBackToken(self):
        self.currentToken -= 1



        

            

    