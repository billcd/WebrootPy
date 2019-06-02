import requests
from .WebrootToken import WebRootToken
from .Site import Site
from .Tools import urlify


class WebrootPy:
    WR_CREDENTIALS = None
    TOKEN = None
    WR_API_URL = "https://unityapi.webrootcloudav.com/service/api"

    def __init__(self, credentials, raw_token=None, token_cache=None):
        self.WR_CREDENTIALS = credentials
        self.TOKEN = WebRootToken(credentials=credentials, raw_token=raw_token, token_cache=token_cache)

    def standard_get(self, url):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.TOKEN.get_token()['access_token']
        }
        url = self.WR_API_URL + url
        return requests.get(url=url, headers=header).json()

    def standard_post(self, url):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.TOKEN.get_token()['access_token']
        }
        url = self.WR_API_URL + url
        return requests.post(url, headers=header)

    def standard_put(self, url, data=None):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.TOKEN.get_token()['access_token']
        }
        url = self.WR_API_URL + url
        return requests.put(url, headers=header, data=data)

    def standard_delete(self, url):
        pass

    # ------ SkyStatus Endpoint Site ------
    # ------ SkyStatus.Site ------
    def skystatus_site_endpoint_status(self, key, machine_id=None, returned_info=None,
                                       modified_since=None, batch_size=None, continuation=None):
        """
        Returns agent status information for all endpoints matching the specified criteria.
        :param key:
        :param machine_id:
        :param returned_info:
        :param modified_since:
        :param batch_size:
        :param continuation:
        :return: json
        """
        criteria = urlify({"modifiedSince": modified_since, "machineId": machine_id, "returnedInfo": returned_info,
                           "batchSize": batch_size, "continuation": continuation})
        url = '/status/site/' + key + criteria
        return self.standard_get(url)

    # ------ SkyStatus Endpoint Status GSM ------
    # ------ SkyStatus.GSM ------
    def skystatus_endpoint_status_gsm(self, key, machine_id=None, returned_info=None,
                                      modified_since=None, batch_size=None, continuation=None):
        """
        Returns agent status information for all endpoints matching the specified criteria.
        :param key:
        :param machine_id:
        :param returned_info:
        :param modified_since:
        :param batch_size:
        :param continuation:
        :return: json
        """
        criteria = urlify({"modifiedSince": modified_since, "machineId": machine_id, "returnedInfo": returned_info,
                           "batchSize": batch_size, "continuation": continuation})
        url = '/status/gsm/' + key + criteria
        return self.standard_get(url)

    # ------ SkyStatus Keycode Usage ------
    # ------ SkyStatus.Usage ------
    def skystatus_keycode_usage_site(self, key, billing_date=None, continuation=None):
        """
        Returns usage information for a site keycode.
        :param key:
        :param billing_date:
        :param continuation:
        :return: json
        """
        criteria = urlify({"billingDate": billing_date, "continuation": continuation})
        url = '/usage/site/' + key + criteria
        return self.standard_get(url)

    def skystatus_keycode_usage_gsm(self, key, billing_date=None, continuation=None):
        """
        Returns usage information for a master keycode.
        :param key:
        :param billing_date:
        :param continuation:
        :return: json
        """
        criteria = urlify({"billingDate": billing_date, "continuation": continuation})
        url = '/usage/gsm/' + key + criteria
        return self.standard_get(url)

    # ------ Console Console GSM ------
    # ------ Console.GSM ------
    def console_gsm(self):
        """
        Gets information about a given GSM console.
        :return: json
        """
        url = '/console/gsm/' + self.WR_CREDENTIALS['key']
        return self.standard_get(url)

    # ------ Console Console GSM Site Management ------
    # Site management - Provides API calls for listing, creating, deactivating, suspending, and resuming sites
    def console_gsm_sites(self, site_id="", key_code=""):
        """
        Gets the list of sites associated with a given GSM console.
        If site_id specified, gets information about a GSM site.
        :param site_id:
        :param key_code: Locates the correct site_id and searches again.
        :return: json
        """
        url = '/console/gsm/' + self.WR_CREDENTIALS['key'] + '/sites/' + site_id

        if key_code:
            sites = self.standard_get(url)['Sites']
            for s in sites:
                if s['AccountKeyCode'] == key_code.replace('-', '').upper():
                    return self.console_gsm_sites(s['SiteId'])
            # key_code was invalid -- send an invalid id for an accurate error from webroot api
            return self.console_gsm_sites("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

        result = self.standard_get(url)
        sites = []
        try:
            for site in result['Sites']:
                sites.append(Site(json_data=site))
            result['Sites'] = sites
        except KeyError:
            pass

        return result

    def console_gsm_sites_edit(self, site_obj):
        """
        Creates a new site under a given GSM console.
        If site_id is set then this edits the site based on the set parameters in site.
        :param site_obj:
        :return: json
        """
        url = '/console/gsm/' + self.WR_CREDENTIALS['key'] + '/sites/' + site_obj.site_id

        if site_obj.site_id:
            # edit site

            return self.standard_put(url, site_obj.to_webroot_json())
        else:
            # create site
            # url = '/console/gsm/' + self.WR_CREDENTIALS['key'] + '/sites'
            return self.standard_post(url, site_obj.to_webroot_json())

    def console_gsm_site_status(self, site_id, status):
        """
        Changes the status of a site under the GSM console.
        :param site_id:
        :param status: deactivate, suspend, resume, converttrial
        :return: json
        """
        url = '/console/gsm/' + self.WR_CREDENTIALS['key'] + '/sites/' + site_id + "/" + status
        return self.standard_post(url)

    # ------ Console Console GSM User Management ------
    # ------ Console Console GSM Policy Management ------

    # ------ Console Console GSM Group Management ------
    # ------ Console Console GSM Endpoint Management ------
    # ------ Console Console GSM Command Management ------

    # ------ Console Console GSM Threat History Information ------
    # ------ Console Console GSM DNS Protection Management ------
