import time
from typing import List

from kognic.io.client import KognicIOClient
from kognic.io.model import SceneStatus
from kognic.io.model.input.input import Input


class SceneException(Exception):
    pass


class SceneFailedException(SceneException):
    pass


class SceneNotFinishedException(SceneException):
    pass


class PreAnnotationFailedException(Exception):
    pass


class PreAnnotationNotAvailableException(Exception):
    pass


class InputNotCreatedException(Exception):
    pass


DEFAULT_TIMEOUT = 300


def wait_for_scene_job(client: KognicIOClient, scene_uuid: str, timeout=DEFAULT_TIMEOUT, fail_on_failed: bool = False) -> SceneStatus:
    wait_for = [SceneStatus.Created] if fail_on_failed else [SceneStatus.Created, SceneStatus.Failed]
    fail_on = [SceneStatus.Failed] if fail_on_failed else []
    return wait_for_scene_job_status(client, scene_uuid, wait_for, fail_on, timeout=timeout)


def wait_for_scene_job_status(
    client: KognicIOClient, scene_uuid: str, wait_for: List[SceneStatus], fail_on: List[SceneStatus], timeout=DEFAULT_TIMEOUT
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


def wait_for_pre_annotation(client: KognicIOClient, pre_annotation_uuid: str, timeout=DEFAULT_TIMEOUT, fail_on_failed: bool = False) -> str:
    wait_for = ["available"] if fail_on_failed else ["available", "failed"]
    fail_on = ["failed"] if fail_on_failed else []
    return wait_for_pre_annotation_status(client, pre_annotation_uuid, wait_for, fail_on, timeout=timeout)


def wait_for_pre_annotation_status(
    client: KognicIOClient, pre_annotation_uuid: str, wait_for: List[str], fail_on: List[str], timeout=DEFAULT_TIMEOUT
) -> str:
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        preanno = client.pre_annotation.list(ids=[pre_annotation_uuid])[0]
        status = preanno["status"]
        if status in fail_on:
            # error isn't yet exposed.
            raise PreAnnotationFailedException(f"Pre-annotation failed: status={status}")
        if status in wait_for:
            return status

        time.sleep(1)

    raise PreAnnotationNotAvailableException(f"Pre-annotation did not become available: {pre_annotation_uuid}")


def wait_for_inputs_for_scene(client: KognicIOClient, scene_uuid: str, count: int = 1, timeout=DEFAULT_TIMEOUT) -> list[Input]:
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        request_inputs = client.input.query_inputs(scene_uuids=[scene_uuid])
        if len(request_inputs) >= count:
            return request_inputs
        time.sleep(1)
    raise InputNotCreatedException(f">={count} request inputs did not get created for scene {scene_uuid}")
