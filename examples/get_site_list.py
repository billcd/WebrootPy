from WebrootPy import WebrootPy, get_webroot_config
from pprint import pprint

wr = WebrootPy(get_webroot_config("credentials.yaml"))

# sites = wr.get_console_gsm_sites()
sites = wr.console_gsm_sites()
for site in sites['Sites']:
    if not site.suspended and not site.deactivated:
        print(site.site_name + " " + site.site_id + " ")
