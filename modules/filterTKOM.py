from enum import Enum, auto
from parserClasses import *
from collections import Counter

class EmailType(Enum):
    ACCOUNTANCY = auto()
    PRODUCTION = auto()
    CUSTOMER_SERVICE = auto()
    UNDEFINED = auto()


class Filter():
    def __init__(self, emailModel):
        self.emailModel = emailModel
        self.emailPartsType = []
        self.emailType = None
        self.reliability = 0
        self.attachmentNum = 0;

    def analizeEmail(self):
        self.checkHeader()
        self.checkEmailMessage()
        if(self.emailModel.attachment is not None):
            for x in range(len(self.emailModel.attachment.attachments)):
                self.checkAttachment(x)
                self.attachmentNum += 1
        self.sortEmail()
        print(self.getEmailType())

    def checkHeader(self):
        if(self.checkIfInstance(self.emailModel.header.subject.phrase, InvoiceFormat, EmailType.ACCOUNTANCY)):
            self.emailPartsType.append(self.emailModel.header.subject.phrase)
            return
        elif(self.checkIfInstance(self.emailModel.header.subject.phrase, ClientPhrase, EmailType.CUSTOMER_SERVICE)):
            self.emailPartsType.append(self.emailModel.header.subject.phrase.orderNum)
            return
        elif(self.checkIfInstance(self.emailModel.header.subject.phrase, ProdPhrase, EmailType.PRODUCTION)):
            self.emailPartsType.append(None)
            return
        else:
            self.emailPartsType.append(EmailType.UNDEFINED)  


    def checkEmailMessage(self):
        if(self.checkIfInstance(self.emailModel.emailMessage.mainBlock.construction, AccConstr, EmailType.ACCOUNTANCY)):
            self.emailPartsType.append(self.emailModel.emailMessage.mainBlock.construction.impNum)
            return
        elif(self.checkIfInstance(self.emailModel.emailMessage.mainBlock.construction, ProConstr, EmailType.PRODUCTION)):
            self.emailPartsType.append(None)
            return
        elif(self.checkIfInstance(self.emailModel.emailMessage.mainBlock.construction, CliConstrBuy, EmailType.CUSTOMER_SERVICE)):
            self.emailPartsType.append(self.emailModel.emailMessage.mainBlock.construction)
            return
        elif(self.checkIfInstance(self.emailModel.emailMessage.mainBlock.construction, CliConstrRet, EmailType.CUSTOMER_SERVICE)):
            self.emailPartsType.append(self.emailModel.emailMessage.mainBlock.construction.type)
            return
        else:
            self.emailPartsType.append(EmailType.UNDEFINED)


    def checkAttachment(self, index):
        if(self.checkIfInstance(self.emailModel.attachment.attachments[index].prefix, InvoiceFormat, EmailType.ACCOUNTANCY)):
            self.emailPartsType.append(self.emailModel.attachment.attachments[index].prefix)
            return
        elif(self.checkIfInstance(self.emailModel.attachment.attachments[index].prefix, OrderFormat, EmailType.CUSTOMER_SERVICE)):
            self.emailPartsType.append(self.emailModel.attachment.attachments[index].prefix)
            return
        elif(self.checkIfInstance(self.emailModel.attachment.attachments[index].prefix, FormPhrase, EmailType.CUSTOMER_SERVICE)):
            self.emailPartsType.append(self.emailModel.attachment.attachments[index].prefix)
            return
        else:
            self.emailPartsType.append(EmailType.UNDEFINED)

    def checkIfInstance(self, checkingObject, classObject, addType):
        if(isinstance(checkingObject, classObject)):
            self.emailPartsType.append(addType)
            return True
        else:
            return False

    def sortEmail(self):
        tempFormatList = []

        for index, part in enumerate(self.emailPartsType):
            if index % 2 == 0:
                if part is not self.emailPartsType[0]:
                    self.reliability = 0.0
                    self.emailType = EmailType.UNDEFINED
                    print("Semantic error\nOccured at " + str(int(index/2 + 1)) + " type")
                    return
            else:
                if(self.emailPartsType[index-1] == EmailType.ACCOUNTANCY):
                    if(isinstance(self.emailPartsType[index], InvoiceFormat)):
                        tempFormatList.append((self.emailPartsType[index].day.value, 
                                                self.emailPartsType[index].month.value, 
                                                self.emailPartsType[index].year.value))
                    else:
                        tempFormatList.append((self.emailPartsType[index-2].day.value, 
                                                self.emailPartsType[index-2].month.value, 
                                                self.emailPartsType[index-2].year.value))

                elif(self.emailPartsType[index-1] == EmailType.CUSTOMER_SERVICE):
                    if(isinstance(self.emailPartsType[index], OrderFormat)):
                        tempFormatList.append((self.emailPartsType[index].firstSeq.value,
                                                self.emailPartsType[index].secondSeq.value))

                    elif(isinstance(self.emailPartsType[index], CliConstrBuy)):
                        tempFormatList.append((self.emailPartsType[index-2].firstSeq.value,
                                                self.emailPartsType[index-2].secondSeq.value))
                    
                    else:
                        tempFormatList.append("reklamacja")
            
        # print(tempFormatList)

        if(len(tempFormatList) == 0):
            self.reliability = 1;
            self.emailType = EmailType.PRODUCTION
            return
            
        countFormatList = Counter(tempFormatList)

        for k, v in countFormatList.items():
            if(self.emailPartsType[0] == EmailType.ACCOUNTANCY):
                self.reliability = v / (2 + self.attachmentNum)
                self.emailType = EmailType.ACCOUNTANCY
                return
            elif(self.emailPartsType[0] == EmailType.CUSTOMER_SERVICE):

                self.reliability = v / (2 + self.attachmentNum)
                self.emailType = EmailType.CUSTOMER_SERVICE
                return
        
    def getEmailType(self) -> str:
        return "Email type is {emailType} with reliability {reliability}% ".format(
            emailType = self.emailType.name,
            reliability = round(self.reliability * 100, 2)
        )
