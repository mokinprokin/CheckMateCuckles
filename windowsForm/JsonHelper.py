# import json
# def write(new_data,array_name):
#     with open("userData.json", encoding="utf8") as f:
#         data=json.load(f)
#         data[array_name].insert(0,new_data)
#         with open("userData.json","w",encoding="utf8") as output:
#             json.dump(data,output,ensure_ascii=False,indent=2)

# def readData(array_name):
#     with open("userData.json", "r",encoding="utf8") as read_file:
#         data = json.load(read_file)
#         return data[array_name]
    
# class history():
#     def __init__(self,login,header,description,date):
#         self.login=login
#         self.header=header
#         self.description=description
#         self.date=date

# data=[history("liliput","xxx","ccc","000"),history("liliput1","xxx1","ccc1","0001")]
# print(data[0].login)

