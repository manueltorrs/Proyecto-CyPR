from magnebot import Magnebot
from tdw.librarian import ModelLibrarian
from tdw.tdw_utils import TDWUtils
from tdw.output_data import OutputData, Images, CameraMatrices, Keyboard
import matplotlib.pyplot as plt


def handleKeyboard(keys_pressed: list, m: Magnebot):
    '''
    Handler for keyboard. It calls other functions depending of the keys pressed
    inputs:
    - key_pressed: list of strings with the keys pressed.
    NOTE: letters are always capitalized: 'A', 'B', ...
    '''
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

if __name__ == '__main__':
    m = Magnebot(launch_build=True, screen_width=500, screen_height=500, skip_frames=0)
    m.init_scene()
            
    m.add_camera({'x': 0.5, 'y': 3, 'z': -1}, camera_id="c")

    done = False

    m.communicate({"$type": "send_keyboard",
                    "frequency": "always"})

    keyboard_pressed = []
    while not done:
        resp = m.communicate([])
        for r in resp[:-1]:
                r_id = OutputData.get_data_type_id(r)
                if r_id == "keyb":
                    keyboard_input = Keyboard(r)
                    for i in range(keyboard_input.get_num_pressed()):
                        if keyboard_input.get_pressed(i):
                            keyboard_pressed.append(keyboard_input.get_pressed(i))
        handleKeyboard(keyboard_pressed, m)
        keyboard_pressed = []
