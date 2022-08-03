"""
Handles the launching of docker containers hosting Jupyter servers.
Currently only one container at a time is supported.

TODO: Support multiple containers.
TODO: Support k8s.
TODO: Support other types of containers i.e. JupyterLab
"""

import logging
import re
from time import sleep

import docker

TOKEN_REGEX = re.compile(r"\?token=(.*)$")
CONTAINER_NAME = "ipylti-nb"


class DockerAgent:
    """
    This class manages the docker client and provides functions for launching containers.

    The client is configured from these ENV variables:
    :DOCKER_HOST: The hostname of the docker daemon.
        :example: DOCKER_HOST=tcp://localhost:2375
        :example: DOCKER_HOST=unix:///var/run/docker.sock
    :DOCKER_CERT_PATH: The path to the docker certificate.
        :example: DOCKER_CERT_PATH=/etc/docker
    :DOCKER_TLS_VERIFY: Whether to verify the docker certificate.
        :example: DOCKER_TLS_VERIFY=1
        :example: DOCKER_TLS_VERIFY=0
    """
    def __init__(self):
        """
        :param: None

        :return: An instance of the DockerAgent class.
        :rtype: DockerAgent
        """

        self.client = docker.from_env()

    def launch_container(self, launch_id):
        """
        Launches a container running an instance of Jupyter notebook.

        :param launch_id: - The unique id of the launch.

        :return: The url including login token for the Jupyter instance.
        :rtype: str
        """
        try:
            # TODO: Find a better way to handle cleanup and support multiple containers.
            self.client.containers.get(CONTAINER_NAME).remove(force=True)
        except Exception: # pylint: disable=broad-except
            pass

        host_name = f"{launch_id[0:12]}.nb.docker"
        container = self.client.containers.run(
            "nb",
            name=CONTAINER_NAME,
            detach=True,
            volumes={self._get_volume_id(launch_id):
                        {"bind": "/notebooks", "mode": "rw"}
                    },
            environment={"VIRTUAL_HOST": host_name, "VIRTUAL_PORT": 8888}
        )

        logging.debug("container: %s", container.status)
        # TODO: Many improvements can be made to this.
        while container.status in ["running", "created"]:
            try:
                logs = container.logs().decode("utf-8")
                token = TOKEN_REGEX.search(logs).group()
                if token:
                    logging.debug("token: %s", token)
                    break
            except AttributeError:
                sleep(2)
                container.reload()
                continue

        return f"http://{host_name}/{token}"

    def _get_volume_id(self, launch_id):
        """
        Finds or creates the volume for the launch.

        :param launch_id: The unique id of the launch.

        :return: The id of the volume.
        :rtype: str
        """
        # TODO: Support cloning from assignment base volume.

        try:
            volume_id = self.client.volumes.get(launch_id).name
        except docker.errors.NotFound:
            volume_id = self.client.volumes.create(name=launch_id).name

        return volume_id
