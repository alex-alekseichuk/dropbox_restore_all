#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Include the Dropbox SDK libraries
import sys
from dropbox import client, rest, session

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'Provide app key here'
APP_SECRET = 'Provide app secret here'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

# Make the user sign in and authorize this token
url = sess.build_authorize_url(request_token)
print "url:", url
print "Please authorize in the browser. After you're done, press enter."
raw_input()

# This will fail if the user didn't visit the above URL and hit 'Allow'
try:
    access_token = sess.obtain_access_token(request_token)
except rest.ErrorResponse, e:
    print "You are not authenticated"
    sys.exit()

client = client.DropboxClient(sess)
#print "linked account:", client.account_info()

def process_folder(path):
    print 'process folder', path.encode('ascii', 'replace')
    folder_metadata = client.metadata(path, include_deleted=True)
    for meta in folder_metadata['contents']:
        if meta['is_dir']:
            process_folder(meta['path'])
        elif meta.has_key('is_deleted') and meta['is_deleted']:
            f = meta['path']
            print 'restore file', f.encode('ascii', 'replace')
            revs = client.revisions(f, rev_limit=2)
            if len(revs) >= 2:
                client.restore(f, revs[1]['rev'])

process_folder(u'/')
