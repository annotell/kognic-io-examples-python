import time
from typing import List

from kognic.io.client import KognicIOClient
from kognic.io.model import SceneStatus


class SceneException(Exception):
    pass


class SceneFailedException(SceneException):
    pass


class SceneNotFinishedException(SceneException):
    pass


def wait_for_scene_job(client: KognicIOClient, scene_uuid: str, timeout=20, fail_on_failed: bool = False) -> SceneStatus:
    wait_for = [SceneStatus.Created] if fail_on_failed else [SceneStatus.Created, SceneStatus.Failed]
    fail_on = [SceneStatus.Failed] if fail_on_failed else []
    return wait_for_scene_job_status(client, scene_uuid, wait_for, fail_on, timeout=timeout)


def wait_for_scene_job_status(
    client: KognicIOClient, scene_uuid: str, wait_for: List[SceneStatus], fail_on: List[SceneStatus], timeout=20
) -> SceneStatus:
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        response = client.scene.get_scenes_by_uuids(scene_uuids=[scene_uuid])
        scene = response[0]
        if scene.status in fail_on:
            raise SceneFailedException(f"Scene creation failed: status={scene.status}, error={scene.error_message}")
        if scene.status in wait_for:
            return scene.status

        time.sleep(1)

    raise SceneNotFinishedException(f"Job was not finished: {scene_uuid}")
