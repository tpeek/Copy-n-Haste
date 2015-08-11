from gevent import monkey
from socketio.server import SocketIOServer
import django.core.handlers.wsgi
import os
import sys

monkey.patch_all()

try:
    import settings
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

PORT = 9000

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

app = django.core.handlers.wsgi.WSGIHandler()

sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))

if __name__ == '__main__':
    print 'Listening on http://127.0.0.1:%s and on port 10843 (flash policy server)' % PORT
    SocketIOServer(('', PORT), app, resource="socket.io").serve_forever()


#namespace

var socket = io.connect("/chat");

from socketio.namespace import BaseNamespace
from socketio import socketio_manage

class ChatNamespace(BaseNamespace):

    def on_user_msg(self, msg):
        self.emit('user_msg', msg)

def socketio_service(request):
    socketio_manage(request.environ, {'/chat': ChatNamespace}, request)
    return 'out'

import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        self.room = room
        self.join(room)
        return True

    def on_nickname(self, nickname):
        self.log('Nickname: {0}'.format(nickname))
        self.nicknames.append(nickname)
        self.socket.session['nickname'] = nickname
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        return True, nickname

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        nickname = self.socket.session['nickname']
        self.nicknames.remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
            self.socket.session['nickname'], msg)
        return True

#chat

var socket = io.connect("/chat");

socket.on('connect', function () {
    $('#chat').addClass('connected');
    socket.emit('join', window.room);
});

socket.on('announcement', function (msg) {
    $('#lines').append($('<p>').append($('<em>').text(msg)));
});

socket.on('nicknames', function (nicknames) {
    console.log("nicknames: " + nicknames);
    $('#nicknames').empty().append($('<span>Online: </span>'));
    for (var i in nicknames) {
        $('#nicknames').append($('<b>').text(nicknames[i]));
    }
});

socket.on('msg_to_room', message);

socket.on('reconnect', function () {
    $('#lines').remove();
    message('System', 'Reconnected to the server');
});

socket.on('reconnecting', function () {
    message('System', 'Attempting to re-connect to the server');
});

socket.on('error', function (e) {
    message('System', e ? e : 'A unknown error occurred');
});

function message (from, msg) {
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}

// DOM manipulation
$(function () {
    $('#set-nickname').submit(function (ev) {
        socket.emit('nickname', $('#nick').val(), function (set) {
            if (set) {
                clear();
                return $('#chat').addClass('nickname-set');
            }
            $('#nickname-err').css('visibility', 'visible');
        });
        return false;
    });

    $('#send-message').submit(function () {
        //message('me', "Fake it first: " + $('#message').val());
        socket.emit('user message', $('#message').val());
        clear();
        $('#lines').get(0).scrollTop = 10000000;
        return false;
    });

    function clear () {
        $('#message').val('').focus();
    }
});

