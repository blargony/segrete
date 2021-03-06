#!/usr/bin/env python
"""
Parse the NCES Data File Format Data files.  Either return a list/dict of items
from the Date Files or cache back as reduced set of the data into much smaller
data files.

Can be run from the command line to pre-filter the NCES raw data into a reduced dataset
to speed up run time.   This can also be done by importing the class itself, but I
exposed it to the command line because this is handy for doing quick experiments.

"""

import argparse
import re
import os
import csv

# Unit testing
import unittest

from fips import fips_to_st
from filters.urban import urban_dist
from filters.big import big_dist
from filters.tuda import tuda_dist
from filters.ca_big import ca_big_dist
from filters.city_zips import sjzips
from data.nces_get import FIRST_YEAR
from data.nces_get import LAST_YEAR

# ==============================================================================
# Constants and RegEx
# ==============================================================================
re_idx_header = re.compile(r'Name\s+Order\s+Type\s+Description')

# Name    Type   Position  Size  Description
re_definition = re.compile(r'^(\w+)\s+(\w+)\s+(\d+)[-](\d+)\s+(\d+)[*]?\s+(.*)$')
re_sub_definition = re.compile(r'^\s*[+](\w+)\s+(\w+)\s+(\d+)[-](\d+)\s+(\d+)\s+(.*)$')

# Variable    Start   End     Field   Data
# Name        Pos.    Pos.    Length  Type    Description
re_alt_definition = re.compile(r'^(\w+)\s+(\d+)\s+(\d+)\s+(\d+)*?\s+(\w+)\s+(.*)$')
re_alt_sub_definition = re.compile(r'^\s*[+](\w+)\s+(\d+)\s+(\d+)\s+(\d+)*?\s+(\w+)\s+(.*)$')

# Index Data Format
# Variable             Data
# Name          Order  Type   Description
re_idx_definition = re.compile(r'^[+]?(\w+)\s+(\d+)[*]?\s+(\w+)\s+(.*)$')

datafile_name = "nces%02d-%02d.txt"
saved_datafile_name = "nces%02d-%02d.csv"
formatfile_name = "nces%02d-%02d_layout.txt"

# ==============================================================================
# Utility Functions
# ==============================================================================
# --------------------------------------
def strip_comment(line, comment_char='#'):
    """
    Strip inline comments - 
    """
    idx = line.find(comment_char)
    if idx != -1:
        line = line[:idx]
    return line.strip()

# --------------------------------------
def longlines(rawdata):
    """
    Generator to merge lines in a text file that end with a "\"
    """
    lines = []
    for i in rawdata.splitlines():
        if i.endswith("\\"):
            lines.append(i.rstrip("\\"))
        else:
            lines.append(i)
            yield "".join(lines)
            lines = []
    if len(lines) > 0: yield "".join(lines)

