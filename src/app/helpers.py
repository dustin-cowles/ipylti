""" Helper functions used by main application """
import json
import logging
import os

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, Markup
from flask_caching import Cache
from pylti1p3.contrib.flask import FlaskCacheDataStorage, FlaskMessageLaunch
from pylti1p3.tool_config import ToolConfJsonFile

from docker_agent import DockerAgent


def setup_app(app_name, template_folder="templates", static_folder="static"):
    """
    Creates a Flask app and configures the Flask app,
    asgi app, logging, and exports the jwks file.

    :param app: The Flask application instance name.

    :return: The Flask application.
    :rtype: Flask application instance.
    :return: The asgi application.
    :rtype: Asgi application instance.
    """
    configure_logging()
    export_jwks(get_tool_conf())
    app = Flask(app_name, template_folder=template_folder, static_folder=static_folder)
    app.config.from_file(os.path.join(
        "config", "flask_config.json"), load=json.load)
    logging.debug("Flask Config: %s", app.config)
    asgi_app = WsgiToAsgi(app)
    return app, asgi_app, get_launch_data_storage(app)


def get_docker_agent():
    """
    Returns the docker agent.

    :params: None

    :return: The docker agent.
    :rtype: DockerAgent
    """

    return DockerAgent()


def configure_logging():
    """
    Configures the Python logging module.

    :params: None

    :return: None
    """
    logging.getLogger().setLevel(10)


def get_launch_data_storage(app):
    """
    Returns the launch data storage.

    :params: None

    :return: The launch data storage.
    :rtype: FlaskCacheDataStorage
    """

    cache = Cache(app)
    return FlaskCacheDataStorage(cache)


def get_tool_conf():
    """
    Loads and returns the tool configuration.

    :params: None

    :return: The tool configuration.
    :rtype: ToolConfJsonFile
    """

    return ToolConfJsonFile(os.path.join("config", "tool_config.json"))


def get_message_launch(launch_id, request, launch_data_storage):
    """
    Retrieves the message_launch from cache and returns it.

    :param launch_id: The original launch_id.
    :param request: The flask request.

    :returns: The message_launch.
    :rtpes: MessageLaunch
    """
    logging.debug("Getting message_launch from cache")
    logging.debug("Launch ID: %s", launch_id)
    logging.debug("Request: %s", request)
    logging.debug("Launch Data Storage: %s", launch_data_storage)
    return FlaskMessageLaunch.from_cache(
        launch_id, request, get_tool_conf(),
        launch_data_storage=launch_data_storage)


def export_jwks(tool_conf):
    """
    Exports the jwks.json file to the well-known directory.

    :param toolconf: The tool configuration.

    :returns: None
    """

    directory = os.path.join(os.path.dirname(__file__), "well-known")

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, "jwks.json"), "w", encoding="utf8") as file:
        file.write(json.dumps(tool_conf.get_jwks()))
