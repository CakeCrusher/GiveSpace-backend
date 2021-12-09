import os
from flask.json import jsonify
import requests
from app.utils.schemas import *
# import asyncio
# import aiohttp
# from aiohttp import ClientSession
import json
import urllib.parse
from bs4 import BeautifulSoup

def fetchGraphQL(query, variables={}):
    graphql = {
      "query": query,
      "variables": variables
    }
    headers = {
      'content-type': 'application/json',
      'x-hasura-admin-secret': os.environ.get('HASURA_ADMIN_SECET'),
    }
    response = requests.post(
      'https://givespace.hasura.app/v1/graphql', 
      headers=headers,
      json=graphql,
    )
    return response.json()

# async def add_friend_rels_from_contacts(user_id, contacts_phone_numbers):
#   # req = request.json["input"]
#   find_users_req = fetchGraphQL(FIND_USERS, {
#     "phone_numbers": contacts_phone_numbers
#   })
#   list_of_user_contacts = map(lambda x: x["id"], find_users_req["data"]["user"])
#   # sort a list of numbers
#   async def create_friend_rels(sorted_pair, session):
#       graphql = {
#         "query": CREATE_FRIEND_REL,
#         "variables": {
#           "user_first_id": sorted_pair[0],
#           "user_second_id": sorted_pair[1],
#           "type": "friends"
#         }
#       }
#       create_friend_rel_req = await session.request(
#         "POST", 
#         "https://givespace.hasura.app/v1/graphql", 
#         headers = {
#           'content-type': 'application/json',
#           'x-hasura-admin-secret': os.environ.get('HASURA_ADMIN_SECET')
#         },
#         json=graphql
#       )
#       print('MADE REQUEST')
#       try:
#         desired_result = create_friend_rel_req["data"]["insert_friend_rel"]["returning"]
#         print(create_friend_rel_req)
#         if len(desired_result):
#           # new_friend_rels.append(desired_result[0]["id"])
#           return desired_result[0]["id"]
#       except:
#         return
      
  
#   async with ClientSession() as session:
#     new_friend_rels = []
#     fetch_tasks = []
#     for id in list_of_user_contacts:
#       sorted_pair = sorted([id,user_id])
#       fetch_tasks.append(create_friend_rels(sorted_pair, session))
#     results = await asyncio.gather(*fetch_tasks)
#     print(results)
#     session.close()
    
#   return new_friend_rels

def add_friend_rels_from_contacts(user_id, contacts_phone_numbers):
  # req = request.json["input"]
  find_users_req = fetchGraphQL(FIND_USERS, {
    "phone_numbers": contacts_phone_numbers
  })
  list_of_user_contacts = map(lambda x: x["id"], find_users_req["data"]["user"])
  # sort a list of numbers
  friend_rels = []
  for id in list_of_user_contacts:
    sorted_pair = sorted([id,user_id])
    friend_rels.append({
      "user_first_id": sorted_pair[0],
      "user_second_id": sorted_pair[1],
      "type": "friends"
    })
  create_friend_rel_req = fetchGraphQL(CREATE_FRIEND_REL, {
    "friend_rels": friend_rels
  })
  try:
    if (create_friend_rel_req["errors"]):
      return []
  except:
    pass
  new_friend_rels = create_friend_rel_req["data"]["insert_friend_rel"]["returning"]
  new_friend_rels_ids = list(map(lambda x: x["id"], new_friend_rels))
  return new_friend_rels_ids

def scrape_features(item_name):
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
  }
  parsed_item_name = urllib.parse.quote_plus(item_name)
  req = requests.get(f"https://www.amazon.com/s?k={parsed_item_name}&ref=nb_sb_noss_2", headers=headers)
  soup = BeautifulSoup(req.text, "html.parser")
  validItems = []

  try:
    container = soup.find_all('div', {'class': 's-asin'})
    for item in container:
      try:
        isSponsored = item.find('span', {'class': 's-label-popover-default'})
        if not isSponsored:
          itemName = item.find('h2').text
          price = item.find('span', {'class': 'a-price-whole'}).text
          if len(price) > 0:
            price = float(price)
          else:
            price = 0.0
          imageUrl = item.find('img', {'class': 's-image'}).get('src')
          itemUrl = item.find('a', {'class': 'a-link-normal'}).get('href')
          itemUrl = "https://www.amazon.com" + itemUrl
          validItems.append({
            "name": itemName,
            "item_url": itemUrl,
            "image_url": imageUrl,
            "price": price
          })
      except:
        pass
  except Exception as e:
    print(e)

  if len(validItems) == 0:
    print("req!:", req.text)
    return {'name': 'NONE', 'item_url': 'NONE', 'image_url': 'https://icons-for-free.com/iconfiles/png/512/gift+present+icon-1320087141027318051.png', 'price': 0}

  return validItems[0]