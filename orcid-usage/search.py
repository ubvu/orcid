import codecs
import orcid_api
from lxml import objectify
import pprint
import os.path
import time
from config import DATAPATH

token=''
def getToken():
    global token
    if token=='':
        token = orcid_api.get_access_token(scope='/read-public', sandbox=False)
    return token

def search_to_file(q, start, rows, filename, sandbox=False):
    token=getToken()
    res = orcid_api.search(token, q, start, rows, sandbox=False)
    fh = open(DATAPATH+filename, "w")
    fh.write(res.content)
    fh.close
    return filename, token

# toevoegen in csv: current affiliation, type employment, zonder end date
def getSearchResults(q):
    datestr=time.strftime("%d%m%y")
    filebase=q.replace('+','')
    filebase = filebase.replace(':', '')
    filebase = filebase.replace('"', '')
    filebase = filebase.replace('*', '')
    filebase = filebase.replace('@', '')
    start=1
    filename='%s_%s_%s.txt' % (filebase,datestr,str(start))

    if not os.path.isfile(DATAPATH + filename):
        search_to_file(q,1,100, filename,sandbox=False)

    with open(DATAPATH+filename) as f:
        content = f.read()
    searchXml=objectify.fromstring(content)

    numfound=int(searchXml['orcid-search-results'].attrib.get('num-found'))
    print('found %s search results for query %s...' % (numfound,q))

    if numfound>0:
        searchfiles=[]
        searchfiles.append(filename)

    if numfound>100:
        iters = numfound / 100
        for c in range(1,iters+1):
            start=(c*100)+1
            filename = '%s_%s_%s.txt' % (filebase, datestr, str(start))
            if not os.path.isfile(DATAPATH + filename):
                search_to_file(q, start, 100, filename, sandbox=False)
            searchfiles.append(filename)
    return searchfiles

def download_orcid(orcid):
    datestr = time.strftime("%m%y")
    dest='%sdownloads/%s' %(DATAPATH,datestr)
    if not os.path.exists(dest):
        os.mkdir(dest)
    dest_file = '%s/%s.xml' %(dest,orcid)
    if not os.path.exists(dest_file):
        token = getToken()
        print('Retrieving %s...' % orcid)
        response = orcid_api.read_public_record(orcid, token, sandbox=False)

        with codecs.open(dest_file, 'w', 'utf-8') as f:
            f.write(response.text)
    else:
        print('Skipping %s, has already been retrieved' % orcid)

resultFiles=getSearchResults('"vu university"+OR+"vrije universiteit amsterdam"')
orcids=[]
for filename in resultFiles:
    with open(DATAPATH+filename) as f:
        content = f.read()
    searchXml=objectify.fromstring(content)
    for child in searchXml['orcid-search-results']['orcid-search-result']:
        orcid=child['orcid-profile']['orcid-identifier']['path']
        #orcids.append(orcid)
        download_orcid(orcid)

