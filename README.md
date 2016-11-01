# orcid-monitor
The orcid monitor contains two tools. The orcid-usage-grade and the orcid-potential.

* [Download and documentation](https://ubvu.github.io/orcid-monitor/)

## orcid-usage-grade
This tool checks how active a person has used the elements and connectability of her ORCiD record.

* input is a list of ORCiD's we know from researchers using it in PURE, our research information system, and the orcid-potential (see below)
* output is a datafile with additional columns defining the usage grade of the orcid records.
* usage grade is measued by if and how many (sub-)entries an orcid record contains about: affiliation, funding, works, other names, other identifiers, etc.

## orcid-potential
This tool checks the pool of researchers in the ORCiD database from a research institution.

* input is based on a datafile exported from the research information systemen PURE. 
* This datafile contains the DOI's of all the currently active researchers, and the last name.
* The tool matches the last name with the returned orcid records.
