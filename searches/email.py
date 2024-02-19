import json
from utils.helpers import splitEmail
from modules.email_lookup import EmailLookup
class Email():

    

    
    async def search(self,email):

        data = await EmailLookup().search(email)
        return data 

