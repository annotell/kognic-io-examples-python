from pathlib import Path
from uuid import uuid4

from kognic.io.client import KognicIOClient
from kognic.io.model.scene.cameras import Cameras, Frame
from kognic.io.model.scene.metadata.metadata import MetaData
from kognic.io.model.scene.resources import Image

# Create a frame
base_dir = Path(__file__).parent.absolute()
frame = Frame(
    images=[
        Image(
            filename=str(base_dir) + "/resources/img_RFC01.jpg",
            sensor_name="RFC01",
        ),
        Image(
            filename=str(base_dir) + "/resources/img_RFC02.jpg",
            sensor_name="RFC02",
        ),
    ],
)

# Create a scene
scene_cameras = Cameras(
    external_id=f"cameras-example-{uuid4()}",  # Generate a random uuid for this example
    frame=frame,
    metadata=MetaData(
        **{
            "location-lat": 27.986065,
            "location-long": 86.922623,
            "vehicle_id": "abg",
        }
    ),
)

# Create an input
client = KognicIOClient()
project = "<project_id>"  # available via `client.project.get_projects()`
batch = "<batch_id>"  # availabel via `client.project.get_project_batches(project_id)`
annotation_types = ["<annotation-type>"]  # available via `client.project.get_annotation_types(project_id)`

created_input = client.cameras.create(
    scene_cameras,
    project=project,
    batch=batch,
    annotation_types=annotation_types,
    dryrun=True,
)
