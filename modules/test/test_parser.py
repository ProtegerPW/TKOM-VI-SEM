import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(module_path)

from tokenTKOM import Token
from lexer import Lexer, KeyWords
from parserClasses import *
from parserTKOM import *

def test_parse_header():
    parser = Parser("./modules/test/parser/headers.txt")

    headersList = []

    for x in range(6):
        headersList.append(parser.parse_header())

    for testHeader in headersList:
        assert isinstance(testHeader, Header)

def test_parse_emailMessage():
    parser = Parser("./modules/test/parser/messages.txt")

    messagesList = []

    for x in range(7):
        messagesList.append(parser.parse_emailMessage())

    for testMessage in messagesList:
        assert isinstance(testMessage, EmailMessage)

def test_parse_attachment():
    parser = Parser("./modules/test/parser/attachments.txt")
    parsedAttachment = parser.parse_attachment()
    assert isinstance(parsedAttachment, Attachment)

    parser = Parser("./modules/test/parser/noattachments.txt")
    noAttachment = parser.parse_attachment()
    assert noAttachment is None

def test_parse_email():
    parser = Parser("./modules/test/parser/email.txt")

    parser.parse_email()
    assert isinstance(parser.parsedEmail, Email)
