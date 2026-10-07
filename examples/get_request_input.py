from __future__ import absolute_import

from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import RequestInput


def run(client: KognicIOClient, request_input_id: str) -> RequestInput:
    return client.input.get_request_input(request_input_id=request_input_id)


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    # Only inputs of requests on flexible workflows are supported
    request_input_id = "<request-input-id>"
    request_input = run(client, request_input_id)

    progress = request_input.progress_details
    stage = progress.current_workflow_stage.name if progress else "unknown stage"
    print(f"{request_input.scene_id}: {request_input.status.value} ({stage})")
