#!/bin/env python3
from magnebot import Magnebot
import rospy
# from std_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import PointCloud2
# from std_msgs.msg import Image as SensorImage
# from PIL import Image as PILImage

rospy.init_node("Nodo_1")

pc_pub = rospy.Publisher("/mgbot/pointcloud", PointCloud2, queue_size=1)
_ = PointCloud2()

m = Magnebot(
    launch_build=True,
    skip_frames=100)

# rgb_pub = rospy.Publisher("/mgbot/rgb_img", SensorImage)

init = 0

m.init_floorplan_scene("2b", 0, 3)
while True:
    m.move_by(0.01)
    pointcloud = m.state.get_point_cloud()
    msg = PointCloud2()
    msg.data = pointcloud
    pc_pub.publish(msg)
    if not init:
        init = 1
        print("starting to pub")
    # rgb_img = m.state.get_pil_images()
    # depth_img = m.state.get_depth_values()
    m.state.save_images("test_image_output")

m.end()
