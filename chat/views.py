import random

from conf.config import rooms
from string import ascii_letters
from flask import request, session, render_template, redirect, url_for, Blueprint

chat = Blueprint('chat', __name__, template_folder='templates')


def generate_room_code(length: int, existing_codes: list[str]) -> str:
    while True:
        code_chars = [random.choice(ascii_letters) for _ in range(length)]
        code = ''.join(code_chars)

        if code not in existing_codes:
            return code


@chat.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)
        if not name:
            return render_template('home.html', error='Необходимо ввести имя!', code=code)
        if create != False:
            room_code = generate_room_code(6, list(rooms.keys()))
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room
        if join != False:
            if not code:
                return render_template('home.html', error="Пожалуйста введите код комнаты", name=name)
            if code not in rooms:
                return render_template('home.html', error="Неправильный код комнаты", name=name)
            room_code = code
        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('chat.room', room_slug=room_code))
    else:
        return render_template('home.html')


@chat.route('/room/<string:room_slug>/')
def room(room_slug):
    room = session.get('room')
    name = session.get('name')
    if name is None or room is None or room not in rooms:
        return redirect(url_for('chat.home'))
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages, room_slug=room)
