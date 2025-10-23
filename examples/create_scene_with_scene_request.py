from __future__ import absolute_import

from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from examples.calibration.calibration import create_sensor_calibration
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import CreateSceneResponse
from kognic.io.model.scene.scene_request import EgoVehiclePose, Frame, ImageResource, LocalFile, SceneRequest, SensorResource


def run(client: KognicIOClient, workspace_id: str) -> Optional[CreateSceneResponse]:
    print("Creating Lidar and Camera Sequence Scene...")

    lidar_sensor1 = "lidar"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    cam_sensor3 = "RFC03"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"}

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1], [cam_sensor1, cam_sensor2, cam_sensor3])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    scene = SceneRequest(
        workspace_id=workspace_id,
        external_id=f"scene-full-example-{uuid4()}",
        frames=[
            Frame(
                frame_id="1",
                timestamp_ns=1742300114000000000,
                pointclouds=[
                    SensorResource(
                        external_resource_uri=None,
                        sensor_name=lidar_sensor1,
                        local_file=LocalFile(filename="./examples/resources/point_cloud_RFL01.las"),
                    )
                ],
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC01.jpg"),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC02.jpg"),
                    ),
                ],
                ego_vehicle_pose=EgoVehiclePose(x=1.0, y=1.0, z=1.0, rotation_x=1.01, rotation_y=1.01, rotation_z=1.01, rotation_w=0.01),
                metadata={"dut_status": "active"},
            ),
            Frame(
                frame_id="2",
                timestamp_ns=1742300115000000000,
                pointclouds=[
                    SensorResource(
                        external_resource_uri=None,
                        sensor_name=lidar_sensor1,
                        local_file=LocalFile(filename="./examples/resources/point_cloud_RFL02.las"),
                    )
                ],
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC11.jpg"),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC12.jpg"),
                    ),
                ],
                ego_vehicle_pose=EgoVehiclePose(x=2.0, y=2.0, z=2.0, rotation_x=2.01, rotation_y=2.01, rotation_z=2.01, rotation_w=0.01),
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    return client.scene.create_scene(scene)


def run_with_alternative_data_sources(client: KognicIOClient, workspace_id: str) -> Optional[CreateSceneResponse]:
    print("Creating Lidar and Camera Sequence Scene...")

    lidar_sensor1 = "lidar"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    cam_sensor3 = "RFC03"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"}

    # Create calibration
    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1], [cam_sensor1, cam_sensor2, cam_sensor3])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    # Callback to sources and returns the bytes for some input file. This example implementation assumes the filename
    # refers to a local file but it may source the bytes for that name via any means.
    def get_bytes(name: str) -> bytes:
        return Path(name).open("rb").read()

    pc_name = "./examples/resources/point_cloud_RFL01.las"
    img1_name = "./examples/resources/img_RFC01.jpg"
    img2_name = "./examples/resources/img_RFC02.jpg"

    scene = SceneRequest(
        workspace_id=workspace_id,
        external_id=f"scene-full-example-{uuid4()}",
        frames=[
            Frame(
                frame_id="1",
                timestamp_ns=1742300114000000000,
                pointclouds=[
                    SensorResource(
                        external_resource_uri=None,
                        sensor_name=lidar_sensor1,
                        # PC is used without any special treatment
                        local_file=LocalFile(filename=pc_name),
                    )
                ],
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        # Alternative 1: data is passed directly as an in-memory blob
                        local_file=LocalFile(filename=img1_name, data=get_bytes(img1_name)),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        # Alternative 2: data will be obtained from a callback
                        local_file=LocalFile(filename=img2_name, callback=get_bytes),
                    ),
                ],
                ego_vehicle_pose=EgoVehiclePose(x=1.0, y=1.0, z=1.0, rotation_x=1.01, rotation_y=1.01, rotation_z=1.01, rotation_w=0.01),
                metadata={"dut_status": "active"},
            ),
            Frame(
                frame_id="2",
                timestamp_ns=1742300115000000000,
                pointclouds=[
                    SensorResource(
                        external_resource_uri=None,
                        sensor_name=lidar_sensor1,
                        local_file=LocalFile(filename="./examples/resources/point_cloud_RFL02.las"),
                    )
                ],
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC11.jpg"),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=cam_sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC12.jpg"),
                    ),
                ],
                ego_vehicle_pose=EgoVehiclePose(x=2.0, y=2.0, z=2.0, rotation_x=2.01, rotation_y=2.01, rotation_z=2.01, rotation_w=0.01),
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    return client.scene.create_scene(scene)


def run_images_only(client: KognicIOClient, workspace_id: str) -> Optional[CreateSceneResponse]:
    print("Creating Cameras Sequence Scene...")

    sensor1 = "RFC01"
    sensor2 = "RFC02"
    metadata = {"location-lat": 27.986065, "location-long": 86.922623, "vehicle_id": "abg"}

    scene = SceneRequest(
        workspace_id=workspace_id,
        external_id=f"scene-images-example-{uuid4()}",
        frames=[
            Frame(
                frame_id="1",
                timestamp_ns=1742300114000000000,
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC01.jpg", data=None, callback=None),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC02.jpg", data=None, callback=None),
                    ),
                ],
                metadata={"dut_status": "active"},
            ),
            Frame(
                frame_id="2",
                timestamp_ns=1742300115000000000,
                images=[
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=sensor1,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC11.jpg", data=None, callback=None),
                    ),
                    ImageResource(
                        external_resource_uri=None,
                        sensor_name=sensor2,
                        start_shutter_timestamp_ns=None,
                        end_shutter_timestamp_ns=None,
                        local_file=LocalFile(filename="./examples/resources/img_RFC12.jpg", data=None, callback=None),
                    ),
                ],
                metadata={"dut_status": "active"},
            ),
        ],
        metadata=metadata,
    )

    # Create scene
    return client.scene.create_scene(scene)


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    run(client, dryrun=True)
