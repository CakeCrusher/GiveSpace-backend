import os
import requests

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