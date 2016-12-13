# How to use this ORCiD-usage Monitor
The monitor will produce an spreadsheet with in each column the usage status of different elements of each ORCiD.
This way you can monitor if and how people ORCiD up to its potential.

#Preparation
- copy this orcid-monitor code to your system
- install python
- open command line, go to the location of the orcid-monitor code

## API keys
Rename file ```config.example.py``` to ```config.py```
Change the Client ID and API key to the one's you got from ORCiD.
Get key's? Read more on https://orcid.org/content/register-client-application-0 

## List organisation markers
First create a file ```organization_ids.txt``` .
This contains id's that are known in the ORCiD database that mark your research organisation.
Currently Ringrold-id's and Fundref-id's are used. List each organisation id on a new line. Use prefix FUNDREF, or RINGOLD, to namespace the id's; use a comma to separate the prefix from id.
Find your organisation id on http://ido.ringgold.com and on http://ftp.crossref.org/fundref/fundref_registry.html

## List ORCiD's
Then make a file ```orcids.txt``` with a list of ORCiDs you want to monitor. Each orcid on a new line. Orcid's include dashes.

# Operation

## Download ORCiD's
Next, download XML from ORCiD's.
In the orcid-monitor folder use the folowing:
```
python download.py [name of dataset folder]
```
For example:
```
python download.py dec2016
```
This will create a folder ```dec2016``` with xml files on each orcid.
 
## Analyse ORCiD's
Now run the analysis.
```
python analyse.py [name of dataset folder]
```
for example:
```
python download.py dec2016
```

This results in a new file ```[name of dataset folder].csv```
