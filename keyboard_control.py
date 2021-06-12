from magnebot import Magnebot, Arm
from tdw.librarian import ModelLibrarian
from tdw.tdw_utils import TDWUtils
from tdw.output_data import OutputData, Images, CameraMatrices, Keyboard
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import numpy as np
from matplotlib import cm


def handleKeyboard(keys_pressed: list, m: Magnebot, jointIds: dict):
    '''
    Handler for keyboard. It calls other functions depending of the keys pressed
    inputs:
    - key_pressed: list of strings with the keys pressed.
    NOTE: letters are always capitalized: 'A', 'B', ...
    '''
    dist = 1
    for key in keys_pressed:
        if key == 'Escape':
            print("STATUS: Terminando simulación...")
            m.end()
            global done
            done = True
        elif key == 'W':
            print("STATUS: Avanzando...")
            m.move_by(1)
        elif key == 'S':
            print("STATUS: Marcha atrás...")
            m.move_by(-1)
        elif key == 'A':
            print("STATUS: Girando izquierda...")
            m.turn_by(-90)
        elif key == 'D':
            print("STATUS: Girando derecha...")
            m.turn_by(90)
        elif key == 'C':
            toggleCamera(m)
        elif key == 'P':
            print('Tomando foto...')
            takePhoto(m)
        else:
            print(key, ' no tiene una acción definida')


def toggleCamera(m):
    if toggleCamera.exteriorCamera:
        m.communicate({"$type": "set_render_order", "render_order": -1, "sensor_name": "SensorContainer", "avatar_id": "a"})
        m.communicate({"$type": "set_render_order", "render_order": 1, "sensor_name": "SensorContainer", "avatar_id": "c"})
        toggleCamera.exteriorCamera = False
        print("STATUS: Cambiando a cámara exterior...")
    else:
        m.communicate({"$type": "set_render_order", "render_order": 1, "sensor_name": "SensorContainer", "avatar_id": "a"})
        m.communicate({"$type": "set_render_order", "render_order": -1, "sensor_name": "SensorContainer", "avatar_id": "c"})
        print("STATUS: Cambiando a cámara interior...")
        toggleCamera.exteriorCamera = True
toggleCamera.exteriorCamera = True

# def moveJoint(m, jointIds, angle, joint):
#     '''
#     This function sends a message to the build to turn the joint of the magnebot
#     by some angle
#     Inputs:
#     - m: magnebot controller
#     - joint: joint to turn
#     - angles: angle (in degrees) to move the joint
#     - joint: string with the name of the string
#     '''
#     actual_angle = m.state.joint_angles[jointIds[joint]][0]
#     print(actual_angle)
#     for j_id in m.state.joint_angles:
#         # print(id_j, m.state.joint_angles[jointIds[joint]][2])
#         position = m.state.joint_angles[j_id]
#         name = m.magnebot_static.joints[j_id].name
#         print(position, name)
#     obj_angle = actual_angle + angle
#     print(obj_angle)
#     commands = []
#     commands.append(
#             {"$type": "set_revolute_target",
#             "joint_id": jointIds[joint],
#             "id": jointIds['magnebot(Clone)'],
#             "target": obj_angle})
#     m.communicate(commands)

def moveArm(m, arm):
    m.reach_for(target={"x": 0.1, "y": 0.1, "z": 0.1}, arm=arm)

def takePhoto(m):
    with Path("./foto.jpg").open("wb") as f:
        f.write(m.state.images["img"])
    # print(m.state.images["depth"])

if __name__ == '__main__':
    robot_id = 0
    m = Magnebot(launch_build=True, screen_width=500, screen_height=500, skip_frames=0)
    m.init_scene()

    jointNamesDict = {} 
    for joint_id in m.magnebot_static.joints:
        jointNamesDict[m.magnebot_static.joints[joint_id].name] = joint_id

    m.add_camera({'x': 0.5, 'y': 3, 'z': -1}, camera_id="c")

    m.add_object("live_edge_coffee_table",
                        position={"x": -12.8, "y": 0.96, "z": -5.47},
                        rotation={"x": 0, "y": -90, "z": 0})
    done = False

    m.communicate([{"$type": "send_keyboard",
                    "frequency": "always"},
                    {"$type": "set_pass_masks",
                    "avatar_id": "a",
                    "pass_masks": ["_img", "_id", "_depth"]},
                    {"$type": "send_images",
                    "ids": ["a"],
                    "frequency": "always"},
                    ])
    m.add_object(model_name="trunck", position={"x": 0, "y": 0, "z": 2})

    keyboard_pressed = []
    img_number = 0
    while not done:
        resp = m.communicate([])
        for r in resp[:-1]:
                r_id = OutputData.get_data_type_id(r)
                if r_id == "keyb":
                    keyboard_input = Keyboard(r)
                    for i in range(keyboard_input.get_num_pressed()):
                        if keyboard_input.get_pressed(i):
                            keyboard_pressed.append(keyboard_input.get_pressed(i))
                elif r_id == "imag":
                    img_identifier = Images(r)
                    for i in range(img_identifier.get_num_passes()):
                        img = img_identifier.get_image(i)
                        pass_mask = img_identifier.get_pass_mask(i)
                        ext = img_identifier.get_extension(i)
                        
                        if pass_mask == '_depth':
                            pil_image = Image.fromarray(TDWUtils.get_shaped_depth_pass(images=img_identifier, index=i))

                        else:
                            pil_image = TDWUtils.get_pil_image(img_identifier, i)
                        if img_number == 0: # Solo mostrar las primeras imágenes
                            pil_image.show()

                        TDWUtils.save_images(images=img_identifier, output_directory="./images", filename="1", append_pass=True)
                    img_number += 1

        handleKeyboard(keyboard_pressed, m, jointNamesDict)
        keyboard_pressed = []
