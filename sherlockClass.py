from engines import *
from sherlock_project import sherlock
# current_path = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(f"{current_path}/sherlock-master/sherlock")



class Sherlock(BaseClass):
    def __init__(self, username, timeout, tor, nsfw):
        self.username = username
        self.timeout = timeout
        self.tor = tor
        self.nsfw = nsfw

    def Search(self):
        username = self.username
        timeout = self.timeout
        tor = self.tor
        nsfw = self.nsfw

        query_notify = sherlock.QueryNotifyPrint(
            result=None, verbose=False, print_all=False, browse=False
        )
        try:
            if False:
                sites = SitesInformation(
                    os.path.join(os.path.dirname(__file__), "resources/data.json")
                )
            else:
                sites = sherlock.SitesInformation(None)
        except Exception as error:
            print(f"ERROR:  {error}")
            sys.exit(1)

        if not nsfw:
            sites.remove_nsfw_sites()
        site_data_all = {site.name: site.information for site in sites}
        if None is None:
            # Not desired to look at a sub-set of sites
            site_data = site_data_all
        else:
            # User desires to selectively run queries on a sub-set of the site list.

            # Make sure that the sites are supported & build up pruned site database.
            site_data = {}
            site_missing = []
            for site in None:
                counter = 0
                for existing_site in site_data_all:
                    if site.lower() == existing_site.lower():
                        site_data[existing_site] = site_data_all[existing_site]
                        counter += 1
                if counter == 0:
                    # Build up list of sites not supported for future error message.
                    site_missing.append(f"'{site}'")

            if site_missing:
                print(f"Error: Desired sites not found: {', '.join(site_missing)}.")

            if not site_data:
                sys.exit(1)

        results = sherlock.sherlock(
            username,
            site_data,
            query_notify,
            tor=tor,
            unique_tor=None,
            proxy=None,
            timeout=timeout,
        )

        results_list = []
        exists_counter = 0
        for website_name in results:
            dictionary = results[website_name]
            if dictionary.get("status").status == sherlock.QueryStatus.CLAIMED:
                exists_counter += 1
                results_list.append(str(dictionary["url_user"]))
        self.results_list = results_list
        # return results_list
    
    def getStatus(self):
        return "Searching"
    
    def getResultsList(self):
        return self.results_list
    
    def getResultsMsgs(self):
        return BaseClass().splitResultsLinksMsg(Sherlock.getResultsList(self))
    
    def getResultsFile(self):
        BaseClass.saveResults(self,"sherlock",self.username,self.results_list)
        return f"sherlock/{self.username}.txt"