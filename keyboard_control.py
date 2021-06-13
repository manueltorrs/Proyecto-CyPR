from magnebot import Magnebot, Arm
from tdw.tdw_utils import TDWUtils
from tdw.output_data import OutputData, Images, Keyboard
from PIL import Image
import numpy as np
import cv2
# import matplotlib.pyplot as plt


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
            exit()
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
            global showExtraCameras
            if showExtraCameras:
                print('Ocultando cámaras extra...')
                showExtraCameras = False
                cv2.destroyAllWindows()
            else:
                print('Mostrando cámaras extra...')
                showExtraCameras = True
        else:
            print(key, ' no tiene una acción definida')
        # Cada vez que hacemos una acción, volvemos a pedirle que nos mande las imágenes
        # Por que si no, deja de hacerlo
        m.communicate({"$type": "send_images",
                       "ids": ["a"],
                       "frequency": "always"})


def toggleCamera(m):
    if toggleCamera.exteriorCamera:
        m.communicate({"$type": "set_render_order", "render_order": -1,
                       "sensor_name": "SensorContainer", "avatar_id": "a"})
        m.communicate({"$type": "set_render_order", "render_order": 1,
                       "sensor_name": "SensorContainer", "avatar_id": "c"})
        toggleCamera.exteriorCamera = False
        print("STATUS: Cambiando a cámara exterior...")
    else:
        m.communicate({"$type": "set_render_order", "render_order": 1,
                       "sensor_name": "SensorContainer", "avatar_id": "a"})
        m.communicate({"$type": "set_render_order", "render_order": -1,
                       "sensor_name": "SensorContainer", "avatar_id": "c"})
        print("STATUS: Cambiando a cámara interior...")
        toggleCamera.exteriorCamera = True
toggleCamera.exteriorCamera = True


def moveArm(m, arm):
    m.reach_for(target={"x": 0.1, "y": 0.1, "z": 0.1}, arm=arm)


def printHelp():
    print('\nControles:')
    print('- W: Mover delante')
    print('- S: Mover detrás')
    print('- A: Girar izquierda')
    print('- D: Girar derecha')
    print('- C: Cambiar cámara exterior/interior')
    print('- P: Mostrar otras vistas (depth, id, albedo)')
    print('- Esc: Terminar simulación')



if __name__ == '__main__':

    m = Magnebot(launch_build=True, screen_width=500,
                 screen_height=500, skip_frames=0) # Se añade el magnebot
    m.init_scene() # Se inicializa la escena
    printHelp() # Se imprime una lista con las acciones que realizan las teclas

    jointNamesDict = {} # Se crea un diccionario con todas las id de las articulaciones del magnebot
    for joint_id in m.magnebot_static.joints:
        jointNamesDict[m.magnebot_static.joints[joint_id].name] = joint_id

    m.add_camera({'x': 0.5, 'y': 3, 'z': -1}, camera_id="c") # Se añade una cámara externa


    # Pruebas mover brazos y torso
    commands = []
    commands.append({"$type": "set_revolute_target",
                     "id": m.magnebot_static.root,
                     "joint_id": jointNamesDict["elbow_left"],
                     "target": 45}) # Se prueba el movimiento de el codo izquierdo

    m.communicate(commands)
    
    # Con estos comandos se consigue lo siguiente:
    # - Que el controlador vaya enviando las teclas pulsadas cada iteración
    # - Que la cámara del magnebot renderize los mapas de profundidad, modo albedo...
    # - Que el controlador pase las imágenes renderizadas cada iteración
    # - Que en la pantalla principal se muestre por defecto la cámara del magnebot
    m.communicate([{"$type": "send_keyboard",
                    "frequency": "always"},
                   {"$type": "set_pass_masks",
                    "avatar_id": "a",
                    "pass_masks": ["_img", "_id", "_depth", "_albedo"]},
                   {"$type": "send_images",
                    "ids": ["a"],
                    "frequency": "always"},
                   {"$type": "set_render_order", "render_order": 1,
                    "sensor_name": "SensorContainer", "avatar_id": "a"},
                   {"$type": "set_render_order", "render_order": -1,
                    "sensor_name": "SensorContainer", "avatar_id": "c"}
                   ])

    m.add_object(model_name="trunck", position={"x": 0, "y": 0, "z": 2}) # Se añade un objeto a la escena
    commands = []

    showExtraCameras = False # Variable global que indica si las cámaras extra se deben mostrar o no
    done = False # Variable global que indica si el script sigue en funcionamiento
    keyboard_pressed = [] # Lista de teclas que han sido presionadas durante esta iteración
    while not done:
        resp = m.communicate([])
        for r in resp[:-1]:
            r_id = OutputData.get_data_type_id(r)
            if r_id == "keyb": # Cuando se presione una tecla, se añade a la lista
                keyboard_input = Keyboard(r)
                for i in range(keyboard_input.get_num_pressed()):
                    if keyboard_input.get_pressed(i):
                        keyboard_pressed.append(keyboard_input.get_pressed(i))
            elif r_id == "imag": # Se procesan las imágenes renderizadas y, en el caso de que sea necesario, se muestran por pantalla
                img_identifier = Images(r)
                if showExtraCameras:
                    for i in range(img_identifier.get_num_passes()):
                        img = img_identifier.get_image(i)
                        pass_mask = img_identifier.get_pass_mask(i)

                        if pass_mask == '_depth':
                            pil_image = Image.fromarray(
                                TDWUtils.get_shaped_depth_pass(images=img_identifier, index=i))
                        else:
                            pil_image = TDWUtils.get_pil_image(img_identifier, i)
                        if pass_mask != '_img':
                            pix = np.array(pil_image)
                            pix = cv2.cvtColor(pix, cv2.COLOR_BGR2RGB)
                            cv2.imshow(pass_mask, pix)
                            cv2.waitKey(1)

        handleKeyboard(keyboard_pressed, m) # Se llama a la función que gestiona las acciones en función de las teclas presionadas
        keyboard_pressed = [] # Se reinicia la lista
    cv2.destroyAllWindows()
