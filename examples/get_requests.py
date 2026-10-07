from typing import List

from kognic.io.client import KognicIOClient
from kognic.io.model import Request


def run(client: KognicIOClient, project_id: str) -> List[Request]:
    print("Listing requests...")
    return client.request.get_requests(project_id=project_id, include_input_progress_counts=True)


if __name__ == "__main__":
    client = KognicIOClient()

    project_id = "00000000-0000-0000-0000-000000000000"
    requests = run(client, project_id=project_id)

    for request in requests:
        counts = request.input_progress_counts
        print(f"{request.title}: {counts.not_started} not started of {counts.total}" if counts else request.title)
