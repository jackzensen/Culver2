import requests
from bs4 import BeautifulSoup
import re
import asyncio
import datetime
from dateutil.parser import parse

import aiohttp

# Configure a virtual browser for parser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


# loc is the restaurant's ID number
# it can be used to travserse a specific restaurant's webpage (eg culvers.com/location/loc)
# For a specific location, it can be found by hovering over the map & directions url on the webpage and reading key=loc, or by reading 
# the preview for adding to your calendar (culvers.com/fotd-add-to-calendar/loc/date)

def scrape(loc):
    TIMEOUT = 5
    s = requests.Session()
    try:
        url = 'http://Culvers.com/location/' + str(loc) + '#entire-month'
        result = s.get(url, timeout=TIMEOUT, headers=headers)
        doc = BeautifulSoup(result.text, "html.parser")

        flav = doc.find_all("div", class_="lowerstub")
        dict_list = []
        RestaurantList = []
        for tag in flav:
            tempDict = {}
            
            Date = tag.select('h3', class_='date h3alt')[0].getText()
            Date = str(Date)
            
            Flavor = tag.select('a', class_='value')[0].getText()
                
            Date = parse(Date, fuzzy=True)
            Date = Date.strftime("%x")
            
            if Flavor == '\n\n':
                continue
            else:
                tempDict[Date] = Flavor 
                dict_list.append(tempDict)
    except:
        print(f'error occured for location {loc}')    
        
    return dict_list

print(scrape(99))





# Start of future implementation to significantly reduce runtime by sending requests to multiple locations at a time. (For larger scraping needs)
# async def main():

#     async with aiohttp.ClientSession() as session:

#         for number in range(853, 854):
#             culvers_url = f'http://Culvers.com/location/' + str(number) + '#entire-month'
#             async with session.get(culvers_url) as resp:
#                 site = await resp.json()
#                 doc = json.loads(response.text)
#                 print(site['name'])
                
                
#                 flav = doc.find_all("div", class_="lowerstub")
#                 dict_list = []
#                 for tag in flav:
#                     tempDict = {}
#                     Date = tag.select('h3', class_='date h3alt')[0].getText()
#                     Flavor = tag.select('a', class_='value')[0].getText()
#                     tempDict[Date] = Flavor
#                     dict_list.append(tempDict)    
#                 print(dict_list)           
# asyncio.run(main())