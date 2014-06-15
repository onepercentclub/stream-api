import cherrypy
import mongo

from utils import append_value, path_value

class Root:
    def index(self):
	    return "Hello, world!"
    index.exposed = True

class Messages(object):

    def GET(self, source=None):
	
	messages = mongo.get_messages_collection()
	result = messages.find_one({"source": source})
	
	if source == None:
	    result = "Here you have all the messages: \n"
	    for message in messages.find():
	    	#result += mongo.to_string(message)
		result = message['text']
		result += "\n ====== \n"
	
	elif result:
	    result = mongo.to_string(message)
	
	else:
	    result = "No messages with the specified ID %s" %source

	return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def POST(self):
        result = mongo.post_message(cherrypy.request.json)
        return "Success"    

    exposed = True

class Donations(object):

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def POST(self):
        json = cherrypy.request.json
        count = 0
        for item in json['results']:
            # import ipdb; ipdb.set_trace()
            message = {}

            if item['user']:
                message['title'] = item['user']['full_name']
            else:
			    message['title'] = "Anonymous Donator"
            message['text'] = item['project']['title']
            message['remote_id'] = item['id']
            message['source'] = 'onepercentsite'
            message['type'] = 'donations'

            # Populate the tags 
            tags = []
            append_value(tags, item, 'project.country.name')
            message['tags'] = tags

            # save the raw message
            message['raw'] = item
            result = mongo.post_message(message)

            if result:
                count += 1

        if count > 0:
            return "Created {0} records.".format(count)
        else:
            return "No records created."
    exposed = True


if __name__ == '__main__':
    cherrypy.tree.mount(
	    Messages(), '/api/messages/',
	    {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
	)
    cherrypy.tree.mount(
	    Donations(), '/api/donations/',
	    {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
	)
    cherrypy.engine.start()
    cherrypy.engine.block()

