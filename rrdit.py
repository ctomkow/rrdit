#!/usr/bin/env python

# Run this script to edit various round robin database (RRD) settings that were originally set


import os
from subprocess import call


class RRDit:

    def __init__(self):

        self.main()

    def main(self):

        # backup
        for rrd in self.rrd_files(".", "MAC-ACCT"):
            self.rrd_dump(rrd)

        # edit
        for rrd in self.rrd_files(".", "MAC-ACCT"):
            self.edit_rrd_counter_dsf_max(rrd, "INOCTETS", "1.2500000000e+09")
            self.edit_rrd_counter_dsf_max(rrd, "OUTOCTETS", "1.2500000000e+09")
            self.rrd_dump(rrd)

    def edit_rrd_counter_dsf_max(self, rrd_file, ds_name, max_value):

        max_input = "{}:{}".format(ds_name, max_value)
        call(["rrdtool", "tune", rrd_file, "--maximum", max_input])

    def rrd_dump(self, rrd_file):

        xml_file = self._replace_extension(rrd_file, ".xml")
        fd = open(xml_file, 'w')
        call(["rrdtool", "dump", rrd_file], stdout=fd)
        fd.close()

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