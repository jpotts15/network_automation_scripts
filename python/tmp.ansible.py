tmper = """411 - FITSP-O or GICSP or CASP+ or CCNP-Security or CISA or SSCP
421 - CASP+ or CCNP-Security or CISA or CISSP or CISSP-ISSAP or CISSP-ISSEP
431 - FITSP-O or GICSP or CASP+ or CCNP-Security or CISA or SSCP
441 - CCNA or GCIA or GCLD or GDSA or GFACT or CASP+ or CCNP-Security or CCSP or GCED or GCIH
451 - FITSP-O or GFACT or CASP+ or CCNP-Security or CCSP
632 - FITSP-D or GCSA or GISF or SSCP
641 - GCSA or CASP+ or GSLC
651 - CISSO or GCIA or GCSA or GCLD or GICSP or CISSP-ISSAP or CISSP-ISSEP
661 - GCLD or CCE or CASP+ or CEH
671 - CCSP
212 - CySA+ or PenTest+ or CFR or GCFE or GCFA or CCE
511 - CySA+ or CBROPS or CFR or FITSP-O or GCIA or GDSA or GICSP or GCFA
521 - GCIA or GCLD or GDSA or GICSP or CISSP-ISSAP or CISSP-ISSEP
531 - CySA+ or CFR or GCFA or GCIA or GDSA or GCIH or GICSP or CCE 
541 - CISSO or CPTE or CySA+ or CFR or FITSP-A or GCSA or GPEN or CCE or CISA or CISM or GCIH or GSNA
611 - FITSP-M or GCSA or GSLC or CCISO or CISM or CISSP-ISSEP or CISSP-ISSMP or CISSP
612 - CISM or CISSO or CPTE or CySA+ or FITSP-A or GCSA or CISA or CISSP or CISSP-ISSEP or GSLC or GSNA
622 - CSC or GCSA or GCLD or CISSP-ISSEP
631 - FITSP-D or GCSA or CISSP-ISSEP
652 - CISM or CISSO or FITSP-D or GCIA or GCSA or GCLD or GDSA or GICSP or CISSP-ISSAP or CISSP-ISSEP
722 - CISM or CISSO or FITSP-M or GCIA or GCSA or GCIH or GSLC or GICSP or CISSP-ISSMP or CISSP
723 - CISM or CISSO or FITSP-M or GCSA or GCIH or GSLC or GICSP"""
dod8140_dict = {'reverse':{},'certs':set(),'classifications':set(),'cert_count':{}}

for line in tmper.split('\n'):
    liner = line.split()
    for item in liner:
        if item == "or":
            liner.remove(item)
    dod8140_dict['classifications'].add(liner[0])
    dod8140_dict[liner[0]] = liner[2:]
for key, value in dod8140_dict.items():
    if key != "reverse":
        for v in value:
            dod8140_dict['certs'].add(v)
            if v not in dod8140_dict['reverse'].keys():
                dod8140_dict['reverse'][v] = [key]
            else:
                dod8140_dict['reverse'][v].append(key)

def sort_by_coverage():
    return sorted(dod8140_dict['reverse'].items(), key=lambda x: len(x[1]), reverse=True)

def find_minimum_cover():
    remaining = set(dod8140_dict['classifications'])
    selected_certs = []
    
    while remaining:
        best_cert, best_cover = max(dod8140_dict['reverse'].items(), key=lambda x: len(set(x[1]) & remaining))
        selected_certs.append(best_cert)
        remaining -= set(best_cover)
        dod8140_dict['reverse'].pop(best_cert)
    
    return selected_certs

# Example usage:
sorted_certs = sort_by_coverage()
print("Sorted Certifications by Coverage:")
for cert, count in sorted_certs:
    print(f"{cert}: {len(count)} classifications")

min_cover = find_minimum_cover()
print("\nMinimum Set of Certifications to Cover All Classifications:")
print(min_cover)
