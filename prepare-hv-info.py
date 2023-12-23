#!/usr/bin/env python3

import json
from collections import defaultdict

parent = {}  # child_taxid -> parent_taxid
with open("nodes.dmp") as inf:
  for line in inf:
    child_taxid, parent_taxid, rank, *_ = \
      line.replace("\t|\n", "").split("\t|\t")
    child_taxid = child_taxid
    parent_taxid = parent_taxid
    parent[child_taxid] = parent_taxid

def add_all_ancestors(taxid, relevant_taxids):
  if taxid == "1":
    return
  relevant_taxids.add(taxid)
  add_all_ancestors(parent[taxid], relevant_taxids)

relevant_taxids = set()
friendly_names = {}
with open("highly_curated_viruses.txt") as inf:
  for line in inf:
    taxid, name = line.rstrip("\n").split("\t")
    friendly_names[taxid] = name
    add_all_ancestors(taxid, relevant_taxids)

for taxid in list(parent):
  if taxid not in relevant_taxids:
    del parent[taxid]

# taxid -> [name]
# first name is scientific name
names = defaultdict(list)

with open("names.dmp") as inf:
  for line in inf:
    taxid, name, unique_name, name_class = line.replace("\t|\n", "").split(
      "\t|\t")

    if taxid in relevant_taxids:
      if name_class == "genbank common name":
        names[taxid].insert(0, name)
      else:
        names[taxid].append(name)

friendly_names[10239] = "Viruses";
for taxid, name in friendly_names.items():
  names[taxid].insert(0, name)
        
with open("html/data.json", "w") as outf:
  json.dump({
    "parent": parent,
    "names": names,
  }, outf)
