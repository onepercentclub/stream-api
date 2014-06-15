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
def post_message(message, uniqueField=''):
    messages = get_messages_collection()
    # If uniqueField set then only post if uniqueField doesn't exist in db
    if len(uniqueField) and message.has_key(uniqueField) and messages.find_one({uniqueField: message[uniqueField]}):
        return False

    message['created'] = datetime.datetime.utcnow()
    message_id = messages.insert(message)
    return True

def to_string(message):
    return message['text']
