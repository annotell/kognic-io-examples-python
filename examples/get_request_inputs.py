from __future__ import absolute_import

from typing import List, Optional

from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model import RequestInput


def run(client: KognicIOClient, request_id: str, scene_id: Optional[str] = None, page_size: Optional[int] = None) -> List[RequestInput]:
    return list(client.input.get_request_inputs(request_id=request_id, scene_id=scene_id, page_size=page_size))


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    # Only requests on flexible workflows are supported
    request_id = "<request-id>"
    request_inputs = run(client, request_id)

    for request_input in request_inputs:
        progress = request_input.progress_details
        stage = progress.current_workflow_stage.name if progress else "unknown stage"
        print(f"{request_input.scene_id}: {request_input.status.value} ({stage})")
