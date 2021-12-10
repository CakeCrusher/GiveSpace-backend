FIND_USERS = """
query MyQuery($phone_numbers: [String!] = "") {
  user(where: {phone_number: {_in: $phone_numbers}}) {
    id
  }
}
"""
# {
#   "phone_numbers": ["+17865557297", "+19545557297"]
# }

CREATE_FRIEND_REL = """
mutation MyMutation($friend_rels: [friend_rel_insert_input!] = []) {
  insert_friend_rel(objects: $friend_rels) {
    returning {
      id
    }
  }
}
"""
# {
#   "friend_rels": [{"user_first_id": "8549a167-e221-49c6-a87e-272a042d54ee", "user_second_id": "9f42db74-b38e-47f7-afa6-638773ae0c23", "type": "friends"}, {"user_first_id": "9f42db74-b38e-47f7-afa6-638773ae0c23", "user_second_id": "c43952b9-d92c-459a-b3b5-86d9f864abfc", "type": "friends"}]
# }

CONTACTS_TO_FRIENDS = """
mutation MyMutation($contacts_phone_numbers: [String!] = "", $user_id: String = "") {
  contacts_to_friends(contacts_phone_numbers: $contacts_phone_numbers, user_id: $user_id) {
    new_friend_rels
  }
}
"""
# {
#   "user_id": "9f42db74-b38e-47f7-afa6-638773ae0c23",
#   "contacts_phone_numbers": ["+19545557297", "+13335557297"]
# }

CREATE_USER = """
mutation MyMutation($password: String = "", $phone_number: String = "", $username: String = "") {
  insert_user(objects: {password: $password, username: $username, phone_number: $phone_number}) {
    returning {
      id
    }
  }
}
"""
# {
#   "password": "secret",
#   "username": "Krabs",
#   "phone_number": "+17865557297"
# }

REGISTER_USER = """
mutation MyMutation($contacts_phone_numbers: [String!] = "", $password: String = "", $phone_number: String = "", $username: String = "") {
  register(contacts_phone_numbers: $contacts_phone_numbers, password: $password, phone_number: $phone_number, username: $username) {
    user_id
  }
}
"""
# {
#   "password": "secret",
#   "username": "Squid",
#   "phone_number": "+14325557297",
#   "contacts_phone_numbers": ["+17865557297","+13335557297","+12345557297"]
# }

CREATE_ITEM = """
mutation MyMutation($price: Float = 1.5, $name: String = "", $item_url: String = "", $image_url: String = "", $list_id: uuid = "") {
  insert_item(objects: {price: $price, name: $name, item_url: $item_url, image_url: $image_url, list_id: $list_id}) {
    returning {
      id
    }
  }
}
"""
# {
#   "list_id": "656e08e4-2b80-4ff4-9175-15b340ccabd9",
#   "name": "television toshiba",
#   "item_url": "https://www.amazon.com/Toshiba-43-inch-4K-UHD-Smart-Fire-TV/dp/B0924WSBXH/ref=sr_1_2?keywords=television+toshiba&qid=1639085436&sr=8-2",
#   "image_url": "https://m.media-amazon.com/images/I/81QvlthwGRS._AC_UY218_.jpg",
#   "price": 0
# }

