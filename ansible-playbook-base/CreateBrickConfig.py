#!/usr/bin/env python

# This would be some python code that would take in the required arguments to
# generate a storage configuration JSON file and also possibly a gdeploy
# configuration file for use with other plays.
# This python will also check (first) if the given volume(s) can be configured
# in the given setup

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("vc_definition", help="Volume configuration definition file")
parser.add_argument("sc_definition", help="Storage setup definition file")
parser.add_argument("saved_facts", help="Saved facts in JSON from server hosts")
args = parser.parse_args()

print(args.vc_definition)
print(args.sc_definition)
print(args.saved_facts)

saved_facts_fp = open(args.saved_facts)

hosts_data = json.load(saved_facts_fp)

# print (json.dumps(hosts_data))

outdict = {}

for k, v in hosts_data.iteritems():
        for idx in range(len(v)):
                outdict[v[idx].get("inventory_hostname", "not found!")] = str(idx) + "test"
                print k, v[idx].get("inventory_hostname", "not found!")

print outdict
print json.dumps(outdict, indent=2)

storage_conf_fp = open("./storageconfiguration.json", "w")

json.dump(outdict, storage_conf_fp)

storage_conf_fp.close()
