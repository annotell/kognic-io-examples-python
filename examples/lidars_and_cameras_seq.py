from kognic.io.client import KognicIOClient
from kognic.io.model.scene.lidars_and_cameras_sequence import (
    Frame,
    LidarsAndCamerasSequence,
)
from kognic.io.model.scene.metadata.metadata import FrameMetaData, MetaData
from kognic.io.model.scene.resources import Image, PointCloud

# Frames
lidar_sensor1 = "lidar"
cam_sensor1 = "RFC01"
cam_sensor2 = "RFC02"
frames = [
    Frame(
        frame_id="1",
        relative_timestamp=0,
        point_clouds=[
            PointCloud(filename="./examples/resources/point_cloud_RFL01.las", sensor_name=lidar_sensor1),
        ],
        images=[
            Image(filename="./examples/resources/img_RFC01.jpg", sensor_name=cam_sensor1),
            Image(filename="./examples/resources/img_RFC02.jpg", sensor_name=cam_sensor2),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),  # metadata is optional and values are arbitary for this example
    ),
    Frame(
        frame_id="2",
        relative_timestamp=100,
        point_clouds=[
            PointCloud(filename="./examples/resources/point_cloud_RFL02.las", sensor_name=lidar_sensor1),
        ],
        images=[
            Image(filename="./examples/resources/img_RFC11.jpg", sensor_name=cam_sensor1),
            Image(filename="./examples/resources/img_RFC12.jpg", sensor_name=cam_sensor2),
        ],
        metadata=FrameMetaData(**{"dut_status": "active"}),  # metadata is optional and values are arbitary for this example
    ),
]

# Scene
# Note: a scene that involves a lidar sensor must have a calibration.
# When creating a calibration, all sensors must match those present on the scene.
# If this is not the case the scene will not be created
# and a validation error will be returned by the Kognic API.
lidars_and_cameras_sequence = LidarsAndCamerasSequence(
    external_id="<scene_id>",
    frames=frames,
    calibration_id="<calibration_id>",  # available via `client.calibration.get_calibrations()`
    metadata=MetaData(
        **{
            "location-lat": 27.986065,
            "location-long": 86.922623,
            "vehicle_id": "abg",
        }
    ),  # metadata is optional and values are arbitary for this example
)


# Create an input on the Kognic Platform
client = KognicIOClient()

created_input = client.lidars_and_cameras_sequence.create(
    lidars_and_cameras_sequence=lidars_and_cameras_sequence,
    project="<project_id>",  # available via `client.project.get_projects()`
    batch="<batch_id>",  # available via `client.project.get_project_batches(project_id)`
    annotation_types=["<annotation-type>"],  # available via `client.project.get_annotation_types(project_id)`
    dryrun=True,
)

print(created_input)  # displays the scene_uuid
