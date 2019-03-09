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
print(access_token)