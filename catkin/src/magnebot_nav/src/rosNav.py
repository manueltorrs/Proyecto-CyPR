#!/bin/env python3
from magnebot import Magnebot
import numpy as np
import ipdb
import rospy
import open3d as o3d
# from std_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import PointCloud2
from tdw.output_data import OutputData, Images, Keyboard
from open3d_ros_helper import open3d_ros_helper as orh
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


if __name__ == "__main__":
    m = Magnebot(launch_build=True)

    m.init_floorplan_scene("2b", 0, 2)
    points = m.state.get_point_cloud()

    rospy.init_node("magnebot_node")
    pub = rospy.Publisher("/pc2_publisher",PointCloud2,queue_size=0)

    # Change points size from (3, 256, 256) to (n, 3) to visualize point cloud
    # Where n is 256x256 and 3 each dimension (x, y, z)
    xyz = np.zeros((np.size(points[0,:,:]), 3))
    xyz[:, 0] = np.reshape(points[0, :, :], -1)
    xyz[:, 1] = np.reshape(points[1, :, :], -1)
    xyz[:, 2] = np.reshape(points[2, :, :], -1)


    aux = np.zeros((np.size(points[0,:,:]), 3))
    pcd = o3d.geometry.PointCloud()
    R = pcd.get_rotation_matrix_from_xyz((np.pi/2, 0, 0))
    pcd.rotate(R, center=(0,0,0))

    # o3d.visualization.ViewControl.camera_local_rotate(0, 90, 0)
    # o3d.visualization.draw([pcd])

    while True:
        pcd.points = o3d.utility.Vector3dVector(xyz)
        rospc = orh.o3dpc_to_rospc(pcd)
        rospc.header.frame_id = "map"
        pub.publish(rospc)
        rospy.sleep(1)
        m.turn_by(-10)
        points = m.state.get_point_cloud()
        aux[:, 0] = np.reshape(points[0, :, :], -1)
        aux[:, 1] = np.reshape(points[1, :, :], -1)
        aux[:, 2] = np.reshape(points[2, :, :], -1)
        xyz = np.append(xyz, aux, axis=0)

    m.end()
