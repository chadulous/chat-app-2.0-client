import socketio
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from getpass import getpass


def obscure(data) -> bytes:
    return b64e(zlib.compress(data, 9))


import signal


def interrupted(signum, frame):
    print("Timeout!")


signal.signal(signal.SIGALRM, interrupted)
signal.alarm(5)
signal.alarm(0)


def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))


sio = socketio.Client()


@sio.on('connect')
def conhandle():
    print(f'''{sio.connection_headers['username']}: ''', end='')


@sio.on('msg')
def mesghandle(data):
    if data['user'] != sio.connection_headers['username']:
        print(f'''\n{data['user']}: {data['msg']} ''',
              end=f'''\n{sio.connection_headers['username']}: ''')
    else:
        print(f'''{sio.connection_headers['username']}: ''', end='')


@sio.on('getback')
def getback():
    msg = input('')
    sio.emit('send', msg)


@sio.on('inc')
def passinc():
    print('password incorrect')
    exit()


@sio.on('alrx')
def already():
    print('that name already exists')
    exit()


new = input('Signup? (y/n): ')
if new.lower() == 'y':
    newv = 'true'
elif new.lower() == 'n':
    newv = 'false'
else:
    exit()
un = input('Username: ')
pw = obscure(bytes(str(getpass('Password: ')), 'utf-8'))
sio.connect('https://video-streamer-1.maverickdev55.repl.co', {
    'username': un,
    'password': pw,
    'new': newv
})
