from __future__ import absolute_import

from pathlib import Path
from typing import Optional
from uuid import uuid4

import kognic.io.model.scene.cameras as CM
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import CreateSceneResponse, Image

base_dir = Path(__file__).parent.absolute()


def run(client: KognicIOClient, dryrun: bool = True, external_id: Optional[str] = None, **kwargs) -> Optional[CreateSceneResponse]:
    print("Creating Cameras Scene...")

    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"}

    scene = CM.Cameras(
        external_id=external_id or f"cameras-example-{uuid4()}",
        frame=CM.Frame(
            images=[
                Image(
                    filename=str(base_dir) + "/resources/img_RFC01.jpg",
                    sensor_name="RFC01",
                ),
                Image(
                    filename=str(base_dir) + "/resources/img_RFC02.jpg",
                    sensor_name="RFC02",
                ),
            ]
        ),
        metadata=metadata,
    )

    # Create scene
    return client.cameras.create(scene, dryrun=dryrun, **kwargs)


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "Project-identifier"

    run(client, project=project)
