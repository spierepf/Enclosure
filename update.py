execfile( "config.py" )

import os.path
if not os.path.isfile('access_token.py'):
    import webbrowser
    from threading import Thread

    url="https://www.thingiverse.com/login/oauth/authorize?response_type=token&client_id="+client_id

    def myfunc(url):
        webbrowser.open(url)

    t = Thread(target=myfunc, args=(url,))
    t.start()

    url=raw_input("Please copy and paste the browser url here: ");

    f = open("access_token.py", "a")
    f.write(url.split("#")[1].replace('=', '="') + '"')
    f.close()

execfile( "access_token.py" )
execfile( "thing_config.py" )

import requests
import logging

r = requests.post("https://www.thingiverse.com/login/oauth/tokeninfo?access_token="+access_token)
r.raise_for_status()

base_url = "https://api.thingiverse.com"
thing_url = base_url + "/things/"+str(thing_id)+"/"

headers = { "Authorization": "Bearer "+access_token }

with open('README.md', 'r') as myfile:
    description=myfile.read()
r = requests.patch(thing_url, json={ "description" : description }, headers=headers)
r.raise_for_status()

r = requests.get(thing_url, headers=headers)
r.raise_for_status()

import json

def update_file(filename):
    r = requests.post(thing_url + "files", json={ "filename" : filename }, headers=headers)
    r.raise_for_status()

    response = json.loads(r.text)
    data = []
    for key in ["AWSAccessKeyId", "bucket", "key", "acl", "success_action_redirect", "policy", "signature", "Content-Type", "Content-Disposition"]:
        data.append((key, (None, response["fields"][key])))

    with open(filename, 'r') as myfile:
        content=myfile.read()

    data.append(("file", (filename, content)))

    r = requests.post(response["action"], files=data, allow_redirects=False)
    r.raise_for_status()

    r = requests.post(response["fields"]["success_action_redirect"], headers=headers)
    r.raise_for_status()

# POST / HTTP/1.1
# Host: thingiverse-production.s3.amazonaws.com
# Content-Type: multipart/form-data; boundary=---------------------------66289253989742337765937765
# Content-Length: 12357

# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="AWSAccessKeyId"

# 0S2CMSXYJEXCGHRR6K82
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="bucket"

# thingiverse-production
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="key"

# uploads/84/37/86/ef/74/SuperCoolThing.stl
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="acl"

# public-read
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="success_action_redirect"

# https://api.thingiverse.com/files/111382/finalize
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="policy"

# eyJleHBpcmF0aW9uIjoiMjAxMi0xMi0yOVQxOTozNDoyN1oiLCJjb25kaXRpb25zIjpbeyJhY2wiOiJwdWJsaWMtcmVhZCJ9LHsiYnVja2V0IjoidGhpbmdpdmVyc2UtcHJvZHVjdGlvbiJ9LFsic3RhcnRzLXdpdGgiLCIka2V5IiwidXBsb2Fkc1wvIl0sWyJzdGFydHMtd2l0aCIsIiRDb250ZW50LVR5cGUiLCIiXSxbInN0YXJ0cy13aXRoIiwiJENvbnRlbnQtRGlzcG9zaXRpb24iLCIiXSx7InN1Y2Nlc3NfYWN0aW9uX3JlZGlyZWN0IjoiaHR0cDpcL1wvd3d3LnRoaW5naXZlcnNlLmNvbVwvdGhpbmdzXC9maW5hbGl6ZSJ9LFsiY29udGVudC1sZW5ndGgtcmFuZ2UiLDEsMjYyMTQ0MDAwXV19
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="signature"

# dyqah6pLNWvjI4AemGsvq/vjVtE=
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="Content-Type"

# application/sla
# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="Content-Disposition"


# -----------------------------66289253989742337765937765
# Content-Disposition: form-data; name="file"; filename="SuperCoolThing.stl"
# Content-Type: application/sla
# ... A BUNCH OF BINARY DATA ...
# -----------------------------66289253989742337765937765    

# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

for thing_file in thing_files:
    if not os.path.isfile(thing_file):
        base_name,extension = os.path.splitext(thing_file)
        source_file = base_name + ".scad"
        assert os.path.isfile(source_file)
        import subprocess
        subprocess.call(["openscad", source_file, "-o", thing_file])
        assert os.path.isfile(thing_file)
        update_file(thing_file)
        os.remove(thing_file)
    else:
        update_file(thing_file)
