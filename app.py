from flask import Flask

from flask_socketio import SocketIO

from conf.config import Config

# APP INIT
app = Flask(__name__)
app.config.from_object(Config)

# Web Socket INIT
socketio = SocketIO(app)
from chat.websocket_events import handle_connect, handle_message, handle_disconnect

# APP ROUTES
from chat.views import chat

app.register_blueprint(chat, url_prefix='')

if __name__ == '__main__':
    socketio.run(app, debug=True)
