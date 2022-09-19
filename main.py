from bottle import route, run, response
import socket
import bottle
import queue
import json

q = queue.Queue()



# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/trashcan/<cmd>')
@enable_cors
def trashcan(cmd):
    print(cmd)
    
    message = {
        'type': cmd
    }
    
    json_string = json.dumps(message)
    q.put(json_string)

    return cmd

@route('/query')
@enable_cors
def query():
    if q.qsize() > 0:
        item = q.get()
        q.task_done()
        return item
    else:
        return '' 

if __name__ == '__main__':
    run(host='0.0.0.0', port=8701)