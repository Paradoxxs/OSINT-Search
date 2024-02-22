import json
from utils.helpers import splitEmail
from modules.email_lookup import EmailLookup
class Email():

    

    
    async def search(self,email):

        ##TODO implement email reputation lookup
        ##TODO implement gravatar lookup
        data = await EmailLookup().search(email)
        return data 

