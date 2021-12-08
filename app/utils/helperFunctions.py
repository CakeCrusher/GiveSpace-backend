import os
from flask.json import jsonify
import requests
from app.utils.schemas import *
# import asyncio
# import aiohttp
# from aiohttp import ClientSession
import json

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