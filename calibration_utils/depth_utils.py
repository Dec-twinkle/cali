#-*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import numpy as np
def get_imgpoint_depth(imgpoints,objpoints,depth_img):
    """
    获取图片对应点的深度值，注意rgb图片要与深度图片align
    :param imgpoints:
    :param depth_img:
    :return:
    """
    objPoint_acc = np.array([])
    depth_point_acc = np.array([])
    imgPoint_acc = np.array([])
    n = imgpoints.shape[0]
    for j in range(n):
        depth = depth_img[int(imgpoints[j, 1]), int(imgpoints[j, 0])] / 1000.0
        if depth == 0:
            continue
        objPoint_acc = np.append(objPoint_acc, objpoints[j, :])
        imgPoint_acc = np.append(imgPoint_acc, imgpoints[j, :])

        # depth_point_acc = np.append(depth_point_acc,Point_cam_cood[i,:])
        depth_point_acc = np.append(depth_point_acc, depth)
    objPoint_acc = objPoint_acc.reshape([-1, 2])
    imgPoint_acc = imgPoint_acc.reshape([-1, 2])
    depth_point_acc = depth_point_acc.reshape([-1, 1])
    return imgPoint_acc, objPoint_acc, depth_point_acc