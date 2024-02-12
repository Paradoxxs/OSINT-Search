
from modules.phonenumber_lookup import pyPhonenumber
class Phone():

    def search(phoneNumber):
        return pyPhonenumber.query(phoneNumber)