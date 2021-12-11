from flask import Flask, jsonify, request
import requests
import os
from app.utils.helperFunctions import *
from app.utils.schemas import *
from argon2 import PasswordHasher
import jwt

Password = PasswordHasher()

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

  new_friend_rels = add_friend_rels_from_contacts(req["user_id"], req["contacts_phone_numbers"])

  return jsonify({"new_friend_rels": new_friend_rels})

@app.route('/register/', methods=['POST'])
def register():
  req = request.json["input"]
  hashedPassword = Password.hash(req["password"])
  register_user_req = fetchGraphQL(CREATE_USER, {
    "password": hashedPassword,
    "phone_number": req["phone_number"],
    "username": req["username"]
  })
  try:
    if (register_user_req["errors"]):
      return jsonify({"message": register_user_req["errors"][0]["message"]})
  except:
    pass
  register_user_req = register_user_req["data"]["insert_user"]["returning"][0]
  add_friend_rels_from_contacts(register_user_req["id"], req["contacts_phone_numbers"])
  return jsonify({"user_id": register_user_req["id"]})

@app.route('/login/', methods=['POST'])
def login():
  req = request.json["input"]

  user_response = fetchGraphQL(FIND_USER_BY_USERNAME, {
    "username": req["username"]
  })
  user = user_response["data"]["user"][0]
  try:
    Password.verify(user["password"], req["password"])
    # MISSING JWT AUTHENTICATION AND PASSWORD UPDATING (https://hasura.io/docs/latest/graphql/core/actions/codegen/python-flask.html)
    return jsonify({"user_id": user["id"]})
  except:
    return jsonify({"message": "Invalid username or password"})

@app.route('/scrape_item/', methods=['POST'])
def scrape_item():
  req = request.json["input"]
  features = scrape_features(req["item_name"])
  create_item_res = fetchGraphQL(CREATE_ITEM, {
    "list_id": req["list_id"],
    "name": req["item_name"],
    "item_url": features["item_url"],
    "image_url": features["image_url"],
    "price": features["price"]
  })
  item_id = create_item_res["data"]["insert_item"]["returning"][0]["id"]
  return jsonify({"item_id": item_id})