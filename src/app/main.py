"""
The main entry point for the application server.
This implements the Flask application server which manages
LTI authentication and launches Jupyter notebook servers.
"""
import logging

from flask import Markup, render_template, send_from_directory
from pylti1p3.contrib.flask import (FlaskCookieService, FlaskMessageLaunch,
                                    FlaskOIDCLogin, FlaskRequest)

from constants import ADMIN_ROLE, INSTRUCTOR_ROLE
from grading import submit_asignment
from helpers import (get_docker_agent, get_message_launch, get_tool_conf,
                     setup_app)

app, asgi_app, launch_data_storage = setup_app(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles login request from tool consumer."""

    flask_request = FlaskRequest()
    target_link_uri = flask_request.get_param("target_link_uri")

    if not target_link_uri:
        raise Exception("Missing target_link_uri")

    return FlaskOIDCLogin(
        request=flask_request,
        tool_config=get_tool_conf(),
        launch_data_storage=launch_data_storage,
        cookie_service=FlaskCookieService(flask_request)
    ).enable_check_cookies().redirect(target_link_uri)


@app.route("/launch", methods=["POST"])
def launch():
    """
    Handles launches from tool consumer.

    :params: None

    :return: A Flask response object redirecting to the launch page.
    :rtype: flask.Response
    """

    flask_request = FlaskRequest()

    message_launch = FlaskMessageLaunch(
        request=flask_request,
        tool_config=get_tool_conf(),
        launch_data_storage=launch_data_storage
    )

    # Cache the public key for the LMS.
    message_launch.set_public_key_caching(launch_data_storage, cache_lifetime=7200)

    launch_id = message_launch.get_launch_id()
    launch_data = message_launch.get_launch_data()
    logging.debug("launch_id: %s\nlaunch_data: %s", launch_id, launch_data)

    user_id = launch_data["https://purl.imsglobal.org/spec/lti/claim/lti1p1"]["user_id"]
    roles = launch_data["https://purl.imsglobal.org/spec/lti/claim/roles"]
    context_id = launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["id"]
    resource_id = launch_data["https://purl.imsglobal.org/spec/lti/claim/resource_link"]["id"]
    title = Markup(
        launch_data["https://purl.imsglobal.org/spec/lti/claim/resource_link"]["title"]
    ).striptags()
    description = Markup(
        launch_data["https://purl.imsglobal.org/spec/lti/claim/resource_link"]["description"]
    ).striptags()

    if all([context_id, user_id, resource_id, roles]):
        build = INSTRUCTOR_ROLE in roles or ADMIN_ROLE in roles
        logging.debug("building assignment? %s", build)
        launch_url = get_docker_agent().launch_container(launch_id, resource_id, build)
        logging.debug("launch_url: %s", launch_url)
    else:
        raise Exception("Missing launch params")
    if not launch_url:
        raise Exception("Missing launch url")

    return render_template(
        "launch.html",
        launch_url=launch_url,
        title=title,
        description=description,
        launch_id=launch_id,
        build=build
    )


@app.route("/submit/<launch_id>", methods=["GET", "POST"])
def submit(launch_id):
    """
    Submits the assignment to the LMS.

    :param launch_id: The launch id.

    :returns: None
    """
    message_launch = get_message_launch(launch_id, FlaskRequest(), launch_data_storage)
    if message_launch.has_ags():
        try:
            submit_asignment(message_launch)
            success = True
        except Exception as err:  # pylint: disable=broad-except
            logging.error("Error submitting assignment: %s", err)
            success = False

    return render_template("submit.html", success=success)


@app.route("/.well-known/<path:filename>")
def well_known(filename):
    """
    Serves files from the well-known directory to aid in tool consumer configuration.

    :param filename: The filename to serve.

    :return: The file as a Flask response object.
    :rtype: flask.Response
    """

    return send_from_directory("well-known", filename, conditional=True)
