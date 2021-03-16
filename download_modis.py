import os
import netrc
def download_date(date, location):
    authTokens = netrc.netrc().authenticators("default")
    command = "modis_download.py -P " + authTokens[2] + " -U " + authTokens[0] + " -p MOD11A1.006 -f " + str(date) + " -e " + str(date) + " -t h11v05,h11v04,h10v05,h09v05,h10v04 " + location
    os.system(command)
