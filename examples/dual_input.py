from __future__ import absolute_import

import os.path
from datetime import datetime
from uuid import uuid4

import kognic.io.model.scene.lidars_and_cameras_sequence as LCS
import kognic.openlabel.models.models as OLM
from examples.calibration.calibration import create_sensor_calibration
from examples.utils import wait_for_scene_job
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import Image, PointCloud
from kognic.io.model.input import Input
from kognic.io.model.scene.metadata.metadata import MetaData


def run(
    client: KognicIOClient,
    sequence_project: str = "lidars_and_cameras_sequence-project",
    aggregated_sequence_project: str = "aggregated_lidars_and_cameras_sequence-project",
) -> list[Input]:

    lidar_sensor1 = "RFL01"
    cam_sensor1 = "RFC01"
    metadata = MetaData(region="us")
    examples_path = os.path.dirname(__file__)

    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [lidar_sensor1], [cam_sensor1])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    scene = LCS.LidarsAndCamerasSequence(
        external_id=f"dual-input-example-{uuid4()}",
        frames=[
            LCS.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    PointCloud(filename=examples_path + "/resources/point_cloud_RFL01.csv", sensor_name=lidar_sensor1),
                ],
                images=[
                    Image(filename=examples_path + "/resources/img_RFC01.jpg", sensor_name=cam_sensor1),
                ],
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    # Create the standalone scene.
    print("Create scene...")
    scene_response = client.lidars_and_cameras_sequence.create(scene, dryrun=False)
    scene_uuid = scene_response.scene_uuid
    print(f"Wait for scene {scene_uuid} ...")
    wait_for_scene_job(client, scene_uuid, fail_on_failed=True)
    print(f"Scene was created: {scene_uuid}")

    # ALCS wants a pre-anno that's squashed to 1 frame. As there only is 1 frame, we can use it for LCS too.
    object_uuid = str(uuid4())
    pre_annotation_ol = OLM.OpenLabelAnnotation(
        openlabel=OLM.Openlabel(
            metadata=OLM.Metadata(name="dual_input test pre-annotation", schema_version=OLM.SchemaVersion.field_1_0_0),
            objects={object_uuid: OLM.Object(name="MyNameIsBox", type="SpaceShip")},
            frames={
                "0": OLM.Frame(
                    frame_properties=OLM.FrameProperties(streams={lidar_sensor1: OLM.Stream()}, timestamp=0, external_id="1"),
                    objects={
                        object_uuid: OLM.Objects(
                            object_data=OLM.ObjectData(
                                cuboid=[
                                    OLM.Cuboid(
                                        attributes=OLM.Attributes(
                                            text=[
                                                OLM.Text(name="stream", val=lidar_sensor1),
                                            ]
                                        ),
                                        name="Cuboid-1",
                                        val=[
                                            -0.37240600585938,
                                            -0.776424407958984,
                                            0.0018768074223771691,
                                            -0.008678210841102768,
                                            0.011558858557049027,
                                            0.2286106806721516,
                                            0.9734106215406072,
                                            1.767102435869269,
                                            4.099334155319101,
                                            1.3691029802958168,
                                        ],
                                    )
                                ],
                                bbox=[
                                    OLM.Bbox(
                                        attributes=OLM.Attributes(
                                            text=[
                                                OLM.Text(name="stream", val=cam_sensor1),
                                                OLM.Text(name="occlusion_ratio", val="Light"),
                                            ]
                                        ),
                                        name="Bounding-box-1",
                                        val=[1.0, 1.0, 4.0, 3.0],
                                    )
                                ],
                                text=[OLM.Text(name="ship_type", val="star_destroyer")],
                            )
                        )
                    },
                )
            },
            frame_intervals=[
                OLM.FrameInterval(frame_start=0, frame_end=0),
            ],
            streams={
                lidar_sensor1: OLM.Stream(type=OLM.StreamTypes.lidar),
                cam_sensor1: OLM.Stream(type=OLM.StreamTypes.camera),
            },
        )
    )

    print("Create pre-annotations ...")
    # Note external IDs are unique within a scene.
    pre_annotation1 = client.pre_annotation.create(
        scene_uuid=scene_uuid, external_id="pa-1", pre_annotation=pre_annotation_ol, dryrun=False
    )
    pre_annotation_uuid1 = pre_annotation1.id
    print(f"Pre-annotation 1: {pre_annotation_uuid1}")
    pre_annotation2 = client.pre_annotation.create(
        scene_uuid=scene_uuid, external_id="pa-2", pre_annotation=pre_annotation_ol, dryrun=False
    )
    pre_annotation_uuid2 = pre_annotation2.id
    print(f"Pre-annotation 2: {pre_annotation_uuid2}")

    # Create an input in two requests:
    # The first request should expect an LCS scene and needs a TaskDef/Annotation Instruction WITHOUT aggregation.
    # The second may expect either an ALCS or LCS scene and needs a TaskDef/Annotation Instruction WITH aggregation.

    print("Create request inputs ...")
    request_input1 = client.input.create_from_pre_annotation(pre_annotation_uuid1, project=sequence_project, dryrun=False)
    print(f"Request input 1 created: {request_input1}")
    request_input2 = client.input.create_from_pre_annotation(pre_annotation_uuid2, project=aggregated_sequence_project, dryrun=False)
    print(f"Request input 2 created: {request_input2}")

    return [request_input1, request_input2]


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    run(client)
