import logging
import re
from time import sleep

import docker

TOKEN_REGEX = re.compile(r"\?token=(.*)$")
CONTAINER_NAME = "ipylti-nb"


class DockerAgent:
    def __init__(self):
        self.client = docker.from_env()

    def launch_container(self, launch_id):
        try:
            self.client.containers.get(CONTAINER_NAME).remove(force=True)
        except Exception:
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
        try:
            volume_id = self.client.volumes.get(launch_id).name
        except docker.errors.NotFound:
            volume_id = self.client.volumes.create(name=launch_id).name

        return volume_id
