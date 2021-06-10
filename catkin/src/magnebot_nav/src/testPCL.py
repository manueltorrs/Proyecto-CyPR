#!/bin/env python3

import numpy as np
import rospy
import ipdb
import open3d as o3d
from open3d_ros_helper import open3d_ros_helper as orh

if __name__ == "__main__":
    rospy.init_node("nodo_culero")
    img = o3d.io.read_point_cloud("/home/paco/Proyecto-CyPR/catkin/src/magnebot_nav/pcl1.ply")
    # print(type(img))
    rospc = orh.o3dpc_to_rospc(img)
    # print(type(rospc))
    pub = rospy.Publisher("/topic_culero",type(rospc),queue_size=0)
    rospc.header.frame_id = "map"
    while True:
        pub.publish(rospc)
        rospy.sleep(1)

