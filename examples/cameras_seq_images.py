from kognic.io.client import KognicIOClient
from kognic.io.model.scene.cameras_sequence import CamerasSequence, Frame
from kognic.io.model.scene.metadata.metadata import MetaData, FrameMetaData
from kognic.io.model.scene.resources import Image

# Frames
sensor1 = "RFC01"
sensor2 = "RFC02"

frames = [
    Frame(
        frame_id="1",
        relative_timestamp=0,
        images=[
            # JPG Images in Frame 1
            Image(
                filename="./examples/resources/img_RFC01.jpg",
                sensor_name=sensor1,
            ),
            Image(
                filename="./examples/resources/img_RFC02.jpg",
                sensor_name=sensor2,
            ),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),  # metadata is optional and values are arbitary for this example
    ),
    Frame(
        frame_id="2",
        relative_timestamp=500,
        images=[
            # PNG Images in Frame 2
            Image(
                filename="./examples/resources/img_RFC11.png",
                sensor_name=sensor1,
            ),
            Image(
                filename="./examples/resources/img_RFC12.png",
                sensor_name=sensor2,
            ),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),  # metadata is optional and values are arbitary for this example
    ),
    Frame(
        frame_id="3",
        relative_timestamp=1000,
        images=[
            # WebP VP8 Images in Frame 3
            Image(
                filename="./examples/resources/img_RFC21.webp",
                sensor_name=sensor1,
            ),
            Image(
                filename="./examples/resources/img_RFC22.webp",
                sensor_name=sensor2,
            ),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),
    ),
    Frame(
        frame_id="4",
        relative_timestamp=1500,
        images=[
            # WebP VP8L Images in Frame 4
            Image(
                filename="./examples/resources/img_RFC31.webp",
                sensor_name=sensor1,
            ),
            Image(
                filename="./examples/resources/img_RFC32.webp",
                sensor_name=sensor2,
            ),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),
    ),
    Frame(
        frame_id="5",
        relative_timestamp=2000,
        images=[
            # WebP VP8X Images in Frame 5
            Image(
                filename="./examples/resources/img_RFC41.webp",
                sensor_name=sensor1,
            ),
            Image(
                filename="./examples/resources/img_RFC42.webp",
                sensor_name=sensor2,
            ),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),
    ),
]

# Scene
cameras_sequence = CamerasSequence(
    external_id="<scene_id>",  # specify an id
    frames=frames,
    metadata=MetaData(
        {
            "location-lat": 27.986065,
            "location-long": 86.922623,
            "vehicle_id": "abg",
        }
    ),
)

# Create an input on the Kognic Platform
client = KognicIOClient()

created_input = client.cameras_sequence.create(
    cameras_sequence=cameras_sequence,
    project="<project_id>",  # available via `client.project.get_projects()`
    batch="<batch_id>",  # available via `client.project.get_project_batches(project_id)`
    annotation_types=["<annotation-type>"],  # available via `client.project.get_annotation_types(project_id)`
    dryrun=True,
)

print(created_input)  # displays the scene_uuid
