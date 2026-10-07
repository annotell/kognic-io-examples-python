from typing import List, Optional

from kognic.io.client import KognicIOClient
from kognic.io.model.input.input import Input


def run(
    client: KognicIOClient,
    scene_uuid: str,
    project: str,
    batch: Optional[str] = None,
    dryrun: bool = False,
) -> Optional[List[Input]]:
    print("Creating inputs from scene...")
    return client.cameras.create_from_scene(scene_uuid=scene_uuid, project=project, batch=batch, dryrun=dryrun)


if __name__ == "__main__":
    client = KognicIOClient()

    scene_uuid = "Scene-identifier"
    project = "<project-identifier>"

    run(client, scene_uuid=scene_uuid, project=project)
