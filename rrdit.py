#!/usr/bin/env python

### PURPOSE ###
#
# Run this script to edit the RRD files created by mac-acct.pl.
# Specifically addresses an issue in Netharbour where the max input value is 2gb only. This changes max value to 10gb.
# See pull request: https://github.com/netharbour/netharbour/pull/6,
# Modifies the max value data store field for INOCTETS and OUTOCTETS
# NOTE: this script first backs-up all MAC accounting RRD files as .xml ('rrdtool dump'). It doesn't currently delete them
#
### REQUIRES ###
#
# Netharbour. https://github.com/netharbour/netharbour
# Python >= 2.6
#
### RUNIT ###
#
# cd /var/www/html/netharbour/rrd-files (or wherever your RRD files exist)
# git clone https://github.com/ctomkow/rrdit .
# chmod a+x rrdit.py
# python ./rrdit.py


import os
from subprocess import call


class RRDit:

    def __init__(self):

        self.main()

    def main(self):

        path = "."

        # backup
        for rrd in self.rrd_files(path, "MAC-ACCT"):
            self.rrd_dump(rrd)

        # edit
        for rrd in self.rrd_files(path, "MAC-ACCT"):
            self.edit_rrd_counter_dsf_max(rrd, "INOCTETS", "1.2500000000e+09")
            self.edit_rrd_counter_dsf_max(rrd, "OUTOCTETS", "1.2500000000e+09")

    def edit_rrd_counter_dsf_max(self, rrd_file, ds_name, max_value):

        max_input = "{0}:{1}".format(ds_name, max_value)
        print(max_input)
        call(["rrdtool", "tune", rrd_file, "--maximum", max_input])

    def rrd_dump(self, rrd_file):

        xml_file = self._replace_extension(rrd_file, ".xml")
        fd = open(xml_file, 'w')
        call(["rrdtool", "dump", rrd_file], stdout=fd)
        fd.close()

    # Not used at the moment
    def rrd_restore(self, rrd_file, xml_file):

        call(["rrdtool", "restore", xml_file, rrd_file, "--force-overwrite"])
        call(["rm", xml_file])

    def rrd_files(self, path, keyword=""):

        all_rrd = []
        for f in os.listdir(path):
            if f.endswith(".rrd"):
                if keyword in f:
                        all_rrd.append(f)
        return all_rrd

    # Helper methods - should not call directly

    def _remove_extension(self, afile):

        filename, extension = os.path.splitext(afile)
        return filename

    def _add_extension(self, afile, extension):

        return afile + extension

    def _replace_extension(self, afile, new_extension):

        filename, old_extension = os.path.splitext(afile)
        return filename + new_extension


if __name__ == '__main__':
    RRDit()