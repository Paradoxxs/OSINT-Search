import httpx
import trio
from collections import namedtuple
from holehe import core
import os
import sys
import requests
from utils.helpers import get_env_var
from pprint import pprint
from ghunt.apis.peoplepa import PeoplePaHttp
from ghunt.objects.base import GHuntCreds







# path to the main folder of the project
PROJECT_HOME = get_env_var("project_dir")

# paths to the different projects
POASTAL_PATHS = ["poastal_github",  "poastal_github/backend/modules"]
PROJECT_PATHS =  POASTAL_PATHS

# add different projects to sys.path
# this is required for the different projects to run without modification
for p in PROJECT_PATHS:
    try:
        sys.path.append(os.path.join(PROJECT_HOME, p))
    except Exception as e:
        print(e)
        pass

# import the relevant tools / chunks one by one
try:
    from poastal_github.backend import cli as poastal
except Exception as e:
    print(e)
    pass


def get_poastal(email):
    try:
        return poastal.check_email(email)
    except: 
        return {}



class ghunt:
    async def query(self,email):
        #check if data is an gmail
        try:
            ghunt_creds = GHuntCreds(get_env_var("ghunt_cookie"))
            ghunt_creds.load_creds()
            as_client = httpx.AsyncClient()
            people_api = PeoplePaHttp(ghunt_creds)
            found, person = await people_api.people_lookup(as_client, email)
            print("ghust: data is {} and is {}".format(found,person))
            if found:
                profile = {
                    "google_id":person.personId,
                    "email":person.emails["PROFILE"].value,
                    "name":person.names["PROFILE"].fullname if "PROFILE" in person.names else "N/A"
                }
                return profile
            else:
                return None
        except:
            return None
    

class holehe:


    async def holehe_wrapper(self,email):
        args = namedtuple('Holehe', ["email", "onlyused", "nocolor",
                        "noclear", "nopasswordrecovery", "csvoutput", "timeout"])
        args.email = email
        args.onlyused = False
        args.nocolor = False,
        args.noclear = False
        args.nopasswordrecovery = False
        args.csvoutput = False
        args.timeout = 10

        # Import Modules
        modules = core.import_submodules("holehe.modules")
        websites = core.get_functions(modules, args)
        # Get timeout
        timeout = args.timeout

        # Def the async client
        client = httpx.AsyncClient(timeout=timeout)
        # Launching the modules
        responses = []

        # remove progress bar is it is not neede for a gui
        # instrument = core.TrioProgress(len(websites))
        # trio.lowlevel.add_instrument(instrument)
        async with trio.open_nursery() as nursery:
            for website in websites:
                nursery.start_soon(core.launch_module, website,
                                email, client, responses)
        # trio.lowlevel.remove_instrument(instrument)

        # Sort by modules names
        responses = sorted(responses, key=lambda i: i['name'].lower())

        # Close the client and return results that exist / rate limit was reported back
        await client.aclose()
        hits = [r for r in responses if (r['exists'] or r['rateLimit'])]
        return hits


    async def query(self,email):
        hits = trio.run(self.holehe_wrapper, email)
        return hits