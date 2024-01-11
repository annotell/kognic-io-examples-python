from kognic.io.client import KognicIOClient
from kognic.io.model.scene.cameras import Cameras, Frame
from kognic.io.model.scene.metadata.metadata import MetaData
from kognic.io.model.scene.resources import Image

# Frame
cam_sensor1 = "RFC01"
cam_sensor2 = "RFC02"

frame = Frame(
    images=[
        Image(
            "./examples/resources/img_RFC01.jpg",
            sensor_name=cam_sensor1,
        ),
        Image(
            "./examples/resources/img_RFC02.jpg",
            sensor_name=cam_sensor2,
        ),
    ],
    metadata=MetaData(
        **{
            "location-lat": 27.986065,
            "location-long": 86.922623,
        }
    ),  # metadata is optional and values are arbitary for this example
)

# Scene
cameras = Cameras(
    external_id="<scene_id>",  # specify an id
    frame=frame,
    metadata=MetaData(
        **{
            "vehicle_id": "abg",
        }
    ),  # metadata is optional and values are arbitary for this example
)

# Create an input on the Kognic Platform
client = KognicIOClient()

created_input = client.cameras.create(
    cameras=cameras,
    project="<project_id>",  # available via `client.project.get_projects()`
    batch="<batch_id>",  # availabel via `client.project.get_project_batches(project_id)`
    annotation_types=["<annotation-type>"],  # available via `client.project.get_annotation_types(project_id)`
    dryrun=True,
)
