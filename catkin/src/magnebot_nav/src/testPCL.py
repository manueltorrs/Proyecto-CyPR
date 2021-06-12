#!/bin/env python3

import numpy as np
import rospy
import ipdb
import open3d as o3d
from open3d_ros_helper import open3d_ros_helper as orh
import copy

if __name__ == "__main__":
    rospy.init_node("nodo_culero")
    img = o3d.io.read_point_cloud("/home/paco/Proyecto-CyPR/catkin/src/magnebot_nav/pcl1.ply")
    img2 = copy.deepcopy(img)
    R = img2.get_rotation_matrix_from_xyz((-np.pi/2, 0, 0))
    img2.rotate(R)#, center=(0,0,0))
    # print(type(img))
    rospc = orh.o3dpc_to_rospc(img)
    rospc2 = orh.o3dpc_to_rospc(img2)
    # print(type(rospc))
    pub = rospy.Publisher("/topic_culero",type(rospc),queue_size=0)
    pub2 = rospy.Publisher("/topic_culero2",type(rospc),queue_size=0)
    rospc.header.frame_id = "map"
    rospc2.header.frame_id = "map"
    while True:
        pub.publish(rospc)
        pub2.publish(rospc2)
        rospy.sleep(1)