# ==============================================================================
# Parser Class
# ==============================================================================
class NCESParser(object):
    """
    Parsing Instructions for an NCES data file.

    The instructions consist of list of columns in the database along
    with information needed to pull the column from the file.  Typically
    it will be a string index:

        [('COLUMN_NAME', idx), ('COLUMN_NAME', idx), ...]

    """
    def __init__(self, year, debug=False):
        self.debug = debug
        self.parse_instr = []
        self.header_count = 0
        self.headers = []
        self.descriptions = {}
        self.index_mode = 0
        self.save_names = [
            "FIPS",      # State FIPS numerical representation
            "LEAID",     # School District ID Number
            "LEANM",     # School District Name
            "SCHNAM",    # School name
            "CITY",      # School City
            "STATE",     # School State
            "ZIP",       # School Zip
            "BLACK",     # Number of African American Students
            "HISP",      # Number of Hispanic (non-white) Students
            "ASIAN",     # Number of Students of Asian Decent (South and East)
            "AM",        # Number of American Indian Students
            "WHITE",     # Number of Caucasian Students
            "MEMBER",    # Number of Students
            "FRELCH",    # Number of Free Lunch Eligible students
            "REDLCH",    # Number of Reduced Price Lunch Eligible Students
            "TYPE",      # School Type (Regular, Special Ed, Alternative, etc...)
            "STATUS",    # School Status
            "GSHI",      # Highest Grade Offered
            "GSLO",      # Lowest Grade Offered
            "CHARTR",    # Charter School
            "MAGNET",    # Magnet School
            "LOCALE",    # School Urban Level (Rural, Suburban, Small City, Urban...)
            "ULOCAL"     # Urban School (located within a urban area)
        ]

        self.year = year
        self.formatfile = self.get_formatfile_name()

    def __repr__(self):
        results = ""
        for instr in self.parse_instr:
            if self.index_mode:
                results += "Name:  %s, Index: %d\n" % (instr[0], instr[2])
            else:
                results += "Name:  %s, Size: %d\n" % (instr[0], instr[3] - instr[2] + 1)
        return results

    # --------------------------------------
    def get_formatfile_name(self):
        return self.get_filename(formatfile_name)

    # --------------------------------------
    def get_datafile_name(self):
        return self.get_filename(datafile_name)

    # --------------------------------------
    def get_saved_datafile_name(self):
        return self.get_filename(saved_datafile_name)

    # --------------------------------------
    def get_filename(self, name_str):
        """
        Construct a filename from the base name, a year and
        the local directory structure.
        """
        fname = name_str % (self.year%100, (self.year+1)%100)
        this_dir, this_filename = os.path.split(__file__)
        fname = os.path.join(this_dir, 'data', fname)
        return fname

    # ==============================================================================
    # Read the Format file into a usable data structure
    # ==============================================================================
    # --------------------------------------
    def read_formatfile(self, formatfile):
        if self.debug:
            print "=" * 80
            print "Reading Format File:  %s" % formatfile
            print "=" * 80
        fh = open(formatfile, 'rb')

        for line in fh:
            if re_idx_header.search(line):
                if self.index_mode == 0:
                    print "Switching to Index MODE!!!"
                    self.index_mode = 1

            if re_definition.search(line):
                col_name, type, loidx, hiidx, size, description = re_definition.search(line).groups()
            elif re_sub_definition.search(line):
                col_name, type, loidx, hiidx, size, description = re_sub_definition.search(line).groups()
            elif re_alt_definition.search(line):
                col_name, loidx, hiidx, size, type, description = re_alt_definition.search(line).groups()
            elif re_alt_sub_definition.search(line):
                col_name, loidx, hiidx, size, type, description = re_alt_sub_definition.search(line).groups()
            elif self.index_mode and re_idx_definition.search(line):
                col_name, loidx, type, description = re_idx_definition.search(line).groups()
                hiidx = loidx
                size = 0
            else:
                if self.debug:
                    print line
                continue

            # Filter out a problematic NCES year to year changes
            if col_name[:5] == "FIPST":
                col_name = "FIPS"
                type = 'AN'
            if col_name[:4] == "FIPS":
                type = 'AN'
            if col_name[:3] == "ZIP" and col_name[:4] != "ZIP4":
                col_name = "ZIP"
            if col_name[:4] == "LZIP" and col_name[:5] != "LZIP4" :  # ZIP or Location ZIP (not Mailing ZIP)
                col_name = "ZIP"
            if col_name[:4] == "GSL0":  # 1994 typo in the format file.
                col_name = "GSLO"
            if col_name == "FLE%02d" % (self.year%100):
                col_name = "FRELCH"
            if col_name == ("IND%02d" % (self.year%100)):
                col_name = "AM"
            elif col_name == "IND":
                col_name = "AM"
            if col_name[:4] == "CITY" or col_name[:5] == "LCITY":
                col_name = "CITY"
            if col_name[:4] == "STATE" or col_name[:5] == "LSTATE":
                col_name = "STATE"
            if (col_name[:5] == "LEAID" or
                col_name[:4] == "TYPE" or
                col_name[:6] == "STATUS"):
                type = 'AN'

            self.add_instr(col_name, type, loidx, hiidx, size, description)

        if self.debug:
            print "=" * 80
            print "Format File Parsing Complete"
            print "=" * 80
            import pprint
            pprint.pprint(self.parse_instr)
            print "=" * 80
            print "\n"

    # --------------------------------------
    def add_instr(self, col_name, type, loidx, hiidx, size, description):
        if self.debug:
            print "Found Column:  %s - %s" % (col_name, size)

        # Strip the year off the column if it is present
        # We store the year in the main data object
        if col_name[-2:].isdigit():
            col_name = col_name[:-2]

        # Is it a number?
        if type == 'N':
            pass

        if col_name in self.save_names:
            self.parse_instr.append((col_name, type, int(loidx)-1, int(hiidx), description.strip()))
            self.add_column(col_name, description)

    # --------------------------------------
    def add_column(self, col_name, description):
        self.headers.append(col_name)
        desc = description.strip().split('\t')[0]   # Filter out any Tab characters
        self.descriptions[col_name] = desc
        self.header_count += 1

    # --------------------------------------
    def get_headers(self):
        return self.headers

    # --------------------------------------
    def get_idx(self, col_name):
        try:
            return self.name_idx_dict[col_name]
        except AttributeError:
            self.name_idx_dict = {}
            for i, name in enumerate(self.headers):
                self.name_idx_dict[name] = i
            return self.name_idx_dict[col_name]

    # --------------------------------------
    def get_descriptions(self):
        return ",".join(self.descriptions)

    # --------------------------------------
    def parse_line(self, line):
        entry = []
        for instr in self.parse_instr:
            if self.index_mode:
                field = line[instr[2]]
            else:
                field = line[instr[2]:instr[3]]   # Python array slicing rules  low_idx : high_idx + 1
            if self.debug:
                print field
            if instr[1] == 'N':   # Number Type
                try:
                    field = float(field)
                except ValueError:
                    field = -1.0    # Squash invalid values to -1 for fields of type 'Number'
            else:
                field = field.strip()    # Otherwise clean up the string
            entry.append(field)

        return entry

    # --------------------------------------
    def parse_orig(self, datafile="", make_dict=False):
        # Read the format file
        self.read_formatfile(self.formatfile)

        # Now open the data file
        if datafile:
            fname = datafile
        else:
            fname = self.get_datafile_name()

        fh = open(fname, 'rb')
        if self.index_mode:
            fh = csv.reader(fh, dialect='excel-tab')
            line = fh.next() # Pop the header line

        skip_count = 0
        self.schools = []
        for line in fh:
            if make_dict:
                school = self.make_dict(self.parse_line(line))
                if school['LEANM'].startswith("NEW YORK CITY GEOGRAPHIC DISTRICT"):
                    school['LEAID'] = "3620580"
                    school['LEANM'] = "NEW YORK CITY GEOGRAPHIC DISTRICTS"
                if school['FIPS'] in fips_to_st.keys():
                    self.schools.append(school)
                else:
                    skip_count += 1
            else:
                school = self.parse_line(line)
                if school[self.get_idx('LEANM')].startswith("NEW YORK CITY GEOGRAPHIC DISTRICT"):
                    school[self.get_idx('LEAID')] = "3620580"
                    school[self.get_idx('LEANM')] = "NEW YORK CITY GEOGRAPHIC DISTRICTS"
                if school[self.get_idx('FIPS')] in fips_to_st.keys():
                    self.schools.append(school)
                else:
                    skip_count += 1

        if self.debug:
            print "Found %d Schools" % len(self.schools)
            print "Skipped %d Schools" % skip_count
        return self.schools


    # --------------------------------------
    def parse_saved(self, make_dict=False):

        saved_fname = self.get_saved_datafile_name()
        fh = open(saved_fname, 'rb')

        if make_dict:
            cfh = csv.DictReader(fh, quoting=csv.QUOTE_NONNUMERIC)
            self.headers = cfh.fieldnames
        else:
            cfh = csv.reader(fh, quoting=csv.QUOTE_NONNUMERIC)
            self.headers = cfh.next()

        self.schools = []
        for line in cfh:
            self.schools.append(line)

        if self.debug:
            print len(self.schools)
        return self.schools


    # --------------------------------------
    def parse(self, datafile="", make_dict=False, forced_orig=False):
        if forced_orig or datafile:
            return self.parse_orig(datafile, make_dict)
        else:
            saved_fname = self.get_saved_datafile_name()
            try:
                open(saved_fname, 'rb')
                print "Loading Previously Saved CSV Data Set"
                return self.parse_saved(make_dict)
            except IOError:
                print "Parsing the NCES Data Set"
                return self.parse_orig(datafile, make_dict)

    # --------------------------------------
    def make_dict(self, school):
        if self.debug:
            print school
        return dict(zip(self.headers, school))

    # --------------------------------------
    def save_parsed_data(self, filter=False, idx="", idx_list=[]):
        """
        Save out the parsed data
        """
        fname = self.get_saved_datafile_name()

        fh = open(fname, 'wb')
        cfh = csv.writer(fh, quoting=csv.QUOTE_NONNUMERIC)
        cfh.writerow(self.get_headers())

        count = 0
        for school in self.schools:
            if (not filter or
                    filter and school[self.get_idx(idx)] in idx_list):
                if self.debug:
                    print school
                cfh.writerow(school)
                count += 1
        print "Saved %d Entries to CSV File %s" % (count, fname)

