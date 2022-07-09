"""Automate WMx dummy load process.
Usage:
------
    $ automate [options]
Run the automation script with mandatory options:
    $ automate -u <username> -p <password> -t <num>
Run the automation script and load totes from excel file:
    $ automate -u <username> -p <password> -t <num> -e <excel>
Use specific loadid:
    $ automate -u <username> -p <password> -t <num> -l <loadid>
Download otr excel sheet:
    $ automate -u <username> -p <password> -t <num> -f
Available options are:
    -u, --username     WMx username to login
    -p, --password     WMx password to login
    -l, --loadid       Load ID to be used for loading
    -t, --threads      Number of threads this script will generate
    -e, --excelfile    Excel file containing Aging Totes Report to be processed and loaded to dummy load. If left empty, script will directly grab ATR from Bax
    -f, --format       Color codes and downloads the Aging Tote Report into an Excel sheet that you can copy to the Sharepoint file
    -v, --version      Display version number
    -h, --help         Show this help
Contact:
--------
- asori015@ucr.edu
More information is available at:
- https://github.com/asori015/wmx
Version:
--------
- wmx-automate v1.1.1
"""
# Standard library imports
import tkinter

# WMx imports
import wmx
from wmx import automate


def main() -> None:
    automate.x()

if __name__ == "__main__":
    main()