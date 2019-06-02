from WebrootPy import WebrootPy, get_webroot_config
from pprint import pprint

wr = WebrootPy(get_webroot_config("credentials.yaml"))

sites = wr.console_gsm_sites()
for site in sites['Sites']:
    if not site.suspended and not site.deactivated:
        ep = wr.skystatus_site_endpoint_status(site.account_key_code)['QueryResults']
        found = False

        for e in ep:
            if e['OSAndVersions']['IsOtherAVEnabled']:
                found = True

        if found:
            print(site.site_name + " (" + site.site_id + ")")
            print("Key: " + site.account_key_code)
            print("-------------------------------------------------")

            for e in ep:
                if e['OSAndVersions']['OtherAVProduct']:
                    print(e['HostName'] + "(" + e['OSAndVersions']['internalIP'] + ") " +
                          e['OSAndVersions']['OtherAVProduct'])

            print("\n\n")
