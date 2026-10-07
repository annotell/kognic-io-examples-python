from typing import List

from kognic.io.client import KognicIOClient
from kognic.io.model import Scene


def run(client: KognicIOClient, external_ids: List[str]) -> List[Scene]:
    print("Listing scenes...")
    return client.scene.get_scenes_by_external_ids(external_ids=external_ids)


if __name__ == "__main__":
    client = KognicIOClient()

    external_ids = ["scene-external-id"]
    run(client, external_ids)
