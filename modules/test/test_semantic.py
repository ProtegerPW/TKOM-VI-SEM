import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(module_path)

from filterTKOM import *
from tokenTKOM import Token
from lexer import Lexer, KeyWords
from parserClasses import *
from parserTKOM import *

def test_filter_mix():
    
    fileName = "mix"

    for index in range(2):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.CUSTOMER_SERVICE and filter.emailType != EmailType.ACCOUNTANCY
        assert filter.reliability == 0

def test_filter_accountancy():

    fileName = "accountancy"

    for index in range(2):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.CUSTOMER_SERVICE and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability == 1


def test_filter_accountancy_false():

    fileName = "f_accountancy"

    for index in range(4):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.CUSTOMER_SERVICE and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability < 1.0 and filter.reliability > 0


def test_filter_order_false():
    fileName = "f_order"

    for index in range(1):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.ACCOUNTANCY and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability < 1

def test_filter_order():
    fileName = "order"

    for index in range(1):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.ACCOUNTANCY and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability == 1

def test_filter_return():
    fileName = "return"

    for index in range(1):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.PRODUCTION and filter.emailType != EmailType.ACCOUNTANCY and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability == 1

def test_filter_production():
    fileName = "production"

    for index in range(3):
        parser = Parser("./modules/test/semantic/" + fileName + str(index) + ".txt")
        parser.parse_email()
        
        filter = Filter(parser.parsedEmail)
        filter.analizeEmail()

        assert filter.emailType != EmailType.CUSTOMER_SERVICE and filter.emailType != EmailType.ACCOUNTANCY and filter.emailType != EmailType.UNDEFINED
        assert filter.reliability == 1