# *****************************************************************************
# Unit Tests
# *****************************************************************************
class TestBasicNetwork(unittest.TestCase):

    def setUp(self):
        self.parse = NCESParser('data/school.test', 'data/school.format')

    def test_old_style(self):
        self.assertEqual(self.parse.something, ["Test"])

# *****************************************************************************
# Program Flow
# *****************************************************************************
# -------------------------------------
# Parse the command line options
# -------------------------------------
def main():
    parser = argparse.ArgumentParser(description='NCES Data File Parser')
    # dataset idx/val matching  - if data[idx] == val then keep this data, filter out all other (e.g. data[state] == CA)
    parser.add_argument('--match_idx', action='store', dest='match_idx', required=False,
            help='Only use data points that match some criterion')
    parser.add_argument('--match_val', nargs='+', action='store', dest='match_val', required=False,
            help='Value to match when using --match_idx')
    # Prepackaged match-idx/val pairs
    parser.add_argument('-urban_only', action='store_true', dest='urban_only', required=False,
            help='Filter out non-Urban Districts')
    parser.add_argument('-big_only', action='store_true', dest='big_only', required=False,
            help='Biggest 50 Districts')
    parser.add_argument('-ca_big_only', action='store_true', dest='ca_big_only', required=False,
            help='Biggest CA Districts')
    parser.add_argument('-tuda_only', action='store_true', dest='tuda_only', required=False,
            help='Select only Districts in the NAEP TUDA List')
    parser.add_argument('-sjzips', action='store_true', dest='sjzips', required=False,
            help='Select only Districts in San Jose, CA')
    # Other Options
    parser.add_argument('-debug', action='store_true',
            help='Print Debug Messages')
    args = parser.parse_args()
    # print args

    # -------------------------------------
    # Actually do the work we intend to do here
    # -------------------------------------
    for year in range(FIRST_YEAR, LAST_YEAR+1):
        print "=" * 80
        print "Saving out a reduced dataset for %d" % year
        print "=" * 80
        parser = NCESParser(year=year, debug=args.debug)
        parser.parse(forced_orig=True)
        if args.urban_only:
            parser.save_parsed_data(filter=True, idx="LEAID", idx_list=urban_dist)
        if args.big_only:
            parser.save_parsed_data(filter=True, idx="LEAID", idx_list=big_dist)
        if args.ca_big_only:
            parser.save_parsed_data(filter=True, idx="LEAID", idx_list=ca_big_dist)
        elif args.tuda_only:
            parser.save_parsed_data(filter=True, idx="LEAID", idx_list=tuda_dist)
        elif args.sjzips:
            parser.save_parsed_data(filter=True, idx="ZIP", idx_list=sjzips)
        elif args.match_idx:
            parser.save_parsed_data(filter=True, idx=args.match_idx, idx_list=args.match_val)
        else:
            parser.save_parsed_data()

# -------------------------------------
# Drop the script name from the args
# and call our command line parser
# -------------------------------------
if __name__ == "__main__":
    main()


