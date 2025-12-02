from typing import Dict, Optional, Union
from uuid import UUID

from kognic.io.client import KognicIOClient
from kognic.io.model.ego import EgoVehiclePose


def run(client: KognicIOClient, scene_uuid: Union[str, UUID]) -> Optional[Dict[str, EgoVehiclePose]]:
    print("Getting scene ego poses...")
    return client.scene.get_ego_poses(scene_uuid=scene_uuid)


if __name__ == "__main__":
    client = KognicIOClient(write_workspace_id="")

    scene_uuid = "add-your-scene-uuid-here"
    ego_poses = run(client, scene_uuid)
    if ego_poses:
        for frame_id, pose in ego_poses.items():
            print(f"Frame {frame_id}: position={pose.position}, rotation={pose.rotation}")
    else:
        print("No ego poses found for this scene")
