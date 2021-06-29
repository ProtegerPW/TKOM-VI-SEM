

class Email:
    def __init__(self, header, message, attachment) -> None:
        self.header = header
        self.emailMessage = message
        self.attachment = attachment

    def __str__(self) -> str:
        return "Classtype EMAIL \n\n{header} \n\n{emailMessage} \n\n{attachment}".format(
            header = repr(self.header),
            emailMessage = repr(self.emailMessage),
            attachment = repr(self.attachment)
        )

    def __repr__(self):
        return self.__str__()


class Header:
    def __init__(self, emailAddress, date, subject) -> None:
        self.emailAddress = emailAddress
        self.date = date
        self.subject = subject

    def __str__(self) -> str:
        return "Classtype HEADER \n{emailAddress} \n{date} \n{subject}".format(
            emailAddress = repr(self.emailAddress),
            date = repr(self.date),
            subject = repr(self.subject)
        )

    def __repr__(self):
        return self.__str__()

class EmailMessage:
    def __init__(self, openingPhrase, mainBlock, footer) -> None:
        self.openingPhrase = openingPhrase
        self.mainBlock = mainBlock
        self.footer = footer

    def __str__(self) -> str:
        return "Classtype EMAIL_MESSAGE \n{openingPhrase} \n{mainBlock} \n{footer}".format(
            openingPhrase = repr(self.openingPhrase),
            mainBlock = repr(self.mainBlock),
            footer = repr(self.footer)
        )

    def __repr__(self):
        return self.__str__()

class MainBlock:
    def __init__(self, construction) -> None:
        self.construction = construction

    def __str__(self) -> str:
        return "Classtype MAIN_BLOCK {construction}".format(
            construction=self.construction
        )

    def __repr__(self) -> str:
        return self.__str__()

class Attachment:
    def __init__(self, attachments) -> None:
        self.attachments = attachments


    def __str__(self) -> str:
        return "Classtype ATTACHMENT {attachments}".format(
            attachments = self.attachments
        )

    def __repr__(self) -> str:
        return self.__str__()


class FileName:
    def __init__(self, prefix, fileFormat) -> None:
        self.prefix = prefix
        self.fileFormat = fileFormat

    def __str__(self) -> str:
        return "Classtype FILE_NAME {prefix}.{fileFormat}".format(
            prefix = repr(self.prefix),
            fileFormat = self.fileFormat.value
        )

    def __repr__(self) -> str:
        return self.__str__()


class EmailAddress:
    def __init__(self, identfierArg, mailDomainArg, countryDomainArg) -> None:
        self.identfier = identfierArg
        self.mailDomain = mailDomainArg
        self.countryDomainArg = countryDomainArg

    def __str__(self) -> str:
        return "Classtype EMAIL_ADDRESS {identfier}@{mailDomain}.{countryDomainArg}".format(
            identfier = self.identfier.value,
            mailDomain = self.mailDomain. value,
            countryDomainArg = self.countryDomainArg.value
        )

    def __repr__(self):
        return self.__str__()

class Date:
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year
    
    def __str__(self) -> str:
        return "Classtype DATE {day}.{month}.{year}.r".format(
            day = self.day.value,
            month = self.month.value,
            year = self.year.value
        )

    def __repr__(self):
        return self.__str__()

class Subject:
    def __init__(self, phrase) -> None:
        self.phrase = phrase
    
    def __str__(self) -> str:
        return "Classtype SUBJECT {phrase}".format(
            phrase = repr(self.phrase)
        )

    def __repr__(self):
        return self.__str__()


class InvoiceFormat:
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year

    def __str__(self) -> str:
        return "Classtype INVOICE_FORMAT {day}/{month}/{year}".format(
            day = self.day.value,
            month = self.month.value,
            year = self.year.value
        )

    def __repr__(self):
        return self.__str__()

# class AccountantPhrase:
#     def __init__(self, invoiceFormat) -> None:
#         self.invoiceFormat = invoiceFormat

#     def __str__(self):
#         return "Classtype ACC_PHRASE {invoiceForm}".format(
#             invoiceForm = repr(self.invoiceFormat)
#         )

class ClientPhrase:
    def __init__(self, cliPhrase, orderNum = None) -> None:
            self.type = cliPhrase
            self.orderNum = orderNum

    def __str__(self) -> str:
        if(self.orderNum is not None):
            return "Classtype CLIENT_PHRASE {type} {orderNum}".format(
                type = self.type,
                orderNum = repr(self.orderNum)
            )
        else:
            return "Classtype CLIENT_PHRASE {type}".format(
                type = self.type
            )

    def __repr__(self):
        return self.__str__()


