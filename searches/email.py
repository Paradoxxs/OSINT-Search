from utils.helpers import splitEmail
from modules.email_lookup import EmailLookup
from modules.leak_lookup import LeakLookup
class Email():

    

    
    async def search(self,email):

        ##TODO implement email reputation lookup
        data = await EmailLookup().search(email)
        leak_data = await LeakLookup().search(email)

        if leak_data != None:
            data["leak"] = leak_data

        return data 

