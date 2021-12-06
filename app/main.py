from flask import Flask, jsonify, request
import requests
import os
from app.utils.helperFunctions import fetchGraphQL
from app.utils.schemas import CREATE_FRIEND_REL, FIND_USERS

app = Flask(__name__)

POS_URL = "https://api-inference.huggingface.co/models/flair/pos-english-fast"
headers = {"Authorization": f"Bearer {os.environ.get('HF_API_KEY')}"}



@app.before_request
def before():
  print('|\n|\n|')


@app.route('/item_search/', methods=['POST'])
def item_search():
  def query(payload):
    response = requests.post(POS_URL, headers=headers, json=payload)
    return response.json()
  req = request.json["input"]
  print(req)
  res = query(req["text"])

  items = []
  for entity in res:
    if (entity["entity_group"] == 'NN') | (entity["entity_group"] == 'NNS'):
      items.append(entity["word"].strip())
  items = list(set(items))

  modified_text = req["text"]
  for item in items:
    modified_text = modified_text.replace(item, f'$${item}$$', 1)

  return jsonify({"inspected_text": modified_text})

@app.route('/contacts_to_friends/', methods=['POST'])
def contacts_to_friends():
  req = request.json["input"]
  find_users_req = fetchGraphQL(FIND_USERS, {
    "phone_numbers": req["contacts_phone_numbers"]
  })
  print(find_users_req)
  list_of_user_contacts = map(lambda x: x["phone_number"], find_users_req["data"]["user"])
  # sort a list of numbers
  new_friend_rels = []
  for phone_number in list_of_user_contacts:
    sorted_pair = sorted([phone_number,req["user_phone_number"]])
    create_friend_rel_req = fetchGraphQL(CREATE_FRIEND_REL, {
      "user_first": sorted_pair[0],
      "user_second": sorted_pair[1],
      "type": "friends"
    })
    try:
      desired_result = create_friend_rel_req["data"]["insert_friend_rel"]["returning"]
      if len(desired_result):
        new_friend_rels.append(desired_result[0]["id"])
    except:
      pass


  return jsonify({"new_friend_rels": new_friend_rels})

