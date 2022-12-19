# xrpc

Example library that implements RPCs using HTTP.  

### Server Example:
```python
import xrpc

xrpc.server.run(8080)

@xrpc.handler
def test(request: xrpc.Request) -> xrpc.Response:
    return xrpc.Response.ok({'msg': 'OK', 'sender': str(request.sender)})

xrpc.server.join()
```

### Call Example:
```python
import xrpc

response = xrpc.call('test', 'localhost', 8080)
print(response.code, response.data)
```
