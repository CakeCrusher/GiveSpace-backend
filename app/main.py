from flask import Flask, jsonify, request
import requests
import os

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