#!/bin/env python3

import numpy as np
import ipdb
import open3d as o3d

if __name__ == "__main__":
    x = np.linspace(-3, 3, 401)
    meshX, meshY= np.meshgrid(x, x)
    z = np.sinc((np.power(meshX, 2) + np.power(meshY, 2)))
    zNorm = (z - z.min()) / (z.max() - z.min())
    xyz = np.zeros((np.size(meshX), 3))
    xyz[:, 0] = np.reshape(meshX, -1)
    xyz[:, 1] = np.reshape(meshY, -1)
    xyz[:, 2] = np.reshape(zNorm, -1)
    print("XYZ")
    print(xyz)

    ipdb.set_trace()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d.io.write_point_cloud("test.ply", pcd)
    pcdLoad = o3d.io.read_point_cloud("test.ply")
    while 1:
        o3d.visualization.draw([pcdLoad])

