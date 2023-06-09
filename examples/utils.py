import time

from kognic.io.client import KognicIOClient
from kognic.io.model import InputStatus, Input


def wait_for_input_creation(client: KognicIOClient, input_uuid: str, timeout=20):
    input = wait_for_input_job(client, input_uuid, timeout)
    if input.status == InputStatus.Created:
        return
    elif input.status == InputStatus.Failed:
        raise Exception(f'Input creation failed for uuid {input_uuid} with error "{input.error_message}"')


def wait_for_input_job(client: KognicIOClient, input_uuid: str, timeout=20) -> Input:
    wait_for_scene_job(client, input_uuid, timeout)
    response = client.input.get_inputs_by_uuids(input_uuids=[input_uuid])
    if not response:
        raise Exception(f"No input found with uuid {input_uuid}")
    return response[0]


def wait_for_scene_job(client: KognicIOClient, scene_uuid: str, timeout=20) -> InputStatus:
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = client.input.get_inputs_by_uuids(input_uuids=[scene_uuid])

        if not response:
            return InputStatus.Created

        input = response[0]
        if input.status in [InputStatus.Created, InputStatus.Failed]:
            return input.status

        time.sleep(1)

    raise Exception(f"Job was not finished")
