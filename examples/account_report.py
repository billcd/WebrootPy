from WebrootPy import WebrootPy, get_webroot_config
import datetime

WEEKS_SINCE_LAST_SEEN = 4

wr = WebrootPy(get_webroot_config("credentials.yaml"))

total_licenses = 0
all_licenses = 0
total_sites = 0

sites = wr.console_gsm_sites()
for site in sites['Sites']:
    if not site.deactivated:
        ep = wr.skystatus_site_endpoint_status(site.account_key_code)['QueryResults']
        found = False
        deactivated_found = False
        missing_machines = []
        awake_deactivated_machines = []
        site_licenses = 0
        for e in ep:

            if (datetime.datetime.now() - datetime.timedelta(weeks=WEEKS_SINCE_LAST_SEEN)) > \
                    datetime.datetime.strptime(e['LastSeen'], "%Y-%m-%dT%H:%M:%S"):
                if not e['Deactivated']:
                    missing_machines.append(e)
                    found = True
                    all_licenses += 1
            else:
                site_licenses += 1
                all_licenses += 1
                if e['Deactivated']:
                    awake_deactivated_machines.append(e)
                    deactivated_found = True

        total_licenses += site_licenses
        total_sites += 1

        print("-------------------------------------------------")
        print(site.site_name + " (" + site.site_id + ")")
        print("Key: " + site.account_key_code + " Usage: " + str(site_licenses))

        if found:
            for e in missing_machines:
                print(e['HostName'] + "(" + e['OSAndVersions']['internalIP'] + ") has not checked-in in " +
                      str(WEEKS_SINCE_LAST_SEEN) + " weeks.")
            # print("\n")
        else:
            print("All machines have checked-in in the last " + str(WEEKS_SINCE_LAST_SEEN) + " weeks.")

        if deactivated_found:
            for e in awake_deactivated_machines:
                print("!! " + e['HostName'] + "(" + e['OSAndVersions']['internalIP'] + ") has checked-in in " +
                      str(WEEKS_SINCE_LAST_SEEN) + " weeks and is disabled. (" +
                      str(datetime.datetime.strptime(e['LastSeen'], "%Y-%m-%dT%H:%M:%S")) + ")")

print("-------------------------------------------------")
print("Total Sites: " + str(total_sites))
print("Total license usage: " + str(total_licenses))
print("All licenses including deactivated: " + str(all_licenses))
