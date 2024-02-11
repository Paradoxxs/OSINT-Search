from modules.Username_lookup import get_sherlock, wmn


class Username():

    async def search(username):
        print(username)
        sherlock_data = get_sherlock(username)
        sherlock_data.sort(key=lambda x: x["domain"].lower(), reverse=False)
        #append source to sherlock hits
        for hit in sherlock_data:
            hit["source"] = "sherlock"
    
        whm_data = wmn.query(username)
        # append source to whm_data
        for hit in whm_data:
            hit["source"] = "whm"
            hit["domain"] = hit["platform"]

            # combine sherlock and whm hits
            hits = sherlock_data + whm_data

            # TODO compromised username
            return hits