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

for find, replace in [
    ("Vira", "Viruses"),
    ("Riboviria", "Riboviria (RNA Viruses)"),
    ("Orthornavirae", "Orthornavirae (RNA Polymerase Viruses)"),
    ("Negarnaviricota", "Negarnaviricota (Negative-strand RNA Viruses)"),
    ("Paramyxoviridae", "Paramyxoviridae (Enveloped Negative-strand RNA Viruses)"),
    ("Filoviridae", "Filoviridae (Hemorrhagic Fever Viruses)"),
    ("Polyploviricotina", "Polyploviricotina (Multi-segmented RNA Viruses)"),
    ("Orthomyxoviridae", "Orthomyxoviridae (Influenza-like Viruses)"),
    ("Reovirales", "Sedoreoviridae (Double-Capsid RNA Viruses)"),
    ("Kitrinoviricota", "Kitrinoviricota (Positive-strand RNA Viruses)"),
    ("Alsuviricetes", "Alsuviricetes (Alpha Subgroup Positive-strand RNA Viruses)"),
    ("Hepelivirales", "Hepelivirales (Hepatitis E-related Viruses)"),
    ("arboviruses group A", "Arboviruses A (usually mosquito-transmitted)"),
    ("Flaviviridae", "Flaviviridae (usually mosquito- and tick-transmitted)"),
    ("Orthoflavivirus", "Orthoflavivirus (usually mosquito- and tick-transmitted)"),
    ("Pisoniviricetes", "Pisoniviricetes"),
    ("Betacoronavirus", "Betacoronavirus"),
    ("Picornavirales", "Picornavirales"),
    ("HCoV-SARS", "HCoV-SARS (SARS-like Coronaviruses"),
    ("Picornaviridae", "Picornaviridae"),
    ("common cold viruses", "Enteric Viruses (Gastrointestional)"),
    ("Revtraviricetes", "Revtraviricetes (Reverse Transcriptase Viruses)"),
    ("Orthoherpesviridae", "Orthoherpesviridae (Herpes Viruses)"),
    ("Alphaherpesvirinae", "Alphaherpesvirinae (Rapidly reproducing Herpes Viruses)"),
    ("Bamfordvirae", "Bamfordvirae (Double Jelly Roll Capsid Viruses)"),
    ("Orthopoxvirus", "Orthopoxvirus (Pox viruses)"),
]:
  for taxid in names:
    for name in names[taxid]:
      if name == find:
        friendly_names[taxid] = replace

for taxid, name in friendly_names.items():
  names[taxid].insert(0, name)

with open("html/data.json", "w") as outf:
  json.dump({
    "parent": parent,
    "names": names,
  }, outf)
