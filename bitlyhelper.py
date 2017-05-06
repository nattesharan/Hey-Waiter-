import urllib2
import json
TOKEN = '6e03eed84a9bed3a4777e8afde4da90db51cf4fe'
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"
class BitlyHelper:
    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN,longurl)
            response = urllib2.urlopen(url).read()
            print(response)
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as E:
            print(E)