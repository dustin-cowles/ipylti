import json
import logging
import os

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, send_from_directory
from flask_caching import Cache
from pylti1p3.contrib.flask import (FlaskCacheDataStorage, FlaskMessageLaunch,
                                    FlaskOIDCLogin, FlaskRequest)
from pylti1p3.tool_config import ToolConfJsonFile

PAGE_TITLE = 'iPyLTI'

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_file(os.path.join(
    'config', 'flask_config.json'), load=json.load)
cache = Cache(app)

logging.getLogger().setLevel(10)
logging.debug('Flask Config: %s', app.config)


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


def get_tool_conf():
    return ToolConfJsonFile(os.path.join('config', 'tool_config.json'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    flask_request = FlaskRequest()
    target_link_uri = flask_request.get_param('target_link_uri')

    if not target_link_uri:
        raise Exception('Missing target_link_uri')

    return FlaskOIDCLogin(
        request=flask_request,
        tool_config=get_tool_conf(),
        launch_data_storage=get_launch_data_storage()
    ).enable_check_cookies().redirect(target_link_uri)


@app.route('/launch', methods=['POST'])
def launch():
    flask_request = FlaskRequest()

    message_launch = FlaskMessageLaunch(
        request=flask_request,
        tool_config=get_tool_conf(),
        launch_data_storage=get_launch_data_storage()
    )

    launch_data = message_launch.get_launch_data()
    logging.debug('launch_data: %s', launch_data)

    return 'LAUNCHED!'


@app.route('/.well-known/<path:filename>')
def well_known(filename):
    return send_from_directory('well-known', filename, conditional=True)


def export_jwks(tool_conf):
    directory = os.path.join(os.path.dirname(__file__), 'well-known')

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, 'jwks.json'), 'w', encoding='utf8') as file:
        file.write(json.dumps(tool_conf.get_jwks()))


export_jwks(get_tool_conf())
asgi_app = WsgiToAsgi(app)
