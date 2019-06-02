from WebrootPy import WebrootPy, get_webroot_config
import urllib
from subprocess import Popen, PIPE
import sys


try:
    import msilib
except ModuleNotFoundError:
    print("This utility will only run from Windows.")
    print("In order to build MSI files, the script requires msilib.")
    sys.exit()


def get_sites_keys():
    sites = wr.console_gsm_sites()
    sk = []
    for site in sites['Sites']:
        if not site.suspended and not site.deactivated:
            sk.append((site.site_name, site.account_key_code))
    return sk


def download_new_msi():
    urllib.request.urlretrieve('http://anywhere.webrootcloudav.com/zerol/wsasme.msi', wsasme)


def get_filename_for_site(site):
    return "wsame_" + site.replace(" ", "").replace("&", "_") + ".msi"


def set_serial(filename, license):
    db = msilib.OpenDatabase(filename, msilib.MSIDBOPEN_DIRECT)
    sql = "select * from Property WHERE `Property`='GUILIC'"
    view = db.OpenView(sql)
    view.Execute(None)
    rec = view.Fetch()

    rec.SetString(2, license)
    view.Modify(msilib.MSIMODIFY_REPLACE, rec)

    view.Close()
    db.Commit()


wr = WebrootPy(get_webroot_config("credentials.yaml"))
wsasme = "wsasme.msi"

sites = get_sites_keys()
download_new_msi()

for site in sites:
    filename = "msi\\" + get_filename_for_site(site[0])
    filename = filename.replace(',', '').replace('/', '-')
    print(filename)
    c = Popen(["copy", wsasme, filename], stdout=PIPE, shell=True)
    c.wait(5000)

    set_serial(filename, site[1])
