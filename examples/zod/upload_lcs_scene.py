import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

import numpy as np
from conversion import (
    convert_calibration,
    convert_to_ego_vehicle_pose,
    convert_zod_camera_frame_to_image,
    convert_zod_lidar_frame_to_point_cloud,
)
from kognic.io.client import KognicIOClient
from kognic.io.model import LidarsAndCamerasSequence
from kognic.io.model.calibration import SensorCalibration
from kognic.io.model.scene.lidars_and_cameras_sequence import Frame as LCSFrame
from utils import ns_to_ms, seconds_to_ns
from zod.constants import Lidar as ZodLidar
from zod.constants import Version as ZodVersion
from zod.zod_sequences import ZodSequence, ZodSequences

logging.basicConfig(level=logging.WARNING)

LARGE_NUMBER = 1000000


def upload_lcs_scenes(
    zod_path: Path,
    zod_version: ZodVersion,
    client: KognicIOClient,
    max_nr_scenes: Optional[int],
    max_nr_frames: Optional[int],
    dryrun: bool,
) -> None:
    sequences = ZodSequences(str(zod_path), version=zod_version)
    for key in sorted(sequences.get_all_ids())[: max_nr_scenes or LARGE_NUMBER]:
        external_id = "sequences_" + key + "_" + str(uuid4())[:8]
        sequence = sequences[key]

        calibration = convert_calibration(sequence.calibration)
        scene = convert_scene(sequence, external_id, max_nr_frames or LARGE_NUMBER)
        scene_uuid = create_scene(client, scene, calibration, dryrun=dryrun)
        print(f"Created scene with UUID: {scene_uuid}")


def create_scene(client: KognicIOClient, scene: LidarsAndCamerasSequence, calibration: SensorCalibration, dryrun: bool = False) -> str:
    created_calibration = client.calibration.create_calibration(calibration)
    scene.calibration_id = created_calibration.id
    created_scene = client.lidars_and_cameras_sequence.create(scene, dryrun=dryrun)
    if dryrun is False:
        return created_scene.scene_uuid


def convert_scene(zod_sequence: ZodSequence, external_id: str, max_nr_frames: int) -> LidarsAndCamerasSequence:
    frames = convert_frames(zod_sequence, max_nr_frames)
    return LidarsAndCamerasSequence(external_id=external_id, frames=frames, calibration_id="<to be set later>")


def convert_frames(sequence: ZodSequence, max_nr_frames: int) -> list[LCSFrame]:
    frames, seen_frame_timestamps = list(), set()
    start_ts_ms = ns_to_ms(seconds_to_ns(sequence.info.get_lidar_frames()[0].time.timestamp()))

    lidar_calibration = sequence.calibration.lidars[ZodLidar.VELODYNE]

    for camera_frame, lidar_frame in list(sequence.info.get_camera_lidar_map())[:max_nr_frames]:
        frame_ts_s = lidar_frame.time.timestamp()

        if frame_ts_s in seen_frame_timestamps:
            continue

        seen_frame_timestamps.add(frame_ts_s)
        frame_ts_ns = seconds_to_ns(frame_ts_s)

        point_cloud = convert_zod_lidar_frame_to_point_cloud(lidar_frame, frame_ts_ns)

        ego_pose_ref = sequence.ego_motion.get_poses(frame_ts_s)  # reference coordinate system
        # transform to lidar coordinate system, since single-lidar
        ego_pose = np.matmul(ego_pose_ref, lidar_calibration.extrinsics.transform)

        frames.append(
            LCSFrame(
                relative_timestamp=ns_to_ms(frame_ts_ns) - start_ts_ms,
                frame_id=str(frame_ts_ns),
                images=[convert_zod_camera_frame_to_image(camera_frame)],
                point_clouds=[point_cloud],
                ego_vehicle_pose=convert_to_ego_vehicle_pose(ego_pose),
                unix_timestamp=frame_ts_ns,
            )
        )
    return frames


if __name__ == "__main__":
    client = KognicIOClient()

    upload_lcs_scenes(
        zod_path=Path("/path/to/zod"),  # change me
        zod_version="mini",
        client=client,
        max_nr_scenes=1,
        max_nr_frames=10,
        dryrun=False,
    )
