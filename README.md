# rrdit
Modify max value in data store fields of RRD files for MAC accounting in Netharbour

### PURPOSE
Run this script to edit the RRD files created by mac-acct.pl.

Specifically addresses an issue in Netharbour where the max input value is 2gb only. This changes max value to 10gb.

See pull request: https://github.com/netharbour/netharbour/pull/6

Modifies the max value data store field for INOCTETS and OUTOCTETS

NOTE: this script first creates backups of all MAC accounting RRD files as .xml ('rrdtool dump'). It doesn't currently delete them

### REQUIRES
Netharbour. https://github.com/netharbour/netharbour

Python >= 2.6

### RUNIT
`cd /var/www/html/netharbour/rrd-files` (or wherever your RRD files exist)

`git clone https://github.com/ctomkow/rrdit .`

`chmod a+x rrdit.py`

`python ./rrdit.py`
