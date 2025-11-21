from typing import Union
from uuid import UUID

from kognic.io.client import KognicIOClient
from kognic.io.model import SceneSummary


def run(client: KognicIOClient, scene_uuid: Union[str, UUID]) -> SceneSummary:
    print("Getting scene information...")
    return client.scene.get_scene_summary(scene_uuid=scene_uuid)


if __name__ == "__main__":
    client = KognicIOClient(write_workspace_id="")

    scene_uuid = "replace-with-scene-uuid"
    scene_summary = run(client, scene_uuid)
    print(f"Scene {scene_uuid} have relative frame timestamps {scene_summary.frame_relative_times}")
