#!/usr/bin/env python

import json
import argparse
import pprint
from enum import Enum

class ResultType(Enum):
    """Types of results we recognize."""

    smallfile = 1
    fio = 2


class Results:
    """Class for all JSON loads"""

    def __init__(self, infile):
        """Initialized with a passed in file path."""
        # close infile_fp on exceptions
        self.infile = infile
        try:
            infile_fp = open(self.infile)
        except:
            raise

        try:
            self.results = json.load(infile_fp)
        except:
            estr = "Unable to parse JSON data in file " + infile
            raise ValueError(estr)

        if "fio version" in self.results:
            self.resulttype = ResultType.fio

        if "params" in self.results and "operation" in self.results["params"]:
                self.resulttype = ResultType.smallfile

    def display(self):
        """Dump the JSON dictionary"""
        print json.dumps(self.results, indent=2)

        return

    def summary(self):
        """Print key summary elements from the results"""
        if self.resulttype is ResultType.fio:
            self.fiosummary()
        if self.resulttype is ResultType.smallfile:
            self.smallfilesummary()
        return

    def fiosummary(self):
        for job in self.results["client_stats"]:
            if job["jobname"] == 'All clients':
                break

        gopts = self.results.get("global options")
        if gopts["rw"] == "randread" or gopts["rw"] == "read":
            section = job.get("read")
        else:
            section = job.get("write")

        print "{0}#{1}#{2}".format(section["iops"], gopts["rw"], section["runtime"])

    def smallfilesummary(self):
        subresults = self.results.get("results")
        gopts = self.results.get("params")
        print "{0}#{1}#{2}".format(subresults["files-per-sec"], gopts["operation"], subresults["elapsed-time"])

def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result_json",
                        help="Results file in JSON format")
    args = parser.parse_args()

    result = Results(args.result_json)

    #result.display()

    result.summary()


if __name__ == "__main__":
    main()