FIND_USERS = """
query MyQuery($phone_numbers: [String!] = "") {
  user(where: {phone_number: {_in: $phone_numbers}}) {
    phone_number
  }
}
"""
# {
#   "phone_numbers": ["+17865557297", "+19545557297"]
# }

CREATE_FRIEND_REL = """
mutation MyMutation($user_first: String! = "", $user_second: String! = "", $type: String = "friends") {
  insert_friend_rel(objects: {user_second: $user_second, type: $type, user_first: $user_first}) {
    returning {
      id
    }
  }
}
"""
# {
#   "user_first": "+17865557297",
#   "user_second": "+19545557297",
# 	"type": "friends"
# }