class OrderFormat:
    def __init__(self, firstSeq, secondSeq) -> None:
        self.firstSeq = firstSeq
        self.secondSeq = secondSeq

    def __str__(self) -> str:
        return "Classtype ORDER_FORMAT {firstSeq}-{secondSeq}".format(
            firstSeq = self.firstSeq.value,
            secondSeq = self.secondSeq.value,
        )

    def __repr__(self):
        return self.__str__()

class ProdPhrase:
    def __init__(self, prodPhrase) -> None:
            self.type = prodPhrase

    def __str__(self) -> str:
            return "Classtype PRODUCTION_PHRASE {type}".format(
                type = self.type.value,
            )

    def __repr__(self):
        return self.__str__()

class FormPhrase:
    def __init__(self, *args) -> None:
        self.phrases = []
        for word in args:
            self.phrases.append(word)

    def __str__(self) -> str:
        if(len(self.phrases) < 2):
            return "Classtype FORM_PHRASE {phrase}".format(
                phrase = self.phrases[0].value
            )
        else:
            return "Classtype FORM_PHRASE {phrase} {phrase2}".format(
                phrase = self.phrases[0].value,
                phrase2 = self.phrases[1].value
            )

    def __repr__(self) -> str:
        return self.__str__()

class OpenClosePhrase:
    def __init__(self, phrase, type) -> None:
        self.phrase = phrase
        self.type = type

    def __str__(self) -> str:
        if(self.type == "open"):
            return "Classtype OPENING_PHRASE {phrase}".format(
                phrase = self.phrase
            )
        else:
            return "Classtype CLOSING_PHRASE {phrase}".format(
                phrase = self.phrase
            )

    def __repr__(self) -> str:
        return self.__str__()

class Signature:
    def __init__(self, name, surname) -> None:
        self.name = name
        self.surname = surname

    def __str__(self) -> str:
        return "Classtype SIGNATURE {name} {surname}".format(
            name = self.name.value,
            surname = self.surname.value
        )

    def __repr__(self) -> str:
        return self.__str__()

class Footer:
    def __init__(self, closingPhrase, signature) -> None:
        self.closingPhrase = closingPhrase
        self.signature = signature

    def __str__(self) -> str:
        return "Classtype FOOTER {closingPhrase} {signature}".format(
            closingPhrase= repr(self.closingPhrase),
            signature= repr(self.signature)
        )
    def __repr__(self) -> str:
        return self.__str__()

class AccConstr:
    def __init__(self, type, impNum) -> None:
        self.type = type
        self.impNum = impNum

    def __str__(self) -> str:
        return "Classtype ACC_CONSTR {type} {impNum}".format(
            type = self.type,
            impNum = self.impNum
        )

    def __repr__(self) -> str:
        return self.__str__()

class ProConstr:
    def __init__(self, type, date = None) -> None:
        self.type = type
        self.date = date

    def __str__(self) -> str:
        if(self.date):
            return "Classtype PRO_CONSTR {type} {date}".format(
                type = self.type,
                date = self.date.value
            )
        else:
            return "Classtype PRO_CONSTR {type}".format(
                type = self.type,
            )

    def __repr__(self) -> str:
        return self.__str__()

class CliConstrBuy:
    def __init__(self, type, link) -> None:
        self.type = type
        self.link = link

    def __str__(self) -> str:
        return "Classtype CLI_CONSTR_BUY {type} {link}".format(
            type = self.type,
            link = self.link
        )

    def __repr__(self) -> str:
        return self.__str__()

class CliConstrRet:
    def __init__(self, type, reason, bankAccount = None) -> None:
        self.type = type
        self.reason = reason
        self.bankAccount = bankAccount

    def __str__(self) -> str:
        if(self.bankAccount):
            return "Classtype CLI_CONSTR_RET {type} {reason} nr. konta {bankAccount}".format(
                type = self.type,
                reason = self.reason.value,
                bankAccount = self.bankAccount.value
            )
        else:
            return "Classtype CLI_CONSTR_RET {type} {reason}".format(
                type = self.type,
                reason = self.reason.value,
            )


    def __repr__(self) -> str:
        return self.__str__()
    

class Link:
    def __init__(self, identifier, countryDomain) -> None:
        self.identifier = identifier
        self.countryDomain = countryDomain

    def __str__(self) -> str:
        return "Classtype LINK www.{identifier}.{countryDomain}".format(
            identifier = self.identifier.value,
            countryDomain = self.countryDomain.value
        )

    def __repr__(self) -> str:
        return self.__str__()