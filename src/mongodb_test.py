import datetime

from mongo_ops import insert_event, get_events_by_user_time


event_sample1 = {
    "time_start": datetime.datetime(2023, 8, 12, 10, 30),
    "time_end": datetime.datetime(2023, 8, 12, 10, 50),
    "Name": "Открытие лектория",
    "Mark": "Брифинг",
    "Speaker": [{"name": "Лиза Владимировна", "status": "Куратор резиденции"},
                {"name": "Владимир Петросян", "status": "Куратор резиденции"}]
}


event_sample2 = {
    "time_start": datetime.datetime(2023, 8, 11, 14, 00),
    "time_end": datetime.datetime(2023, 8, 11, 16, 00),
    "Name": "LE BEAU SERGE"
}


insert_event(event_sample1)
insert_event(event_sample2)
test_time = datetime.datetime(2023, 8, 11, 15, 00)
test = get_events_by_user_time(test_time)

for i in test:
    print(i)
