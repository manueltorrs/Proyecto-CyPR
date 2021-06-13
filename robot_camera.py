#-----------placing the table and puzzle box-----------#
#Libraries
from tdw.librarian import ModelLibrarian

#Preparing the models file
lib = ModelLibrarian("models_core.json")
# Get the record for the table.
table_record = lib.get_record("small_table_green_marble")

table_id = 0

#-----------placing magnebot-----------#
#Libraries
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.output_data import OutputData, StaticRobot

#-----------Importing Yolov4-----------#
import libreria as yolo

"""
Add a camera to a Magnebot.
"""

if __name__ == "__main__":
    c = Controller(launch_build=True)
    c.start()
    robot_id = 0
    avatar_id = "a"
    # Add a Magnebot to the scene. Request static robot data.
    resp = c.communicate([TDWUtils.create_empty_room(12, 12),
                          {"$type": "add_magnebot",
                           "position": {"x": 0, "y": 0, "z": 0},
                           "rotation": {"x": 0, "y": 0, "z": 0},
                           "id": robot_id},
                          {"$type": "send_static_robots",
                           "frequency": "once"},
                            {"$type": "set_screen_size",
                            "width": 1024,
                            "height": 780}])
    # Find the static robot data and get the ID of the torso.
    torso_id = -1
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "srob":
            static_robot = StaticRobot(resp[i])
            for j in range(static_robot.get_num_joints()):
                if static_robot.get_joint_name(j) == "torso":
                    torso_id = static_robot.get_joint_id(j)
    # Create an avatar and parent it to the torso.
    c.communicate([{"$type": "create_avatar",
                    "type": "A_Img_Caps_Kinematic",
                    "id": avatar_id},
                   {"$type": "parent_avatar_to_robot",
                    "position": {"x": 0, "y": 0.053, "z": 0.1838},
                    "id": robot_id,
                    "avatar_id": avatar_id,
                    "body_part_id": torso_id}])
    




"""
if __name__ == "__main__":
    c = Controller(launch_build=True)
    c.start()
    robot_id = 0
    avatar_id = "a"
    # Add a Magnebot to the scene. Request static robot data.
    resp = c.communicate([TDWUtils.create_empty_room(12, 12),
                            {"$type": "add_magnebot",
                            "position": {"x": 0, "y": 0, "z": 0},
                            "rotation": {"x": 0, "y": 0, "z": 0},
                            "id": robot_id},
                            {"$type": "send_static_robots",
                            "frequency": "once"},
                            {"$type": "set_screen_size",
                            "width": 1920,
                            "height": 1080}])
                            
    c.communicate([{"$type": "load_scene",
                            "scene_name": "ProcGenScene"},
                            c.get_add_object(model_name=table_record.name,
                                        object_id=table_id,
                                        position={"x": -10, "y": 10, "z": 0},
                                        rotation={"x": 0, "y": 0, "z": 0}),
                            {"$type": "send_bounds",
                            "ids": [table_id],
                            "frequency": "once"}])
    # Find the static robot data and get the ID of the torso.
    torso_id = -1
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "srob":
            static_robot = StaticRobot(resp[i])
            for j in range(static_robot.get_num_joints()):
                if static_robot.get_joint_name(j) == "torso":
                    torso_id = static_robot.get_joint_id(j)
    # Create an avatar and parent it to the torso.
    c.communicate([{"$type": "create_avatar",
                    "type": "A_Img_Caps_Kinematic",
                    "id": avatar_id},
                   {"$type": "parent_avatar_to_robot",
                    "position": {"x": 0, "y": 0.053, "z": 0.1838},
                    "id": robot_id,
                    "avatar_id": avatar_id,
                    "body_part_id": torso_id}])
"""