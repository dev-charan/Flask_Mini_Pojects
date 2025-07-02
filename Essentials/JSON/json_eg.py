# import json

# data = {
#     "name": "Charan",
#     "age": 22,
#     "is_active": True
# }
# # to json
# json_string = json.dumps(data)
# print(json_string)

# #json to pyhton

# pyhton_dict = json.loads(json_string)
# print(pyhton_dict["name"])

import json

data = {"name": "Charan", "active": True}

with open("data.json", "w") as f:
    json.dump(data, f)  # dump = dumps + write
