import socket, select, thread

def _poll(sd, eo):
    connections = {}
    def serve(event):
        ld, e = event
        # in the event of receiving a connection/msg
        if e & select.EPOLLIN:
            if (ld is sd.fileno()):
                fd, addr = sd.accept()
                fd.setblocking(False)
                eo.register(fd.fileno(), select.EPOLLIN)
                connections[fd.fileno()] = fd
                open_handler()
            else:
                # recv complete message
                # TODO: change this to infinite message size
                msg = connections[ld].recv(8192)
                    
                # in the event of closing a connection (msg '' and event select.EPOLLIN)
                if msg == '':
                    eo.unregister(ld)
                    connections[ld].close()
                    del connections[ld]
                    close_handler()
                else:
                    # execute synch/asynch handler with the recvd message as the argument
                    msg = eval(msg)
                    if msg['type'] == 'synch':
                        ret = synch_handler(msg['msg'])
                        connections[ld].send(str(ret))
                    else:
                        asynch_handler(msg['msg'])
                    
    while(True):
        events = eo.poll(0)
        # map(lambda e: serve, events)
        # TODO: use the above map properly instead of list comprehension
        # TODO: the below error handling needs to be more informative, this is just so that the thread doesn't fail. 
        try:
            [serve(e) for e in events]
        except Exception as e:
            print e

# Default open/close and synch/asynch handlers (server)
def open_handler():
    print "new connection"

def synch_handler(msg):
    return eval(msg)

def asynch_handler(msg):
    eval(msg)

def close_handler():
    print "close handler"
    

# listens on this port for connections (server)
# TODO: sd needs to be a singleton object, figure out how to do it in functional way
def listen(port):
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sd.setblocking(0)
    sd.bind((socket.gethostname(),port))
    # number of concurrent connections
    sd.listen(4000)

    # launch a thread polling and accepting connections and triggering registered handlers for the respective calls.
    eo = select.epoll()
    eo.register(sd.fileno(), select.EPOLLIN)
    thread.start_new(_poll, (sd, eo))
    return sd

# returns a cd (client)
def open(hp):
    cd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cd.connect(hp)
    return cd

# asynchronous tcp send msg to sd (client) 
def asynch(cd, m):
    cd.setblocking(False)
    msg = {}
    msg['type'] = 'asynch'
    msg['msg'] = m
    cd.send(str(msg))

# synchronous tcp send msg to sd (client)
def synch(cd, m):
    cd.setblocking(True)
    msg = {}
    msg['type'] = 'synch'
    msg['msg'] = m
    cd.send(str(msg))
    ret = cd.recv(8192)
    return(eval(ret))
