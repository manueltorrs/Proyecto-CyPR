#!/bin/env python3
from magnebot import Magnebot

m = Magnebot(launch_build=True)

m.init_floorplan_scene("2b", 0, 1)

m.state.save_images("test_image_output")

m.end()
