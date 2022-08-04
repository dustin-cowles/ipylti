"""
Handles the launching of docker containers hosting Jupyter servers.
Currently only one container at a time is supported.

TODO: Support multiple containers.
TODO: Support k8s.
TODO: Support other types of containers i.e. JupyterLab
"""
import logging
from time import sleep

import docker

from constants import CONTAINER_NAME, JUPYTER_TOKEN_REGEX, JUPYTER_IMAGE

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

    def launch_container(self, launch_id, resource_id, build):
        """
        Launches a container running an instance of Jupyter notebook.

        If build == True, the resource_id will be used to generate the base
        volume which will be used when creating new student volumes.

        :param launch_id: The unique id of the launch.
        :param resource_id: The unique id of the resource/assignment. 
        :param build: Should be True for Instructor launches, False otherwise.

        :return: The url including login token for the Jupyter instance.
        :rtype: str
        """
        try:
            # We currently only support a single container at a time.
            self.client.containers.get(CONTAINER_NAME).remove(force=True)
        except docker.errors.NotFound:
            pass

        host_name = f"{launch_id[0:12]}.nb.docker"
        logging.debug("Launching container %s", host_name)
        container = self.client.containers.run(
            JUPYTER_IMAGE,
            name=CONTAINER_NAME,
            detach=True,
            volumes={self._get_volume_id(launch_id, resource_id, build):
                        {"bind": "/jupyter-workspace", "mode": "rw"}
                    },
            environment={"VIRTUAL_HOST": host_name, "VIRTUAL_PORT": 8888}
        )

        logging.debug("container: %s", container.status)
        # This should probably have a timeout
        for line in container.logs(stream=True):
            match = JUPYTER_TOKEN_REGEX.search(line.decode("utf-8"))
            if match:
                token = match.group()
                logging.debug("token: %s", token)
                break

        return f"http://{host_name}/{token}"

    def _get_volume_id(self, launch_id, resource_id, build):
        """
        Finds or creates the volume for the launch.

        If build == True, the resource_id will be used to name the volume.

        If build == False and a new volume is created, the resource_id will
        be used to find a base volume to clone contents from.

        :param launch_id: The unique id of the launch.
        :param resource_id: The unique id of the resource/assignment.
        :param build: Should be True for Instructor launches, False otherwise.

        :return: The id of the volume.
        :rtype: str
        """
        # TODO: Support cloning from assignment base volume.

        volume_name = resource_id if build else launch_id

        try:
            volume_id = self.client.volumes.get(volume_name).name
        except docker.errors.NotFound:
            volume_id = self.client.volumes.create(name=volume_name).name
            if not build: # A student launching for first time
                if self.client.volumes.get(resource_id): # A base volume exists
                    # Clone the resource_id (base) volume into the student volume.
                    self._clone_volume(resource_id, volume_id)

        return volume_id

    def _clone_volume(self, source_volume_id, destination_volume_id):
        """
        Clones the source volume to the destination volume.

        :param source_volume_id: The id of the source volume.
        :param destination_volume_id: The id of the destination volume.

        :return: None
        """
        logging.debug("Cloning %s into %s", source_volume_id, destination_volume_id)
        container_logs = self.client.containers.run(
            "alpine",
            ["sh", "-c", "cp -R /source/* /destination/ && chown -R 1000:1000 /destination"],
            volumes={
                source_volume_id: {"bind": "/source", "mode": "ro"},
                destination_volume_id: {"bind": "/destination", "mode": "rw"}})
        logging.debug("START clone container logs")
        logging.debug(container_logs)
        logging.debug("END clone container logs")
