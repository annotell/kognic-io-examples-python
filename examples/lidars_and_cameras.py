from kognic.io.client import KognicIOClient
from kognic.io.model.scene.lidars_and_cameras import Frame, LidarsAndCameras
from kognic.io.model.scene.metadata.metadata import MetaData
from kognic.io.model.scene.resources import Image, PointCloud

# Frame
lidar_sensor1 = "lidar"
cam_sensor1 = "RFC01"
cam_sensor2 = "RFC02"

frame = Frame(
    point_clouds=[
        PointCloud(
            filename="./examples/resources/point_cloud_RFL01.las",
            sensor_name=lidar_sensor1,
        )
    ],
    images=[
        Image(
            filename="./examples/resources/img_RFC01.jpg",
            sensor_name=cam_sensor1,
        ),
        Image(
            filename="./examples/resources/img_RFC02.jpg",
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
# Note: a scene that involves a lidar sensor must have a calibration.
# When creating a calibration, all sensors must match those present on the scene.
# If this is not the case the scene will not be created
# and a validation error will be returned by the Kognic API.
lidars_and_cameras = LidarsAndCameras(
    external_id="<scene_id>",  # specify an id
    frame=frame,
    calibration_id="<calibration_id>",  # available via `client.calibration.get_calibrations()`
    metadata=MetaData(
        **{
            "vehicle_id": "abg",
        }
    ),  # metadata is optional and values are arbitary for this example
)

# Create an input on the Kognic Platform
client = KognicIOClient()

created_input = client.lidars_and_cameras.create(
    lidars_and_cameras=lidars_and_cameras,
    project="<project_id>",  # available via `client.project.get_projects()`
    batch="<batch_id>",  # available via `client.project.get_project_batches(project_id)`
    annotation_types=["<annotation-type>"],  # available via `client.project.get_annotation_types(project_id)`
    dryrun=True,
)
