import os 
import sys
import concurrent.futures
from utils.helpers import QueryResponse
import requests
from utils.helpers import get_env_var
import dataclasses
from sherlock_project import sherlock


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




class wmn:

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


        # now we make the request
        try:
            r = requests.get(url)
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
            "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json")
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

