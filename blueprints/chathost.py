from flask import Blueprint, render_template, session, request
from flask_socketio import SocketIO, join_room, leave_room, send

socketio = SocketIO()

chathost = Blueprint('chathost', __name__)

# Route to load chat interface
@chathost.route("/chat")
def chat():
    return render_template("chathost.html")

# Handle new messages
@socketio.on('message')
def handle_message(data):
    room = session.get('room')
    send({'msg': data['msg'], 'username': session.get('username')}, room=room)

# Handle user joining a room
@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = data['room']
    join_room(room)
    send({'msg': f"{username} has entered the room."}, room=room)

# Handle user leaving a room
@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = data['room']
    leave_room(room)
    send({'msg': f"{username} has left the room."}, room=room)
