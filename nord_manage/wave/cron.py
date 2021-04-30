import urllib.request

def email_report():
    url = 'http://localhost:8000/email_report'

    web_url = urllib.request.urlopen(url)

    print(web_url.getcode())

