exec(open("./config.py").read())

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

exec(open("./access_token.py").read())
exec(open("./thing_config.py").read())

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

def list_files():
    r = requests.get(thing_url + "files/", headers=headers)
    return json.loads(r.text)

def delete_file(filename):
    for file in list_files():
        if(file["name"] == filename):
            requests.delete(thing_url + "files/" + str(file["id"]), headers=headers)
            r.raise_for_status()

def upload_file(filename):
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

def update_file(filename):
    delete_file(filename)
    upload_file(filename)

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
