import requests
import json

APIKEY = "AIzaSyBFy_T6NOGizsaY-C8RP2AjKGwmsglSchc "

results = []

def findPlaces(loc=("39.186984","-75.541606"),radius=4500, pagetoken = None):
   lat, lng = loc
   type = ['restaurant']
   url = "https://maps.googleapis.com/maps/api/place/textsearch/json?location={lat},{lng}&radius={radius}&query={type}&key={APIKEY}{pagetoken}".format\
          (lat = lat, lng = lng, radius = radius, type = type,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
   print(url)
   response = requests.get(url)
   res = json.loads(response.text)

   for result in res["results"]:
       results.append(result["name"])

   pagetoken = res.get("next_page_token",None)

   return pagetoken

pagetoken = None

def getPlaces():
    global pagetoken
    while True:
        pagetoken = findPlaces(pagetoken=pagetoken)
        import time
        time.sleep(0.5)

        if not pagetoken:
            break

    return results

