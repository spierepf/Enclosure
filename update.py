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

r = requests.post("https://www.thingiverse.com/login/oauth/tokeninfo?access_token="+access_token)
r.raise_for_status()

base_url = "https://api.thingiverse.com"

headers = { "Authorization": "Bearer "+access_token }

with open('README.md', 'r') as myfile:
    description=myfile.read()
r = requests.patch(base_url + "/things/"+str(thing_id)+"/", json={ "description" : description }, headers=headers)
r.raise_for_status()

r = requests.get(base_url + "/things/"+str(thing_id)+"/", headers=headers)
r.raise_for_status()
print(r.text)