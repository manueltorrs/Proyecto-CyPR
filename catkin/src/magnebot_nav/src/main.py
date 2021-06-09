#!/bin/env python3
from magnebot import Magnebot
import numpy as np
import ipdb
import rospy
import open3d as o3d
# from std_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import PointCloud2
# from std_msgs.msg import Image as SensorImage
# from PIL import Image as PILImage


def stop():
    done = True
    m.communicate({"$type": "terminate"})

def move(magnebot, target = 1500):
    commands = []
    for wheel in magnebot.magnebot_static.wheels:
        commands.append({"$type": "set_revolute_target",
                                 "target": target,
                                 "joint_id": magnebot.magnebot_static.wheels[wheel]})
    magnebot.communicate(commands)
    done = True

# rospy.init_node("Nodo_1")

# pc_pub = rospy.Publisher("/mgbot/pointcloud", PointCloud2, queue_size=1)
# _ = PointCloud2()

# m = Magnebot(
    # launch_build=True,
    # skip_frames=100)

# # rgb_pub = rospy.Publisher("/mgbot/rgb_img", SensorImage)

# init = 0

# m.init_floorplan_scene("2b", 0, 3)
# while True:
    # m.move_by(0.01)
    # pointcloud = m.state.get_point_cloud()
    # msg = PointCloud2()
    # msg.data = pointcloud
    # pc_pub.publish(msg)
    # if not init:
        # init = 1
        # print("starting to pub")
    # # rgb_img = m.state.get_pil_images()
    # # depth_img = m.state.get_depth_values()
    # m.state.save_images("test_image_output")

if __name__ == "__main__":
    # m = Magnebot(launch_build=True, screen_width=1920, screen_height=1080)
    m = Magnebot(launch_build=True)

    m.init_floorplan_scene("2b", 0, 2)
    # ipdb.set_trace()
    points = m.state.get_point_cloud()
    images = m.state.get_pil_images()
    print("PC: {}".format(points))
    print("Type: {}".format(type(points)))
    print("Shape: {}".format(points.shape))
    m.add_camera(position={"x": 1.43, "y": 1.87, "z": 0.77}, look_at=True, follow=True)

    done = False
    status = False
    # commands = []
    # for wheel in m.magnebot_static.wheels:
        # commands.append({"$type": "set_revolute_target",
                                 # "target": 1500,
                                 # "joint_id": m.magnebot_static.wheels[wheel]})
    # m.listen(key="esc", function=stop)
    # m.listen(key="B", function=move(m))
    ids = 0 
    commands = []
    # for joint in m.magnebot_static.joints.values():
        # if joint.name == "column":
            # ids = joint.id
    # commands.append({"$type": "set_revolute_target",
                     # "joint_id": ids,
                     # "target": 124})
    # m.communicate(commands)
    # # Wait for a bit
    # for i in range(100):
        # m.communicate([])
    

    # for wheel in m.magnebot_static.wheels:
        # commands.append({"$type": "set_revolute_target",
                         # "joint_id": m.magnebot_static.wheels[wheel],
                         # "target": 1200})

    # Change points size from (3, 256, 256) to (n, 3) to visualize point cloud
    # Where n is 256x256 and 3 each dimension (x, y, z)
    xyz = np.zeros((np.size(points[0,:,:]), 3))
    xyz[:, 0] = np.reshape(points[0, :, :], -1)
    xyz[:, 1] = np.reshape(points[1, :, :], -1)
    xyz[:, 2] = np.reshape(points[2, :, :], -1)

    ipdb.set_trace()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)

    o3d.visualization.draw([pcd])
     
     
     
    # countBase = 100
    # countRot = 20
    # m.listen(key='W', commands=[{"$type": "set_revolute_target",
                         # "joint_id": m.magnebot_static.wheels[wheel],
                         # "target": (countBase+1)} for wheel in m.magnebot_static.wheels],
             # events=["press", "hold"])
    # m.listen(key="R", commands={"$type": "set_revolute_target",
                                # "joint_id": ids,
                                # "target": (countRot+10)}, events=["press", "hold"])
    # m.listen(key="E", commands={"$type": "set_revolute_target",
                                # "joint_id": ids,
                                # "target": (countRot-10)}, events=["press", "hold"])
    # m.listen(key='S', function=m.reset_position)
        # # print("Joint name: {}".format(joint))
    # # m.listen(key="R", commands={"$type": "set_revolute_target",
                     # # "joint_id": m.magnebot_static.joints[],
                     # # "target": 124}, events=["press", "hold"])
    # # m.listen(key="w", function=m.move_by(0.001))
    # # m.listen(key="d", function=m.turn_by(0.001))
    # while not done:
        # m.communicate([])
        # # m.turn_by(0.001)
        # # m.move_by(0.01)
    # # m.communicate(commands)

    m.state.save_images("test_image_output")

    m.end()
