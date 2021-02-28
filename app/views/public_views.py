from flask import Blueprint, render_template
from flask import redirect, request, render_template, url_for
from flask_security import login_required, current_user
from bson.json_util import dumps
from flask_socketio import SocketIO
from db import *
public_blueprint = Blueprint('public', __name__, template_folder='templates', url_prefix="/user")
socketio = SocketIO()

@public_blueprint.route('/')
def home_page():
    rooms = get_rooms_for_user(current_user.username)
    return render_template('public/home_page.html',rooms=rooms)

@public_blueprint.route('/test')
def test_page():
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
    return render_template('public/test.html', rooms=rooms)

@public_blueprint.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for('view_room', room_id=room_id))
        else:
            message = "Failed to create room"
    return render_template('chat/create_room.html', message=message)


@public_blueprint.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room edited successfully'
            room_members_str = ",".join(new_members)
        return render_template('chat/edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404


@public_blueprint.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    rooms = get_rooms_for_user(current_user.username)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('public/view_room.html',rooms=rooms, username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404


@public_blueprint.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404
