from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import uuid
from flask import request

app = Flask(__name__)
socketio = SocketIO(app)

users = {}  # store connected users

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = str(uuid.uuid4())[:6]
    users[request.sid] = user_id
    emit('user_joined', {'user': user_id}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = users.pop(request.sid, None)
    if user_id:
        emit('user_left', {'user': user_id}, broadcast=True)

@socketio.on('draw_event')
def handle_draw(data):
    emit('draw_event', data, broadcast=True, include_self=False)

@socketio.on('clear_event')
def handle_clear():
    emit('clear_event', broadcast=True, include_self=False)

@socketio.on('undo_event')
def handle_undo():
    emit('undo_event', broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
