import codecs
import os
import sys

import orcid_api


def download_orcid(orcid, dest_folder, token):
    dest_file = os.path.join(dest_folder, orcid + '.xml')

    if not os.path.exists(dest_file):
        print('Retrieving %s...' % orcid)
        response = orcid_api.read_public_record(orcid, token, sandbox=False)

        with codecs.open(dest_file, 'w', 'utf-8') as f:
            f.write(response.text)

    else:
        print('Skipping %s, has already been retrieved' % orcid)


if __name__ == '__main__':
    path = sys.argv[1]

    dest = os.path.join(os.getcwd(), 'data', 'downloads', path)

    if not os.path.exists(dest):
        os.mkdir(dest)

    token = orcid_api.get_access_token(scope='/read-public', sandbox=False)

    with open('orcids.txt') as f:
        for line in f:
            download_orcid(line.rstrip('\r\n'), dest, token)
