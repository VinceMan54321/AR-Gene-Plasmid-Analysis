#!/usr/bin/env python

'''
check-ecological-annotation.py by Vincent Huang and Rohan Maddamsetti.

This script compares the output of annotate-ecological-category.py
to the manual annotation in manually-curately-gbk-annotation.table.csv.

Usage: 

'''

manual_accession_to_host = {}
manual_accession_to_isolation_source = {}
manual_accession_to_annotation = {}
with open("../data/manually-curated-gbk-annotation-table.csv") as fh:
    for i, line in enumerate(fh):  # iterates through every line in file, i is a counter
        if i == 0: continue
        line = line.strip()  # trims leading and ending whitespaces
        fields = line.split(',')  # creates a list out of each entry
        accession, host, isolation_source, annotation = fields
        manual_accession_to_host[accession] = host
        manual_accession_to_isolation_source[accession] = isolation_source
        manual_accession_to_annotation[accession] = annotation


notAnnotatedCount = 0
errorCount = 0
correctCount = 0
unstableAnnotationCount = 0

computational_accessions = [] ## for error checking.

with open("../results/AR-gene-duplication/computationally-annotated-gbk-annotated-table.csv") as fh:
    for i, line in enumerate(fh):
        if i == 0: continue ## skip the header.
        line = line.strip()
        fields = line.split(',')
        accession_id, host, isolation_source, annotation = fields
        computational_accessions.append(accession_id)
        if accession_id not in manual_accession_to_annotation:
            notAnnotatedCount += 1
        elif (host != manual_accession_to_host[accession_id]) or (isolation_source != manual_accession_to_isolation_source[accession_id]):
            unstableAnnotationCount += 1
        elif annotation != manual_accession_to_annotation.get(accession_id):
            print("ERROR: annotation does not match.")
            print("Accession ID: ", accession_id)
            print("Manual annotation:", manual_accession_to_annotation.get(accession_id))
            print("Computational annotation:", annotation)
            print()
            errorCount += 1
        elif annotation == manual_accession_to_annotation.get(accession_id):
            correctCount += 1

## find the set difference between the accession ID sets.
unannotated_set = set(computational_accessions) - set([k for k in manual_accession_to_annotation.keys()])
            
print("ERRORS:", errorCount)
print("NOT MANUALLY ANNOTATED:", notAnnotatedCount)
print("EXPECTED NUMBER THAT ARE NOT MANUALLY ANNOTATED:", len(unannotated_set))
print("UNSTABLE ANNOTATIONS (probably upstream errors in gbk parsing):", unstableAnnotationCount)
print("CORRECT:", correctCount)