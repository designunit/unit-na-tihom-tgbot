import datetime
import gridfs


from mongo_ops import insert_event, get_events_by_user_time, connect


# event_sample1 = {
#     "time_start": datetime.datetime(2023, 8, 12, 10, 30),
#     "time_end": datetime.datetime(2023, 8, 12, 10, 50),
#     "Name": "Открытие лектория",
#     "Mark": "Брифинг",
#     "Speaker": [
#         {"name": "Лиза Владимировна", "status": "Куратор резиденции"},
#         {"name": "Владимир Петросян", "status": "Куратор резиденции"},
#     ],
# }


# event_sample2 = {
#     "time_start": datetime.datetime(2023, 8, 11, 14, 00),
#     "time_end": datetime.datetime(2023, 8, 11, 16, 00),
#     "Name": "LE BEAU SERGE",
# }


# insert_event(event_sample1)
# insert_event(event_sample2)
# test_time = datetime.datetime(2023, 8, 11, 15, 00)
# test = get_events_by_user_time(test_time)

# for i in test:
#     print(i)



### ADD FILE

conn = connect()
db = conn['tixiy_bot_db']
fs = gridfs.GridFS(db)

name = 'music.jpg'
file_location = '/home/danila/Documents/unit_na_tixom_files/' + name

with open(file_location, 'rb') as file:
    data = file.read()

fs.put(data, filename=name)
print('upload completed')

# name2 = 'test123.jpj'
# new_data = db.fs.files.find_one({"filename": name})
# my_id = new_data['_id']
# output_data = fs.get(my_id).read()
# download_location = '/home/danila/Downloads/' + name2
# with open(download_location, 'wb') as file:
#     file.write(output_data) 
# print("download completed")