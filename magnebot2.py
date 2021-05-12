from tdw.controller import Controller
from tdw.output_data import OutputData, StaticRobot
from tdw.tdw_utils import TDWUtils
from tdw.keyboard_controller import KeyboardController


if __name__ == "__main__":
    c = Controller(launch_build=True)
    print("This controller demonstrates low-level controls for the Magnebot")
    print("For a high-level API, please see: https://github.com/alters-mit/magnebot")
    c.start()
    robot_id = 0
    # Add a Magnebot to the scene and request static data.
    commands = [TDWUtils.create_empty_room(12, 12),
                          {"$type": "add_magnebot",
                           "id": robot_id,
                           "position": {"x": 0, "y": 0, "z": 0},
                           "rotation": {"x": 0, "y": 0, "z": 0}},
                          {"$type": "send_static_robots",
                           "ids": [robot_id],
                           "frequency": "once"}]
    # Add a camera to the scene.
    commands.extend(TDWUtils.create_avatar(position={"x": -2.49, "y": 4, "z": 0},
                                           look_at={"x": 0, "y": 0, "z": 0}))
    resp = c.communicate(commands)
    wheel_ids = []
    torso_ids = []
    arm_ids = []
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "srob":
            sr = StaticRobot(resp[i])
            for j in range(sr.get_num_joints()):
                joint_id = sr.get_joint_id(j)
                joint_name = sr.get_joint_name(j)
                print(joint_name, joint_id)
                # Find all of the wheels.
                if "wheel" in joint_name:
                    wheel_ids.append(joint_id)
                if "elbow" in joint_name:
                    arm_ids.append(joint_id)
                if "torso" in joint_name:
                    torso_ids.append(joint_id)

    # Move the wheels forward.
    commands = []
    for wheel_id in wheel_ids:
        commands.append({"$type": "set_revolute_target",
                         "id": robot_id,
                         "joint_id": wheel_id,
                         "target": 360})
    c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])
    # Move backwards. The target is always the TOTAL degrees traversed, as opposed to a delta.
    commands = []
    for wheel_id in wheel_ids:
        commands.append({"$type": "set_revolute_target",
                         "id": robot_id,
                         "joint_id": wheel_id,
                         "target": -360})
    c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])
#----------------------------------------------

# ----------movimiento de brazos y torso-------
    # Move elbows.
    commands = []
    for arm_id in arm_ids:
        commands.append({"$type": "set_revolute_target",
                        "id": robot_id,
                        "joint_id": arm_id,
                        "target": 1000})
        c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])

    # Move torso.
    commands = []
    for torso_id in torso_ids:
        commands.append({"$type": "set_revolute_target",
                        "id": robot_id,
                        "joint_id": torso_id,
                        "target": 3000})
        c.communicate(commands)
    # Wait a bit.
    for i in range(100):
        c.communicate([])
#----------------------------------------------

# ----------CONTROL POR TECLADO----------------


#----------------------------------------------

from magnebot import Magnebot, Arm
import keyboard
from tdw.output_data import OutputData, StaticRobot
from tdw.tdw_utils import TDWUtils





if __name__ == '__main__':
    m = Magnebot(launch_build=True, screen_width=500, screen_height=500, skip_frames=0)
    m.init_scene()

    m.add_camera({'x': 0.5, 'y': 3, 'z': 1})
   
    # Control por teclado
    while True:
        resp = m.communicate([])
        if(keyboard.is_pressed('w')):
            m.move_by(1)
        elif(keyboard.is_pressed('s')):
            m.move_by(-1)
            pass
        elif(keyboard.is_pressed('esc')):
            m.end()
            break

    