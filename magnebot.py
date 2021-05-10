from tdw.controller import Controller
from tdw.output_data import OutputData, StaticRobot
from tdw.tdw_utils import TDWUtils
from tdw.keyboard_controller import KeyboardController
from typing import Union
import ipdb

"""
Add a Magnebot and move it around the scene.
"""

# Dict to stores joint names with its current id
jointNamesDict = {
    "wheelLeftFront": 0,
    "wheelLeftBack": 1,
    "wheelRightFront": 2,
    "wheelRightBack": 3,
    "column": 4,
    "torso": 5,
    "shoulderLeft": 6,
    "elbowLeft": 7,
    "wristLeft": 8,
    "magnetLeft": 9,
    "shoulderRight": 10,
    "elbowRight": 11,
    "wristRight": 12,
    "magnetRight": 13,
}


class KeyboardControl(KeyboardController):
    """
    Heredates from KeybpardController.
    Creates new methods within the class to move different parts of the magnebot robot.
    """
    def __init__(self, robotId: Union[int, str],  port: int = 1071) -> None:
        """
        Initialize class.

        Args:
        port -> default 1071.
        Returns:
        None.
        """
        super().__init__(port = port)
        self.id = robotId

    def moveBase(self, direction: int, force: float = 80) -> dict:
        """
        Move magnebot's base.

        Args:
        directions -> movement's direction.
        force -> movement-s force.
        Returns:
        A `move_avatar_forward_by` command.
        """
        return {"$type": "move_avatar_forward_by",
                "magnitude": force * direction,
                "avatar_id": self.id}











if __name__ == "__main__":
    c = Controller()
    c.start()
    robot_id = 0
    # Add a Magnebot to the scene and request static data.
    commands = [TDWUtils.create_empty_room(12, 12),
                          {"$type": "add_magnebot",
                           "id": robot_id,
                           "position": {"x": 0, "y": 0, "z": 0},
                           "rotation": {"x": 0, "y": 90, "z": 0}},
                          {"$type": "send_static_robots",
                           "ids": [robot_id],
                           "frequency": "once"},
                          {"$type": "set_screen_size",
                           "width": 1920,
                           "height": 1080}]
    # Add a camera to the scene.
    # commands.extend(TDWUtils.create_avatar(position={"x": -2.49, "y": 4, "z": 0},
    commands.extend(TDWUtils.create_avatar(position={"x": 4.0, "y": 1, "z": 0},
                                           look_at={"x": 0, "y": 1, "z": 0}))
    resp = c.communicate(commands)
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "srob":
            sr = StaticRobot(resp[i])
            for j in range(sr.get_num_joints()):
                joint_id = sr.get_joint_id(j)
                joint_name = sr.get_joint_name(j)
                print(joint_name, joint_id)
                # Find all of the wheels.
                if "wheel_left_front" in joint_name:
                    jointNamesDict.update({"wheelLeftFront": joint_id})
                elif "wheel_left_back" in joint_name:
                    jointNamesDict.update({"wheelLeftBack": joint_id})
                elif "wheel_right_front" in joint_name:
                    jointNamesDict.update({"wheelRightFront": joint_id})
                elif "wheel_right_back" in joint_name:
                    jointNamesDict.update({"wheelRightBack": joint_id})
                elif "column" in joint_name:
                    jointNamesDict.update({"column": joint_id})
                elif "torso" in joint_name:
                    jointNamesDict.update({"torso": joint_id})
                elif "shoulder_left" in joint_name:
                    jointNamesDict.update({"shoulderLeft": joint_id})
                elif "elbow_left" in joint_name:
                    jointNamesDict.update({"elbowLeft": joint_id})
                elif "wrist_left" in joint_name:
                    jointNamesDict.update({"wristLeft": joint_id})
                elif "magnet_left" in joint_name:
                    jointNamesDict.update({"magnetLeft": joint_id})
                elif "shoulder_right" in joint_name:
                    jointNamesDict.update({"shoulderRight": joint_id})
                elif "elbow_right" in joint_name:
                    jointNamesDict.update({"elbowRight": joint_id})
                elif "wrist_right" in joint_name:
                    jointNamesDict.update({"wristRight": joint_id})
                elif "magnet_right" in joint_name:
                    jointNamesDict.update({"magnetRight": joint_id})

    # Create empty list to store commands
    commands = []
    # for wheel_id in wheel_ids:
        # commands.append({"$type": "set_revolute_target",
                         # "id": robot_id,
                         # "joint_id": wheel_id,
                         # "target": 1500})
    # for id1 in ids:
        # commands.append({"$type": "set_prismatic_target",
                         # "id": robot_id,
                         # "joint_id": id1,
                         # "target": 2})

    commands.append({"$type": "set_revolute_target",
                     "id": robot_id,
                     "joint_id": jointNamesDict["column"],
                     "target": 180})
    c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])

    # Reset command list
    commands = []
    # for wheel_id in wheel_ids:
        # commands.append({"$type": "set_revolute_target",
                         # "id": robot_id,
                         # "joint_id": wheel_id,
                         # "target": 0})
    # for id1 in ids:
        # commands.append({"$type": "set_prismatic_target",
                         # "id": robot_id,
                         # "joint_id": id1,
                         # "target": 0.75})

    commands.append({"$type": "set_revolute_target",
                     "id": robot_id,
                     "joint_id": jointNamesDict["column"],
                     "target": 0.75})
    c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])

    # Colse communication after movements
    c.communicate({"$type": "terminate"})
