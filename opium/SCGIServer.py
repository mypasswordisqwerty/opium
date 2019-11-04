from scgi.scgi_server import SCGIHandler, SCGIServer
import json

_PIPE = None


class Handler(SCGIHandler):
    def produce(self, env, bodysize, input, output):
        global _PIPE
        pack = input.read(bodysize)
        data = json.loads(pack)
        _PIPE.send(data)
        resp = json.dumps(_PIPE.recv())
        output.write("Content-Type: application/json\r\n")
        output.write("Content-Length: "+str(len(resp))+"\r\n\r\n")
        output.write(resp)


def serve(pipe, port):
    global _PIPE
    _PIPE = pipe
    try:
        SCGIServer(handler_class=Handler, host="127.0.0.1", port=port).serve()
    except:
        pass
    _PIPE.close()
