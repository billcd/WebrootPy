from WebrootPy import WebrootPy, get_webroot_config
import datetime

WEEKS_SINCE_LAST_SEEN = 4

wr = WebrootPy(get_webroot_config("credentials.yaml"))

sites = wr.console_gsm_sites()
for site in sites['Sites']:
    if not site.deactivated:
        ep = wr.skystatus_site_endpoint_status(site.account_key_code)['QueryResults']
        found = False
        machines = []

        for e in ep:
            if datetime.datetime.strptime(e['LastSeen'], "%Y-%m-%dT%H:%M:%S") < \
                    (datetime.datetime.now() - datetime.timedelta(weeks=WEEKS_SINCE_LAST_SEEN)) \
                    and not e['Deactivated']:
                machines.append(e)
                found = True

        if found:
            print(site.site_name + " (" + site.site_id + ")")
            print("Key: " + site.account_key_code)
            print("-------------------------------------------------")

            for e in machines:
                print(e['HostName'] + "(" + e['OSAndVersions']['internalIP'] + ")")

            print("\n")
