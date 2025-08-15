from __future__ import absolute_import

import os.path
import time
from datetime import datetime
from uuid import uuid4

import kognic.io.model.scene.cameras_sequence as CS
import kognic.openlabel.models.models as OLM
from examples.calibration.calibration import create_sensor_calibration
from examples.utils import wait_for_scene_job
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import Image
from kognic.io.model.input import Input
from kognic.io.model.scene.metadata.metadata import MetaData


def run(client: KognicIOClient, cameras_sequence_project: str = "cameras_sequence-project") -> Input:
    cam_sensor1 = "RFC01"
    metadata = MetaData(region="kz")
    examples_path = os.path.dirname(__file__)

    calibration_spec = create_sensor_calibration(f"Collection {datetime.now()}", [], [cam_sensor1])
    created_calibration = client.calibration.create_calibration(calibration_spec)

    scene = CS.CamerasSequence(
        external_id=f"update-pre-annotation-example-{uuid4()}",
        frames=[
            CS.Frame(
                frame_id="1",
                relative_timestamp=0,
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
    scene_response = client.cameras_sequence.create(scene, dryrun=False)
    scene_uuid = scene_response.scene_uuid
    print(f"Wait for scene {scene_uuid} ...")
    wait_for_scene_job(client, scene_uuid, fail_on_failed=True)
    print(f"Scene was created: {scene_uuid}")

    # Create two pre-annotations
    object_uuid1 = str(uuid4())
    pre_annotation_ol1 = OLM.OpenLabelAnnotation(
        openlabel=OLM.Openlabel(
            metadata=OLM.Metadata(name="update_pre_annotation test pre-annotation 1", schema_version=OLM.SchemaVersion.field_1_0_0),
            objects={object_uuid1: OLM.Object(name="NormalVehicle", type="Vehicle")},
            frames={
                "0": OLM.Frame(
                    frame_properties=OLM.FrameProperties(streams={cam_sensor1: OLM.Stream()}, timestamp=0, external_id="1"),
                    objects={
                        object_uuid1: OLM.Objects(
                            object_data=OLM.ObjectData(
                                bbox=[
                                    OLM.Bbox(
                                        attributes=OLM.Attributes(
                                            text=[
                                                OLM.Text(name="stream", val=cam_sensor1),
                                                OLM.Text(name="OcclusionRatio", val="Light (1%-20%)"),
                                            ]
                                        ),
                                        name="Bounding-box-1",
                                        val=[10.0, 10.0, 50.0, 30.0],
                                    )
                                ]
                            )
                        )
                    },
                )
            },
            frame_intervals=[
                OLM.FrameInterval(frame_start=0, frame_end=0),
            ],
            streams={
                cam_sensor1: OLM.Stream(type=OLM.StreamTypes.camera),
            },
        )
    )

    object_uuid2 = str(uuid4())
    pre_annotation_ol2 = OLM.OpenLabelAnnotation(
        openlabel=OLM.Openlabel(
            metadata=OLM.Metadata(name="update_pre_annotation test pre-annotation 2", schema_version=OLM.SchemaVersion.field_1_0_0),
            objects={object_uuid2: OLM.Object(name="SecondBox", type="Vehicle")},
            frames={
                "0": OLM.Frame(
                    frame_properties=OLM.FrameProperties(streams={cam_sensor1: OLM.Stream()}, timestamp=0, external_id="1"),
                    objects={
                        object_uuid2: OLM.Objects(
                            object_data=OLM.ObjectData(
                                bbox=[
                                    OLM.Bbox(
                                        attributes=OLM.Attributes(
                                            text=[
                                                OLM.Text(name="stream", val=cam_sensor1),
                                                OLM.Text(name="OcclusionRatio", val="Heavy (51%-80%)"),
                                            ]
                                        ),
                                        name="Bounding-box-2",
                                        val=[100.0, 100.0, 80.0, 60.0],
                                    )
                                ]
                            )
                        )
                    },
                )
            },
            frame_intervals=[
                OLM.FrameInterval(frame_start=0, frame_end=0),
            ],
            streams={
                cam_sensor1: OLM.Stream(type=OLM.StreamTypes.camera),
            },
        )
    )

    # Note external IDs are unique within a scene.
    pre_annotation1 = client.pre_annotation.create(
        scene_uuid=scene_uuid, external_id="pa-1", pre_annotation=pre_annotation_ol1, dryrun=False
    )
    pre_annotation_id1 = pre_annotation1.id
    print(f"Pre-annotation 1: {pre_annotation_id1}")

    pre_annotation2 = client.pre_annotation.create(
        scene_uuid=scene_uuid, external_id="pa-2", pre_annotation=pre_annotation_ol2, dryrun=False
    )
    pre_annotation_id2 = pre_annotation2.id
    print(f"Pre-annotation 2: {pre_annotation_id2}")

    # Create an input with the first pre-annotation
    print("Create request input with first pre-annotation...")
    request_input = client.input.create_from_pre_annotation(pre_annotation_id1, project=cameras_sequence_project, dryrun=False)
    print(f"Request input created: {request_input}")
    time.sleep(2)

    print(f"Updating input {request_input.uuid} to pre-annotation to {pre_annotation_id2}...")
    client.input.update_pre_annotation(request_input.uuid, pre_annotation_id2)

    return request_input


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    run(client)
