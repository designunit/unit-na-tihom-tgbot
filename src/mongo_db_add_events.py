from mongo_ops import insert_events, get_events_by_user_time, connect
import all_events


insert_events(all_events.all_events)



