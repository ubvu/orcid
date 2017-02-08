import codecs
import os
import sys
from multiprocessing import Process, Queue
from lxml import etree
import tablib

COLNAME_MODIFIED_DATE = 'last modified date'
COLNAME_CREATION_DATE = 'creation date'
COLNAME_KEYWORDS = 'keywords'
COLNAME_EMAIL = 'email'
COLNAME_WORKS = 'works'
COLNAME_FUNDING = 'funding'
COLNAME_AFFILIATIONS = 'affiliations'
COLNAME_OTHER_NAMES = 'other-names'
COLNAME_CREDIT_NAME = 'credit-name'
COLNAME_FAMILY_NAME = 'family-name'
COLNAME_ORCID = 'orcid'
COLNAME_GIVEN_NAMES = 'given-names'
COLUMN_INTERNAL = 'Internal (by disam. source id)'

nsmap = {
    'x': 'http://www.orcid.org/ns/orcid'
}


def save_to_file(persons, dest):
    column_names = [
        COLNAME_ORCID,
        COLNAME_GIVEN_NAMES,
        COLNAME_FAMILY_NAME,
        COLNAME_CREDIT_NAME,
        COLNAME_OTHER_NAMES,
        COLNAME_AFFILIATIONS,
        COLUMN_INTERNAL,
        COLNAME_FUNDING,
        COLNAME_WORKS,
        COLNAME_EMAIL,
        COLNAME_KEYWORDS,
        COLNAME_CREATION_DATE,
        COLNAME_MODIFIED_DATE,
    ]

    # Add column names for (initially unknown) external identifiers
    all_col_names = {x for person in persons for x in person.keys()}
    ext_id_col_names = {x for x in all_col_names if x not in column_names}
    column_names.extend(ext_id_col_names)

    dataset = tablib.Dataset(column_names, title='ORCID analyse')

    for person in persons:
        person_data = map(lambda x: person.get(x, ''), column_names)
        dataset.append(person_data)

    file_path = os.path.join(os.getcwd(), 'data', dest + '.csv')
    with open(file_path, 'wb') as f:
        f.write(dataset.csv)


with open('organization_ids.txt') as f:
    internal_org_ids = {tuple(line.rstrip('\r\n').split(',')) for line in f}

def parse_person(filehandle):
    person = {}
    root = etree.parse(filehandle).getroot()
    person[COLNAME_ORCID] = root.xpath('//x:orcid-identifier/x:path/text()', namespaces=nsmap)[0]

    print person[COLNAME_ORCID]
    #print sys.getsizeof(root)

    person[COLNAME_AFFILIATIONS] = len(root.xpath('//x:affiliation[x:type[text()=\'employment\']]', namespaces=nsmap))
    person[COLNAME_FUNDING] = len(root.xpath('//x:funding', namespaces=nsmap))
    person[COLNAME_WORKS] = len(root.xpath('//x:orcid-works/x:orcid-work', namespaces=nsmap))

    given_name_elems = root.xpath('//x:personal-details/x:given-names/text()', namespaces=nsmap)
    if len(given_name_elems) > 0:
        person[COLNAME_GIVEN_NAMES] = given_name_elems[0]

    person[COLNAME_OTHER_NAMES] = len(root.xpath('//x:personal-details/x:other-names/x:other-name', namespaces=nsmap))
    family_name_elems = root.xpath('//x:personal-details/x:family-name/text()', namespaces=nsmap)
    if len(family_name_elems) > 0:
        person[COLNAME_FAMILY_NAME] = family_name_elems[0]

    credit_name_elems = root.xpath('//x:personal-details/x:credit-name/text()', namespaces=nsmap)
    if len(credit_name_elems) > 0:
        person[COLNAME_CREDIT_NAME] = credit_name_elems[0]

    email_elems = root.xpath('//x:contact-details/x:email/text()', namespaces=nsmap)
    if len(email_elems) > 0:
        person[COLNAME_EMAIL] = email_elems[0]

    keywords_elems = root.xpath('//x:keywords/x:keyword', namespaces=nsmap)
    person[COLNAME_KEYWORDS] = 'No' if len(keywords_elems) == 0 else 'Yes'

    person[COLNAME_CREATION_DATE] = root.xpath('//x:submission-date/text()', namespaces=nsmap)[0][:10]
    person[COLNAME_MODIFIED_DATE] = root.xpath('//x:last-modified-date/text()', namespaces=nsmap)[0][:10]

    for ext_id_node in root.xpath('//x:external-identifier', namespaces=nsmap):
        source = ext_id_node.find('x:external-id-common-name', nsmap).text
        reference = ext_id_node.find('x:external-id-reference', nsmap).text
        person[source] = reference

    employment_affiliations = root.xpath('//x:affiliation[x:type[text()=\'employment\']]', namespaces=nsmap)
    person[COLNAME_AFFILIATIONS] = len(employment_affiliations)

    person[COLUMN_INTERNAL] = 'N'
    # find the source without an enddate
    curr_affls = 0
    for affiliation in employment_affiliations:
        disam_org_identifier = affiliation.xpath(
            './/x:disambiguated-organization/x:disambiguated-organization-identifier', namespaces=nsmap)
        disam_org_source = affiliation.xpath('.//x:disambiguated-organization/x:disambiguation-source',
                                             namespaces=nsmap)
        org_name = affiliation.xpath('.//x:organization/x:name/text()', namespaces=nsmap)[0]
        org_name = org_name.lower()
        end_date = affiliation.xpath('.//x:end-date', namespaces=nsmap)
        end_year = affiliation.xpath('.//x:end-date/x:year/text()', namespaces=nsmap)

        if len(end_date) == 0:
            colname = 'affl' + str(curr_affls)
            if org_name.find('amsterdam') > -1 or org_name.find('vu') > -1 or org_name.find('free') > -1 or org_name.find('vrije') > -1:
                person[colname] = org_name
                curr_affls = curr_affls + 1

        # check for RINNGOLD ID and strings VU University or Vrije Universiteit
        if len(end_date) == 0:  # current employer
            print org_name
            if disam_org_identifier and disam_org_source:
                if (disam_org_source[0].text, disam_org_identifier[0].text) in internal_org_ids:
                    person[COLUMN_INTERNAL] = 'Y'
            if (org_name.find('vu university') > -1 and org_name.find('vu university medical center')==-1) or org_name.find('vrije universiteit amsterdam') > -1 or org_name.find('free university amsterdam') > -1:
                print '****YES****'
                person[COLUMN_INTERNAL] = 'Y'
    return person

if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        path = '0217'
    source = os.path.join(os.getcwd(), 'data', 'downloads', path)
    persons = []
    for fn in os.listdir(source):
        f = codecs.open(os.path.join(source, fn), 'r', 'utf-8')
        # with open(os.path.join(source, fn), 'r') as f:
        # result = executor.submit(persons.append(parse_person(f)), *args, **kwargs).result()
        persons.append(parse_person(f))
        f.close
    save_to_file(persons, path)
