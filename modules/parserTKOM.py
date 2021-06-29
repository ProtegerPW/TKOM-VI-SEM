from lexer import Lexer
from parserClasses import *
from errors import ParserError

class Parser():
    def __init__(self, filePath):
        self.lexer = Lexer(filePath)
        self.parsedEmail = None

    def parse_email(self):
        parsedHeader = self.parse_header()
        parsedMessage = self.parse_emailMessage()
        parsedAttachment = self.parse_attachment()
        self.parsedEmail = Email(parsedHeader, parsedMessage, parsedAttachment)

    def parse_header(self):
        emailAddress = self.parse_emailAddress()
        emailDate = self.parse_date()
        emailSubject = self.parse_subject()
        return Header(emailAddress, emailDate, emailSubject)

    def parse_emailMessage(self):
        messageOpening = self.parse_openingPhrase()
        messageMainBlock = self.parse_mainBlock()
        messageFooter = self.parse_footer()
        return EmailMessage(messageOpening, messageMainBlock, messageFooter)

    def parse_attachment(self):
        attachmentsList = []

        while(self.lexer.getNextToken() != None):

            if(self.lexer.getToken().type == "FAKTURA_UC"):
                invoiceNum = self.parse_invoiceNum()
                fileFormat = self.parse_fileFormat()
                attachmentsList.append(FileName(invoiceNum, fileFormat))
                continue
            
            elif(self.lexer.getToken().type == "ZAMOWIENIE_UC"):
                orderNum = self.parse_orderNum()
                fileFormat = self.parse_fileFormat()
                attachmentsList.append(FileName(orderNum, fileFormat))
                continue

            elif(self.lexer.getToken().type == "FORMULARZ_UC"):
                formPhrase = self.parse_formPhrase()
                fileFormat = self.parse_fileFormat()
                attachmentsList.append(FileName(formPhrase, fileFormat))
                continue

            else:
                raise ParserError("Expected ATTACHMENT", self.lexer.getToken())


        if(len(attachmentsList) == 0):
            return None
        else:
            return Attachment(attachmentsList)


    def parse_fileFormat(self):
        if(self.lexer.getNextToken().type != "DOT"):
            raise ParserError("Expected DOT", self.lexer.getToken())

        if(self.lexer.getNextToken().type != "FILE_FORMAT"):
            raise ParserError("Expected FILE_FORMAT", self.lexer.getToken())

        return self.lexer.getToken()


    def parse_emailAddress(self):
        mailIdent = self.lexer.getNextToken()

        if(mailIdent.type != "IDENTIFIER"):
            raise ParserError("Expected IDENTIFIER", mailIdent)

        if(self.lexer.getNextToken().type != "AT_SIGN"):
            raise ParserError("Expected AT_SIGN", self.lexer.getToken())

        mailDomain = self.lexer.getNextToken()
        if(mailDomain.type != "MAIL_DOMAIN"):
            raise ParserError("Expected MAIL_DOMAIN", self.lexer.getToken())

        if(self.lexer.getNextToken().type != "DOT"):
            raise ParserError("Expected DOT", self.lexer.getToken())

        mailCountry = self.lexer.getNextToken()
        if(mailCountry.type != "COUNTRY_DOMAIN"):
            raise ParserError("Expected COUNTRY_DOMAIN", self.lexer.getToken())

        return EmailAddress(mailIdent, mailDomain, mailCountry)


    def parse_date(self):
        dateList = []
        for x in range(3):
            if(self.lexer.getNextToken().type != "TWO_DIGITS"):
                 raise ParserError("Expected TWO_DIGITS", self.lexer.getToken())

            dateList.append(self.lexer.getToken())

            if(self.lexer.getNextToken().type != "DOT"):
                raise ParserError("Expected DOT", self.lexer.getToken())

        if(self.lexer.getNextToken().type != "YEAR"):
            raise ParserError("Expected YEAR", self.lexer.getToken())

        return Date(dateList[0], dateList[1], dateList[2]) 
        

    def parse_subject(self):
        mainSubject = self.lexer.getNextToken()

        if(mainSubject.type == "FAKTURA_UC"):
            accountancyPhrase = self.parse_invoiceNum()
            return Subject(accountancyPhrase)

        elif(mainSubject.type == "ZAMOWIENIE_UC"):
            orderFormat = self.parse_orderNum()
            client = ClientPhrase(mainSubject.type, orderFormat)
            return Subject(client)
        
        elif(mainSubject.type == "REKLAMACJA_UC"):
            client = ClientPhrase(mainSubject.type)
            return Subject(client)


        elif(mainSubject.type == "DOSTAWA_UC" or mainSubject.type == "OPOZNIENIE_UC" or mainSubject.type == "MATERIAL_UC"):
            production = ProdPhrase(self.lexer.getToken())
            return Subject(production)

        else:
            raise ParserError("Expected SUBJECT", self.lexer.getToken())


    def parse_openingPhrase(self):
        opening = self.lexer.getNextToken()

        if(opening.type == "DZIEN_UC"):
            if(self.lexer.getNextToken().type == "DOBRY"):
                if(self.lexer.getNextToken().type == "COMMA"):
                    return OpenClosePhrase("Dzien dobry", "open")
                else:
                    raise ParserError("Expected COMMA", self.lexer.getToken())
            else:
                raise ParserError("Expected DOBRY", self.lexer.getToken())
        
        elif(opening.type == "SZANOWNI_UC"):
            if(self.lexer.getNextToken().type == "PANSTWO_UC"):
                if(self.lexer.getNextToken().type == "COMMA"):
                    return OpenClosePhrase("Szanowni Panstwo", "open")
                else:
                    raise ParserError("Expected COMMA", self.lexer.getToken())
            else:
                raise ParserError("Expected PANSTWO_UC", self.lexer.getToken())
        
        else:
            raise ParserError("Expected DZIEN_UC or SZANOWNI_UC ", self.lexer.getToken())

    def parse_mainBlock(self):
        token = self.lexer.getNextToken()
        
        if(token.type == "INTRO_ACC_CONTSR"):
            return MainBlock(self.parse_accConstr())
        
        elif(token.type == "INTRO_PRO_CONTSR"):
            return MainBlock(self.parse_proConstr())
        
        elif(token.type == "INTRO_CLI_CONTSR"):
            return MainBlock(self.parse_cliConstr())

        else:
            raise ParserError("Expected INTRO_ACC_CONTSR or INTRO_PRO_CONTSR or INTRO_CLI_CONTSR", self.lexer.getToken())
    
    def parse_accConstr(self):
        token = self.lexer.getNextToken()

        if(token.type == "WYKONAC"):
            if(self.lexer.getNextToken().type == "PRZELEW"):
                if(self.lexer.getNextToken().type == "BANK_ACCOUNT_NUM"):
                    return AccConstr("Przelew", self.lexer.getToken())
                else:
                    raise ParserError("Expected BANK_ACCOUNT_NUM", self.lexer.getToken())
            else:
                raise ParserError("Expected PRZELEW", self.lexer.getToken())

        elif(token.type == "ZAPLACIC"):
            if(self.lexer.getNextToken().type == "ZA"):
                if(self.lexer.getNextToken().type == "FAKTURE"):
                    return AccConstr("Zaplata", self.parse_invoiceNum())
                else:
                    raise ParserError("Expected FAKTURE", self.lexer.getToken())
            else:
                raise ParserError("Expected ZA", self.lexer.getToken())
        else:
            raise ParserError("Expected ACC_CONSTR", self.lexer.getToken())

    def parse_proConstr(self):

        if(self.lexer.getNextToken().type == "ZE"):
            token = self.lexer.getNextToken()

            if(token.type == "DOSTAWA"):
                if(self.lexer.getNextToken().type == "MATERIALU"):
                    if(self.lexer.getNextToken().type == "DOJDZIE"):
                        return ProConstr("Dostawa", self.parse_date())
                    else:
                        raise ParserError("Expected DOJDZIE", self.lexer.getToken())
                else:
                    raise ParserError("Expected MATERIALU", self.lexer.getToken())

            elif(token.type == "WYSTAPILO"):
                if(self.lexer.getNextToken().type == "OPOZNIENIE"):
                    return ProConstr("Opoznienie")
                else:
                    raise ParserError("Expected OPOZNIENIE", self.lexer.getToken())
            else:
                raise ParserError("Expected PRO_CONSTR", self.lexer.getToken())
        else:
            raise ParserError("Expected ZE", self.lexer.getToken())

    def parse_cliConstr(self):
        token = self.lexer.getNextToken()

        if(token.type == "CLI_VERB_BUY"):
            if(self.lexer.getNextToken().type == "TOWAR"):
                return CliConstrBuy("Zamowienie", self.parse_link())
            else:
                raise ParserError("Expected TOWAR", self.lexer.getToken())

        elif(token.type == "CLI_VERB_RET"):
            if(self.lexer.getNextToken().type == "TOWAR"):
                reason = self.parse_reasonForm()
                if(self.lexer.getNextToken().type == "DOT"):
                    bankNum = self.parse_returnMoney()
                    return CliConstrRet("Reklamacja", reason, bankNum)
                else:
                    self.lexer.getBackToken()
                    return CliConstrRet("Reklamacja", reason)
            else:
                raise ParserError("Expected TOWAR", self.lexer.getToken())
        else:
            raise ParserError("Expected ZAMOWIC or ZWROCIC", self.lexer.getToken())

    def parse_reasonForm(self):
        if(self.lexer.getNextToken().type == "Z"):
            if(self.lexer.getNextToken().type == "PRZYCZYNY"):
                if(self.lexer.getNextToken().type == "COLON"):
                    reason = self.lexer.getNextToken()

                    if(reason.type == "USTERKA"):
                        return self.lexer.getToken()
                    elif(reason.type == "USZKODZENIE"):
                        return self.lexer.getToken()
                    elif(reason.type == "ZGUBIENIE"):
                        return self.lexer.getToken()
                    else:
                        raise ParserError("Expected REASON", self.lexer.getToken())
                else:
                    raise ParserError("Expected COLON", self.lexer.getToken())
            else:
                raise ParserError("Expected PRZYCZYNY", self.lexer.getToken())
        else:
            raise ParserError("Expected Z", self.lexer.getToken())

    def parse_returnMoney(self):
        if(self.lexer.getNextToken().type == "PROSZE_UC"):
            if(self.lexer.getNextToken().type == "O"):
                if(self.lexer.getNextToken().type == "ZWROT"):
                    if(self.lexer.getNextToken().type == "PIENIEDZY"):
                        if(self.lexer.getNextToken().type == "BANK_ACCOUNT_NUM"):
                            return self.lexer.getToken()
                        else:
                            raise ParserError("Expected BANK_ACCOUNT_NUM", self.lexer.getToken())
                    else:
                        raise ParserError("Expected PIENIEDZY", self.lexer.getToken())
                else:
                    raise ParserError("Expected ZWROT", self.lexer.getToken())
            else:
                raise ParserError("Expected O", self.lexer.getToken())
        else:
            self.lexer.getBackToken()
            return None


    def parse_footer(self):
        token = self.lexer.getNextToken()

        if(token.type == "Z"):
            if(self.lexer.getNextToken().type == "POWAZANIEM"):
                return Footer(OpenClosePhrase("Z powazaniem", "close"), self.parse_signature())
            else:
                raise ParserError("Expected POWAZANIEM", self.lexer.getToken())
        
        elif(token.type == "POZDRAWIAM_UC"):
            return Footer(OpenClosePhrase("Pozdrawiam", "close"), self.parse_signature())
        
        else:
            raise ParserError("Expected CLOSING_PHRASE", self.lexer.getToken())

    def parse_signature(self):
        self.signatureList = []
        for x in range(2):
            if(self.lexer.getNextToken().type != "PERSONAL"):
                raise ParserError("Expected PERSONAL", self.lexer.getToken())
            self.signatureList.append(self.lexer.getToken())
        return Signature(self.signatureList[0], self.signatureList[1])


    def parse_invoiceNum(self):
            num2List = []

            for x in range(2):
                if(self.lexer.getNextToken().type != "TWO_DIGITS"):
                    raise ParserError("Expected TWO_DIGITS", self.lexer.getToken())
                
                num2List.append(self.lexer.getToken())

                if(self.lexer.getNextToken().type != "SLESH"):
                    raise ParserError("Expected SLESH", self.lexer.getToken())

            if(self.lexer.getNextToken().type != "FOUR_DIGITS"):
                raise ParserError("Expected FOUR_DIGITS", self.lexer.getToken())

            return InvoiceFormat(num2List[0], num2List[1], self.lexer.getToken())

    def parse_orderNum(self):
        alpha6List = []

        if(self.lexer.getNextToken().type != "SIX_ALPHA"):
            raise ParserError("Expected SIX_ALPHA", self.lexer.getToken())

        alpha6List.append(self.lexer.getToken())

        if(self.lexer.getNextToken().type != "DASH"):
            raise ParserError("Expected DASH", self.lexer.getToken())

        if(self.lexer.getNextToken().type != "SIX_ALPHA"):
            raise ParserError("Expected SIX_ALPHA", self.lexer.getToken())

        alpha6List.append(self.lexer.getToken())
        
        return OrderFormat(alpha6List[0], alpha6List[1])
    


    def parse_formPhrase(self):
        token = self.lexer.getNextToken()

        if(token.type == "REKLAMACJI"):
            return FormPhrase(self.lexer.getToken())

        elif(token.type == "PRZEKAZANIA"):
            if(self.lexer.getNextToken().type == "TOWARU"):
                return FormPhrase(token ,self.lexer.getToken())
            else:
                raise ParserError("Expected TOWARU", self.lexer.getToken())
        else:
            raise ParserError("Expected FORM_PHRASE", self.lexer.getToken())

    def parse_link(self):
        if(self.lexer.getNextToken().type == "WWW"):
            if(self.lexer.getNextToken().type == "DOT"):
                identifier = self.lexer.getNextToken()

                if(identifier.type == "IDENTIFIER"):
                    if(self.lexer.getNextToken().type == "DOT"):
                        if(self.lexer.getNextToken().type == "COUNTRY_DOMAIN"):
                            return Link(identifier, self.lexer.getToken())
                        else:
                            raise ParserError("Expected COUNTRY_DOMAIN", self.lexer.getToken())
                    else:
                        raise ParserError("Expected DOT", self.lexer.getToken())
                else:
                    raise ParserError("Expected IDENTIFIER", self.lexer.getToken())
            else:
                raise ParserError("Expected DOT", self.lexer.getToken())
        else:
            raise ParserError("Expected WWW", self.lexer.getToken())




    