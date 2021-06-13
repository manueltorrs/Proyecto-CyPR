#!/bin/env python3
"""
Ros module.
Publics Point Cloud to /pc2_publisher topic and reads movements over /magnebot/cmd_vel topic
"""
from magnebot import Magnebot
import numpy as np
import ipdb
import rospy
import open3d as o3d
from sensor_msgs.point_cloud2 import PointCloud2
from geometry_msgs.msg import Twist
from tdw.output_data import OutputData, Images, Keyboard
from open3d_ros_helper import open3d_ros_helper as orh

UNINIT = object()
m = UNINIT
checkMove = False


def movement_callback(msg: Twist):
    """
    Callback function for ROS subscriber.
    """
    global m
    global checkMove
    rotation = msg.angular.z
    velocity = msg.linear.x
    m.turn_by(rotation)
    m.move_by(velocity)
    checkMove = True

def main():
    global m
    global checkMove
    if m is UNINIT:
        m = Magnebot(launch_build=True)

    m.init_floorplan_scene("2b", 0, 2)
    points = m.state.get_point_cloud()

    rospy.init_node("magnebot_node")
    movement_sub = rospy.Subscriber("/magnebot/cmd_vel",Twist, callback=movement_callback)
    pub = rospy.Publisher("/pc2_publisher",PointCloud2,queue_size=0)

    # Change points size from (3, 256, 256) to (n, 3) to visualize point cloud
    # Where n is 256x256 and 3 each dimension (x, y, z)
    xyz = np.zeros((np.size(points[0,:,:]), 3))
    xyz[:, 0] = np.reshape(points[0, :, :], -1)
    xyz[:, 1] = np.reshape(points[1, :, :], -1)
    xyz[:, 2] = np.reshape(points[2, :, :], -1)

    aux = np.zeros((np.size(points[0,:,:]), 3))
    pcd = o3d.geometry.PointCloud()
    rotMat = pcd.get_rotation_matrix_from_xyz((-np.pi/2, 0, 0))

    while True:
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.rotate(rotMat)
        rospc = orh.o3dpc_to_rospc(pcd)
        rospc.header.frame_id = "map"
        pub.publish(rospc)
        rospy.sleep(0.001)
        if checkMove:
            points = m.state.get_point_cloud()
            aux[:, 0] = np.reshape(points[0, :, :], -1)
            aux[:, 1] = np.reshape(points[1, :, :], -1)
            aux[:, 2] = np.reshape(points[2, :, :], -1)
            xyz = np.append(xyz, aux, axis=0)
            checkMove = False

    m.end()


if __name__ == "__main__":
    main()
