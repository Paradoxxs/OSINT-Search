import os 
import sys
import concurrent.futures
from utils.helpers import QueryResponse
from utils.user_agents import UserAgent
import requests
from utils.helpers import get_env_var
import dataclasses


header = {
    "User-Agent": UserAgent("computer").user_agent
}


# path to the main folder of the project
PROJECT_HOME = get_env_var("project_dir")
SHERLOCK_PATHS = ["sherlock_github/sherlock"]
PROJECT_PATHS =  SHERLOCK_PATHS

# remove sherlock  main.py that messes up imports
try:
    os.remove(os.path.join(PROJECT_HOME, "__main__.py"))
except:
    pass

# add different projects to sys.path
# this is required for the different projects to run without modification
for p in PROJECT_PATHS:
    try:
        sys.path.append(os.path.join(PROJECT_HOME, p))
    except Exception as e:
        print(e)
        pass
try:
    from sherlock_github.sherlock import sherlock
except Exception as e:
    print(e)
    pass

def get_sherlock(username):
    # results will go here
    hits = []

    # fetch data.json from Github
    sites = sherlock.SitesInformation()

    # Create original dictionary from SitesInformation() object.
    site_data_all = {site.name: site.information for site in sites}
    site_data = site_data_all

    # Create notify object for query results.
    query_notify = sherlock.QueryNotifyPrint(result=None,
                                             verbose=False,
                                             print_all=False,
                                             browse=False)

    results = sherlock.sherlock(username,
                                site_data,
                                query_notify,
                                tor=False,
                                unique_tor=False,
                                proxy=None,
                                timeout=10)

    for website_name, dictionary in results.items():
        if dictionary.get("status").status == sherlock.QueryStatus.CLAIMED:
            hits.append({
                "url": dictionary['url_user'],
                "domain": website_name
            })
    query_notify.finish()
    return hits


# coding: utf-8




class wmn():

    def get_data(self,username, checker_dict):

        platform_name = checker_dict["name"]
        response = QueryResponse(platform=platform_name, selector=username)

        # filter out username with invalid chars - could also be done outside this function
        invalid_chars = checker_dict.get("invalid_chars")
        if invalid_chars and invalid_chars in username:
            return response

        # the template where the username goes
        url_template = checker_dict["uri_check"]
        url = url_template.format(**{"account": username})
        try:
            url_pretty = checker_dict["uri_pretty"].format(**{"account": username})
        except:
            url_pretty = url


        # custom client
        # we use a dict for shared args
        # but tls_client does not have a timeout (it is hardcoded to 10 sec) where as requests does
        args = {
            "headers": header,
            "allow_redirects": False
        }

        # now we make the request
        try:
            r = requests.get(url, **args)
        except Exception as e:
            #unable to connect
            response.exists = None
            return response

        # if exists
        e_code = checker_dict["e_code"]
        e_string = checker_dict["e_string"]

        # if missing
        m_string = checker_dict["m_string"]
        m_code = checker_dict["m_code"]

        html = r.text
        status_code = r.status_code

        # exists
        if e_code == status_code and e_string in html:
            account_exists = True
            response.url = url_pretty

        # missing
        elif m_code == status_code and m_string in html:
            account_exists = False

        # status_code and string does not match
        else:
            print(
                f"Unexpected response: {url}")
            account_exists = None
        response.exists = account_exists
        return response


    def get_sites_from_github(self):
        r = requests.get(
            "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json", headers=header)
        data = r.json()
        github_sites = data["sites"]
        return github_sites


    def query(self,username):
        Sites = self.get_sites_from_github()

        MAX_WORKERS = 10

        usernames = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.get_data, username, checker_dict) for checker_dict in Sites]

        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            usernames.append(response)
            print(response)
        print(usernames)

        usernames = [dataclasses.asdict(r) for r in usernames if r.exists]
        usernames.sort(key=lambda x: x["platform"].lower(), reverse=False)
        return usernames

