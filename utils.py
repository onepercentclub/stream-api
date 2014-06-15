def append_value(lst, item, keyPath):
    try:
        lst.append(path_value(item, keyPath, False))
    except:
        pass

def path_value(item, keyPath, handleExcept=True):
    keys = keyPath.split('.')
    value = item.copy()    
    try:
        for key in keys:
            value = value[key]
        return value
    except KeyError as e:
    	if handleExcept:
        	return None
        else:
        	raise e