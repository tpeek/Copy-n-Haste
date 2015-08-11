#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import sys
import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.bind(server_address)

server.listen(5)

message_queues = {}

TIMEOUT = 1000

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

poller = select.poll()
poller.register(server, READ_ONLY)

fd_to_socket = {server.fileno(): server}

while True:

    print >>sys.stderr, '\nwaiting for the next event'
    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        s = fd_to_socket[fd]
        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                connection, client_address = s.accept()
                print >>sys.stderr, 'new connection from', client_address
                connection.setblocking(0)
                fd_to_socket[connection.fileno()] = connection
                poller.register(connection, READ_ONLY)

                message_queues[connection] = Queue.Queue()

            else:
                data = s.recv(1024)
                if data:
                    print >>sys.stderr, 'received "%s" from %s' % (
                        data,
                        s.getpeername()
                    )
                    message_queues[s].put(data)
                    poller.modify(s, READ_WRITE)

                else:
                    print >>sys.stderr, 'closing', client_address, 'after reading no data'
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]

        elif flag & select.POLLHUP:
            print >>sys.stderr, 'closing', client_address, 'after receiving HUP'
            poller.unregister(s)
            s.close()

        elif flag & select.POLLOUT:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
                poller.modify(s, READ_ONLY)
            else:
                print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
                s.send(next_msg)

        elif flag & select.POLLERR:
            print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
            poller.unregister(s)
            s.close()
            del message_queues[s]
