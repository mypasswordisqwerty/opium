from flup.server.fcgi import WSGIServer
import json
import threading

_PIPE = None
_LOCK = threading.Lock()


def handler(environ, start_response):
    global _PIPE, _LOCK
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    pack = environ['wsgi.input'].read(request_body_size)
    data = json.loads(pack)
    _LOCK.acquire()
    try:
        _PIPE.send(data)
        obj = _PIPE.recv()
    except Exception as e:
        print(f"Exception in pipe communication: {e}")
    _LOCK.release()
    resp = json.dumps(obj)
    status = '200 OK'
    response_headers = [('Content-type', 'application/json'), ('Content-Length', str(len(resp)))]
    start_response(status, response_headers)
    return resp


def serve(pipe, port):
    global _PIPE
    _PIPE = pipe
    try:
        WSGIServer(handler, bindAddress=('127.0.0.1', port)).run()
    except Exception as e:
        print(f"Error: {e}")
    _PIPE.close()
