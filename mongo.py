import datetime
from pymongo import MongoClient

MONGO_URL = 'mongodb://localhost:27017/'
DATABASE_NAME = 'stream'

#connection = MongoClient(MONGO_URL)
#db = connection[DATABASE_NAME]

"""
Typical message Structure

{"created": datetime.datetime.utcnow(),
 "text": "The message we want to deliver",
 "tags": ["PULL REQUEST", "FAIL"],
 "source": "Github" 
}

"""

# this internal function return the database connection
def __get_db():
    connection = MongoClient(MONGO_URL)
    db = connection[DATABASE_NAME]
    return db

# this function returns the messages collection
def get_messages_collection():
    db = __get_db()
    return db.messages

# This function store a message into the collection messages
def post_message(message):
    if not get_messages_collection().find_one({'remote_id': message['remote_id']}):
        message['created'] = datetime.datetime.utcnow() 
        messages = get_messages_collection()
        message_id = messages.insert(message)
        return message_id

def to_string(message):
    return message['text']
