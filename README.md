EXAMPLE
=======
```
Console A (server)
$> python
>>> from kommons import node
>>> node.listen(56000)

Console B (client)
$> python
>>> from kommons import node
>>> import socket
>>> w = node.open((socket.gethostname(), 56000))
>>> node.synch(w, "[1, 2, 3, 4, 54, 6]")
[1, 2, 3, 4, 54, 6]
>>> node.synch(w, "{'k1': "value1", 'k2': "value2"}")
{'k1': "value1", 'k2': "value2"}
```
